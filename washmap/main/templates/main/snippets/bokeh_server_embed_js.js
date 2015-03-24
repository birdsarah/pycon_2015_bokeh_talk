{% with modulename=applet.modulename classname=applet.classname parentname=applet.parentname %}
    {# This is a copy of bokeh/server/templates/app.js #}
    window.{{ modulename }} = {};
    {{ modulename }} = window.{{ modulename }};
    {{ modulename }}.main = function(){
    {{ classname }}View  = Bokeh.{{ parentname }}.View.extend({
    });
    {{ classname }} = Bokeh.{{ parentname }}.Model.extend({
        type : "{{classname}}",
        default_view : {{ classname }}View
    });
    {{ classname }}s = Backbone.Collection.extend({
        model : {{ classname }}
    });
    Bokeh.Collections.register("{{ classname }}", new {{classname}}s ());
    }

    {# Extracted from server embed examples - we call the main function #}
    window.{{ classname }}.main();
{% endwith %}

{# Extracted relevant line from bokeh/_templates/autoload.js #}
Bokeh.embed.inject_plot("{{ applet.elementid }}", null);
