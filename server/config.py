import os, urlparse

pub_zmqaddr = "ipc:///tmp/0"
sub_zmqaddr = "ipc:///tmp/1"
run_forwarder = True
model_backend = {'type': 'shelve'}
secret_key = os.environ.get('BOKEH_SECRET_KEY', 'another secret key')
multi_user = False
scripts = [
    'blueprints/sliders_app_hbox.py',
    'blueprints/washmap_app.py',
]
