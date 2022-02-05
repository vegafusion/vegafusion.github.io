# Altair Renderer and Data Transformer
## VegaFusion Renderer
As an alternative to using the `VegaFusionWidget` directly, VegaFusion provides a custom [Altair renderer](https://altair-viz.github.io/user_guide/display_frontends.html). This uses the a `VegaFusionWidget` for display, but it doesn't require the explicit construction of a `VegaFusionWidget` instance.

## VegaFusion Data Transformer
VegaFusion also provides a custom [data transformer](https://altair-viz.github.io/user_guide/data_transformers.html). When an Altair chart is created based on a pandas DataFrame, the VegaFusion transformer will extract the DataFrame and save it to a [feather file](https://arrow.apache.org/docs/python/feather.html) in the `_vegafusion_data` directory in the current directory.  The feather file's name is generated based on a hash of the DataFrame's contents, so new files will only be added to the directory when charts are created with new DataFrames.  Feel free to delete the directory when no interactive VegaFusion charts are currently being displayed, but deleting the directory while an interactive chart is being displayed may result in an error.

## Activating Renderer and Data Transformer
The VegaFusion renderer and data transformer can both be activated using the `enable` function from the `vegafusion-jupyter` package.

```python
import vegafusion as vf
vf.jupyter.enable()
```

After calling `enable`, subsequent Altair charts will automatically be rendered using VegaFusion.

```python
import altair as alt
from vega_datasets import data

source = data.movies.url

alt.Chart(source).mark_bar().encode(
    alt.X("IMDB_Rating:Q", bin=True),
    y='count()',
)
```

<img width="519" alt="Histogram" src="https://user-images.githubusercontent.com/15064365/148783521-81c5d183-0a6f-41ca-a0c1-0c76e23d65df.png">

