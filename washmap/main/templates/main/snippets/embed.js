<script>
    bokehJS.done( function () {
        {% for figure in figures %}
            {% include 'main/snippets/bokeh_script.js' %}
        {% endfor %}
        resize_figures();
    });
</script>
