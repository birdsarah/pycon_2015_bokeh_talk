"""
This file demonstrates a bokeh applet, which can be viewed directly
on a bokeh-server. See the README.md file in this directory for
instructions on running.
"""

import numpy as np

from bokeh.models import ColumnDataSource, Plot
from bokeh.models.widgets import HBox, Slider, TextInput, VBoxForm
from bokeh.properties import Instance


class SlidersApp(HBox):

    """
    Note these are not needed server side, because the server side code
    doesn't use/reference them.
    js_model = "SlidersApp"
    parent_model = "HBox"
    """

    inputs = Instance(VBoxForm)

    text = Instance(TextInput)

    offset = Instance(Slider)
    amplitude = Instance(Slider)
    phase = Instance(Slider)
    freq = Instance(Slider)

    plot = Instance(Plot)
    source = Instance(ColumnDataSource)

    """
    THIS IS ONLY NEEDED ON THE CLIENT SIDE.
    @classmethod
    def create(cls):
        obj = cls()

        obj.source = ColumnDataSource(data=dict(x=[], y=[]))

        obj.text = TextInput(
            title="title", name='title', value='my sine wave'
        )

        obj.offset = Slider(
            title="offset", name='offset',
            value=0.0, start=-5.0, end=5.0, step=0.1
        )
        obj.amplitude = Slider(
            title="amplitude", name='amplitude',
            value=1.0, start=-5.0, end=5.0
        )
        obj.phase = Slider(
            title="phase", name='phase',
            value=0.0, start=0.0, end=2 * np.pi
        )
        obj.freq = Slider(
            title="frequency", name='frequency',
            value=1.0, start=0.1, end=5.1
        )

        toolset = ""

        # Generate a figure container
        obj.plot = figure(
            title_text_font_size="12pt",
            plot_height=400,
            plot_width=400,
            tools=toolset,
            toolbar_location=None,
            title=obj.text.value,
            x_range=[0, 4 * np.pi],
            y_range=[-2.5, 2.5]
        )

        # Plot the line by the x,y values in the source property
        obj.plot.line(
            'x', 'y', source=obj.source,
            line_width=3,
            line_alpha=0.6
        )

        obj.update_data()

        obj.inputs = VBoxForm(
            children=[
                obj.text, obj.offset, obj.amplitude, obj.phase, obj.freq
            ]
        )

        obj.children = [obj.inputs, obj.plot]

        return obj
    """

    def setup_events(self):
        if not self.text:
            return

        # Text box event registration
        self.text.on_change('value', self, 'input_change')

        # Slider event registration
        for w in ["offset", "amplitude", "phase", "freq"]:
            getattr(self, w).on_change('value', self, 'input_change')

    def input_change(self, obj, attrname, old, new):
        self.update_data()
        self.plot.title = self.text.value

    def update_data(self):
        N = 200

        # Get the current slider values
        a = self.amplitude.value
        b = self.offset.value
        w = self.phase.value
        k = self.freq.value

        # Generate the sine wave
        x = np.linspace(0, 4 * np.pi, N)
        y = a * np.sin(k * x + w) + b

        self.source.data = dict(x=x, y=y)
