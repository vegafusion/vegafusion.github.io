# Debouncing
The `VegaFusionWidget` provides configurable [debouncing](https://css-tricks.com/debouncing-throttling-explained-examples/) to control how frequently user interaction updates are sent from the browser to the Python kernel.  

The widget's `debounce_wait` and `debounce_max_wait` properties correspond to the `wait` and `max_wait` properties of the [lodash debounce](https://lodash.com/docs/#debounce) function. VegaFusion uses sensible defaults (`debounce_wait` of 30ms and `debounce_max_wait` of 60ms), but it can be useful to increase the default values to handle interactions on large datasets.

Here is the specification for a chart that provides histogram data selection on a 10 million row dataset.

```python
import altair as alt
from vega_datasets import data
import pandas as pd
import vegafusion as vf

source = pd.concat([data.flights_2k()] * 5000).reset_index()

brush = alt.selection(type='interval', encodings=['x'])

# Define the base chart, with the common parts of the
# background and highlights
base = alt.Chart().mark_bar().encode(
    x=alt.X(alt.repeat('column'), type='quantitative', bin=alt.Bin(maxbins=20)),
    y='count()'
).properties(
    width=160,
    height=130
)

# gray background with selection
background = base.encode(
    color=alt.value('#ddd')
).add_selection(brush)

# blue highlights on the transformed data
highlight = base.transform_filter(brush)

# layer the two charts & repeat
chart = alt.layer(
    background,
    highlight,
    data=source
).repeat(column=["distance", "delay"])

widget = vf.jupyter.VegaFusionWidget(chart)
widget
```

## Default debouncing
 Here is what the default interactivity looks like using on a 2015 Macbook pro. 

<video width="600" controls>
  <source src="https://user-images.githubusercontent.com/15064365/148806511-879bd7c5-78d3-44f6-8dbe-1c654bd0e89c.mov" type="video/mp4">
This browser does not support the video tag.
</video>

You can see that the server falls behind, resulting in a poor interaction experience.

## Slower debouncing
Debouncing can be adjusted to improve the interaction experience.  By setting `debounce_wait` to 50ms and `debounce_max_wait` to `None` the client will not send a request to the server until there has been a period of 50ms without any user interaction events.  This results in a user interaction experience where the chart is not updated until the full interaction has completed.

```python
vf.jupyter.VegaFusionWidget(chart, debounce_wait=50, debounce_max_wait=None)
```

<video width="600" controls>
  <source src="https://user-images.githubusercontent.com/15064365/148806495-e2df06f9-655d-401f-8534-f2c41985b6ae.mov" type="video/mp4">
This browser does not support the video tag.
</video>
