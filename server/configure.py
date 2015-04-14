from __future__ import print_function

import logging
import time
import json
import imp
import sys
import zmq
import redis

from os.path import dirname
from six.moves.queue import Queue

from bokeh.server.app import bokeh_app
from bokeh.server.configure import StaticFilter
from bokeh.server.models import docs, convenience as mconv
from bokeh.server.forwarder import Forwarder
from bokeh.server.server_backends import (
    InMemoryServerModelStorage,
    MultiUserAuthentication,
    RedisServerModelStorage,
    ShelveServerModelStorage,
    SingleUserAuthentication,
)
from bokeh.server.serverbb import (
    InMemoryBackboneStorage,
    RedisBackboneStorage,
    ShelveBackboneStorage
)
from bokeh.server.settings import settings as server_settings
from bokeh.server.websocket import WebSocketManager, WebSocketHandler
from bokeh.server.zmqpub import Publisher
from bokeh.server.zmqsub import Subscriber

from tornado.web import Application, FallbackHandler
from tornado.wsgi import WSGIContainer

timeout = 0.1


def configure_flask(config_file=None):
    server_settings.from_file(config_file)
    for handler in logging.getLogger().handlers:
        handler.addFilter(StaticFilter())

    # must import views before running apps
    from bokeh.server.views import deps
    backend = server_settings.model_backend
    if backend['type'] == 'redis':
        rhost = backend.get('redis_host', '127.0.0.1')
        rport = backend.get('redis_port', 6379)
        rpass = backend.get('redis_password')
        bbdb = backend.get('backbone_storage_db_id')
        smdb = backend.get('servermodel_storage_db_id')
        bbstorage = RedisBackboneStorage(
            redis.Redis(host=rhost, port=rport, password=rpass, db=bbdb)
        )
        servermodel_storage = RedisServerModelStorage(
            redis.Redis(host=rhost, port=rport, password=rpass, db=smdb)
        )
    elif backend['type'] == 'memory':
        bbstorage = InMemoryBackboneStorage()
        servermodel_storage = InMemoryServerModelStorage()

    elif backend['type'] == 'shelve':
        bbstorage = ShelveBackboneStorage()
        servermodel_storage = ShelveServerModelStorage()

    if not server_settings.multi_user:
        authentication = SingleUserAuthentication()
    else:
        authentication = MultiUserAuthentication()
    bokeh_app.url_prefix = server_settings.url_prefix
    bokeh_app.publisher = Publisher(server_settings.ctx,
                                    server_settings.pub_zmqaddr, Queue())

    for script in server_settings.scripts:
        script_dir = dirname(script)
        if script_dir not in sys.path:
            print("adding %s to python path" % script_dir)
            sys.path.append(script_dir)
        print("importing %s" % script)
        imp.load_source("_bokeh_app", script)

    bokeh_app.setup(
        backend,
        bbstorage,
        servermodel_storage,
        authentication,
    )


class PingingSubscriber(Subscriber):
    def __init__(self, ctx, addrs, wsmanager):
        self.keep_alive_queue = {}
        self.timer = 0
        super(PingingSubscriber, self).__init__(ctx, addrs, wsmanager)

    def handle_keepalive(self, log):
        self.timer += 1
        # Ping from the server every ~40s (keeps heroku alive)
        if self.timer > 400:
            self.timer = 0
            currenttime = time.time()
            for topic, timestamp in self.keep_alive_queue.items():
                # Stop sending keep alives after 30 minutes.
                if currenttime - timestamp > (60 * 30):
                    del self.keep_alive_queue[topic]
                else:
                    log.warning("Keep Alive ping sent")
                    self.wsmanager.send(
                        topic,
                        json.dumps({"msgtype": "Keep Alive"}),
                        exclude=[])

    def process_messages(self, socks):
        for socket, v in socks.items():
            msg = socket.recv_json()
            topic, msg, exclude = msg['topic'], msg['msg'], msg['exclude']
            self.keep_alive_queue[topic] = time.time()
            self.wsmanager.send(topic, msg, exclude=exclude)

    def run(self):
        sockets = []
        poller = zmq.Poller()
        log = logging.getLogger(__name__)
        for addr in self.addrs:
            socket = self.ctx.socket(zmq.SUB)
            socket.connect(addr)
            socket.setsockopt_string(zmq.SUBSCRIBE, u"")
            sockets.append(socket)
            poller.register(socket, zmq.POLLIN)
        try:
            while not self.kill:
                socks = dict(poller.poll(timeout * 1000))
                self.handle_keepalive(log)
                self.process_messages(socks)
        except zmq.ContextTerminated:
            pass
        finally:
            for s in sockets:
                s.close()


class TornadoApplication(Application):
    def __init__(self, flask_app, **settings):
        self.flask_app = flask_app
        tornado_flask = WSGIContainer(flask_app)
        url_prefix = server_settings.url_prefix
        handlers = [
            (url_prefix + "/bokeh/sub", WebSocketHandler),
            (r".*", FallbackHandler, dict(fallback=tornado_flask))
        ]
        super(TornadoApplication, self).__init__(handlers, **settings)
        self.wsmanager = WebSocketManager()

        def auth(auth, docid):
            if docid.startswith("temporary-"):
                return True
            doc = docs.Doc.load(bokeh_app.servermodel_storage, docid)
            status = mconv.can_read_doc_api(doc, auth)
            return status
        self.wsmanager.register_auth('bokehplot', auth)

        self.subscriber = PingingSubscriber(server_settings.ctx,
                                            [server_settings.sub_zmqaddr],
                                            self.wsmanager)
        self.forwarder = Forwarder(server_settings.ctx,
                                   server_settings.pub_zmqaddr,
                                   server_settings.sub_zmqaddr)

    def start_threads(self):
        bokeh_app.publisher.start()
        self.subscriber.start()
        if self.forwarder:
            self.forwarder.start()

    def stop_threads(self):
        bokeh_app.publisher.stop()
        self.subscriber.stop()
        if self.forwarder:
            self.forwarder.stop()
