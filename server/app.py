from configure import configure_flask, TornadoApplication
from bokeh.server.app import app
from bokeh.server.configure import register_blueprint
from bokeh.server.settings import settings as server_settings

configure_flask(config_file='config.py')
register_blueprint()

app.secret_key = server_settings.secret_key
tornado_app = TornadoApplication(app, debug=server_settings.debug)
tornado_app.start_threads()
