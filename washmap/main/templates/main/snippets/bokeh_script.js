var modelid = "{{ figure.modelid }}";
var modeltype = "{{ figure.modeltype }}";
var elementid = "{{ figure.elementid }}";
Bokeh.logger.info("start plotting " + elementid);
var all_models = {{ figure.all_models|safe }};
Bokeh.load_models(all_models);
var model = Bokeh.Collections(modeltype).get(modelid);
var view = new model.default_view({model: model, el: '#{{ figure.elementid }}'});
Bokeh.index[modelid] = view
