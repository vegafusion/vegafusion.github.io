# Altair Renderer and Data Transformer
## VegaFusion Renderer
As an alternative to using `VegaFusionWidget` directly, VegaFusion provides a custom [Altair renderer](https://altair-viz.github.io/user_guide/display_frontends.html). This uses the `VegaFusionWidget` for display, but it doesn't require explicit construction of a `VegaFusionWidget` instance.

## VegaFusion Data Transformer
VegaFusion also provides a custom [data transformer](https://altair-viz.github.io/user_guide/data_transformers.html). When an Altair chart is created based on a pandas DataFrame, the VegaFusion transformer will extract the DataFrame and save it to a feather file in the `_vegafusion_data` directory in the current directory

## Activating Renderer and Data Transformer
The VegaFusion renderer and data transformer can both be activated using the `enable` function from the `vegafusion-jupyter` package.

```python
import vegafusion_jupyter as vf
vf.enable()
```

After calling `enable`, subsequent Altair charts will be rendered using VegaFusion

```python
import altair as alt
from vega_datasets import data

source = data.movies.url

chart = alt.Chart(source).mark_bar().encode(
    alt.X("IMDB_Rating:Q", bin=True),
    y='count()',
)
```

<img width="519" alt="Histogram" src="https://user-images.githubusercontent.com/15064365/148783521-81c5d183-0a6f-41ca-a0c1-0c76e23d65df.png">

