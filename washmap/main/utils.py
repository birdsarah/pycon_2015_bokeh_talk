import uuid
import json

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


def build_coords_lists(boundary_series):
    def get_coords(boundary_cell):
        boundary = json.loads(boundary_cell)
        xs = []
        ys = []
        if boundary['type'] == 'MultiPolygon':
            for polygon in boundary['coordinates']:
                for coord in polygon:
                    if len(coord) == 2:
                        xs.append(coord[0])
                        ys.append(coord[1])
                    else:
                        for co in coord:
                            xs.append(co[0])
                            ys.append(co[1])
        elif boundary['type'] == 'Polygon':
            polygon = boundary['coordinates'][0]
            for coord in polygon:
                xs.append(coord[0])
                ys.append(coord[1])
        return xs, ys
    xs, ys = zip(*boundary_series.map(get_coords))
    return xs, ys
