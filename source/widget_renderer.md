# Widget Renderer

The VegaFusion widget renderer uses a custom Jupyter Widget to display Altair charts and maintain a live connection between the Python kernel and the chart in the browser.  This is a more complex setup than the mime renderer, but it makes it possible for chart [interactions](https://altair-viz.github.io/user_guide/interactions.html) (e.g. histogram selection) to be processed by the VegaFusion runtime.  Note that for static charts, the mime renderer provides the same benefits as the widget renderer without requiring the custom Jupyter Widget extension.

## Installation
The widget renderer is included in the `vegafusion-jupyter` Python package:

```bash
pip install "vegafusion-jupyter[embed]"
```

The required Jupyter Widget extensions for the Classic Notebook and JupyterLab are bundled with the Python package and should be enabled automatically. 

## Activation
The VegaFusion widget renderer can be enabled using the `vegafusion.enable_widget()` function. Here is a full example of an interactive chart that is displayed using the widget renderer:

```python
import pandas as pd
import altair as alt
import vegafusion as vf

vf.enable_widget()

flights = pd.read_parquet(
    "https://vegafusion-datasets.s3.amazonaws.com/vega/flights_1m.parquet"
)

brush = alt.selection_interval(encodings=['x'])

# Define the base chart, with the common parts of the
# background and highlights
base = alt.Chart().mark_bar().encode(
    x=alt.X(alt.repeat('column')).bin(maxbins=20),
    y='count()'
).properties(
    width=160,
    height=130
)

# gray background with selection
background = base.encode(
    color=alt.value('#ddd')
).add_params(brush)

# blue highlights on the selected data
highlight = base.transform_filter(brush)

# layer the two charts & repeat
chart = alt.layer(
    background,
    highlight,
    data=flights
).transform_calculate(
    "time",
    "hours(datum.date)"
).repeat(column=["distance", "delay", "time"])
chart
```

<video width="700" controls>
  <source src="https://user-images.githubusercontent.com/15064365/209974420-480121b4-b206-4bb2-b473-0c663e38ea5e.mov" type="video/mp4">
This browser does not support the video tag.
</video>

## Feather Data Transformer
The VegaFusion widget renderer provides a custom [data transformer](https://altair-viz.github.io/user_guide/data_transformers.html). When an Altair chart is created based on a pandas DataFrame, the `VegaFusionWidget`'s data transformer will extract the DataFrame and save it to a [feather file](https://arrow.apache.org/docs/python/feather.html) in a `_vegafusion_data` directory in the current directory.  The feather file's name is generated based on a hash of the DataFrame's contents, so new files will only be added to the directory when charts are created with new DataFrames.  Feel free to delete the directory when no interactive VegaFusion charts are currently being displayed, but deleting the directory while an interactive chart is being displayed may result in an error.

This approach is implemented by the `"vegafusion-feather"` data transformer, which is automatically enabled by the `vegafusion.enable_widget()` function or when using `VegaFusionWidget` directly.

### Customizing Feather File Directory
The directory that these feather files are written to can be customized using the `data_dir` argument to `vegafusion.enable_widget()`. For example:

```python
import vegafusion as vf
vf.enable_widget(data_dir='my_data_dir')
```
