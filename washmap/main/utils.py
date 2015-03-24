import uuid

from bokeh.document import Document
from bokeh.protocol import serialize_json
from bokeh.session import Session


class BokehScriptComponents(object):
    def __init__(self, plot_object, elementid=None, min_width=700):
        if not elementid:
            elementid = str(uuid.uuid4())
        self.elementid = elementid
        self.min_width = min_width
        self.modelid = plot_object.ref["id"]
        self.modeltype = plot_object.ref["type"]
        self.all_models = serialize_json(plot_object.dump())


def app_document_no_tag(prefix, url="default"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            document = Document()
            session = Session(name=url, root_url=url)
            session.use_doc(document.docid)
            session.load_document(document)
            session.publish()
            document.autoadd = False
            document.autostore = False

            obj = func(*args, **kwargs)
            obj._docid = session.docid
            obj._root_url = session.root_url

            document.add(obj)
            session.store_document(document)
            return obj
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator
