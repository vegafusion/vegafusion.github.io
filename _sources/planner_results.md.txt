# Planner Results
As discussed in the {ref}`planner` section, VegaFusion uses a planning phase to split an input Vega specification into a specification to run on the client and a specification to run on the server.  Additionally, a communication plan is produced that specifies which signal and dataset values must be passed between the server and client to preserve interactivity.  For debugging, the client spec, server spec, and communication plan are available as properties on the `VegaFusionWidget` instance after the chart has been displayed.

First, wrap the chart in a `VegaFusionWidget` and display it.

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

widget = vf.VegaFusionWidget(alt.layer(bars, line, data=source))
widget
```
<video width="600" controls>
  <source src="https://user-images.githubusercontent.com/15064365/148408648-43a5cfd0-b0d8-456e-a77a-dd344d8d07df.mov" type="video/mp4">
This browser does not support the video tag.
</video>

Then print out the value of the following widget properties:

 - `widget.spec`: This is the Vega-Lite specification created by Altair
 - `widget.full_vega_spec`: This is the Vega specification produced by Vega-Lite
 - `widget.server_vega_spec`: This is the portion of the full Vega spec that was planned to run on the server (The Python kernel in case)
 - `widget.client_vega_spec`: This is the portion of the full Vega spec that was planned to run on the client, being rendered by Vega.js
 - `widget.comm_plan`: This is the specification of which signals and datasets must be transfered between the client and server in order to preserve the interactive behavior of the original specification.
