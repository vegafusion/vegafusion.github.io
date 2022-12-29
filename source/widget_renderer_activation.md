# Activating Widget Renderer
The VegaFusion widget renderer can be activated using the `enable_widget()` function from the `vegafusion` package.

```python
import vegafusion as vf
vf.enable_widget()
```

After calling `enable_widget()`, subsequent Altair charts will automatically be displayed using `VegaFusionWidget`.

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

