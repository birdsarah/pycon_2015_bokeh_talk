<script>
    bokehJS.done( function () {
        {% for figure in figures %}
            {% include 'main/snippets/bokeh_script.js' %}
        {% endfor %}
        resize_figures();
    });
    function resize_figures() {
        var width, plot_width, plot_height;
        {% for figure in figures %}
            element = $("#{{ figure.elementid }}");
            element_width = element.width();
            element_min_width = element.attr("data-min-width");
            element.removeClass("screen-too-small");
            if ( element_width < element_min_width ) {
                element.addClass("screen-too-small"); 
            }

            cur_width = $("#{{ figure.elementid }} .bk-canvas-wrapper").width();
            cur_height = $("#{{ figure.elementid }} .bk-canvas-wrapper").height();
            aspect_ratio = cur_width / cur_height;
            plot_width = Math.max(element_width, 300);
            plot_height = parseInt(plot_width / aspect_ratio);
            Bokeh.index["{{ figure.modelid }}"].model.set('plot_width', plot_width);
            Bokeh.index["{{ figure.modelid }}"].model.set('plot_height', plot_height);
        {% endfor %}
    }
    $(window).resize(resize_figures);
</script>
