# Verbosity
The `VegaFusionWidget` provides a `verbose` flag that can be used to enable verbose logging of the messages sent between the server and client.  When set, log messages are written to the browser's JavaScript console.

Here is an example of enabling verbose logging for the [interactive average](https://altair-viz.github.io/gallery/selection_layer_bar_month.html) example.

```python
import altair as alt
from vega_datasets import data

source = data.seattle_weather()
brush = alt.selection(type='interval', encodings=['x'])

bars = alt.Chart().mark_bar().encode(
    x='month(date):O',
    y='mean(precipitation):Q',
    opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7)),
).add_selection(
    brush
)

line = alt.Chart().mark_rule(color='firebrick').encode(
    y='mean(precipitation):Q',
    size=alt.SizeValue(3)
).transform_filter(
    brush
)

chart = alt.layer(bars, line, data=source)
widget = vf.VegaFusionWidget(chart, verbose=True)
widget
```

<video width="600" controls>
  <source src="https://user-images.githubusercontent.com/15064365/148408648-43a5cfd0-b0d8-456e-a77a-dd344d8d07df.mov" type="video/mp4">
This browser does not support the video tag.
</video>

Now open the browser's JavaScript console and then click and drag on the chart to create a selection. Messages containing the selection region and average value will be written to the console.
