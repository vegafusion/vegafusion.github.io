# Mime Renderer

The VegaFusion mime renderer makes it possible to display Altair charts that reference large datasets in a wide variety of Python notebook and compute environments.  While the mime renderer is compatible with both static and interactive charts, the widget renderer is better suited for interactive charts that reference large datasets.

## Installation
The mime renderer is included in the `vegafusion` Python package:

```bash
pip install "vegafusion[embed]"
```

## Activation
The VegaFusion mime renderer is enabled using the `vegafusion.enable_mime()` function. For example:

```python
import vegafusion as vf
vf.enable_mime(mimetype="vega")
...
chart
```

The mime renderer can also be enabled temporarily by using `vegafusion.enable_mime()` as a context manager:

```python
import vegafusion as vf
from IPython.display import display
with vf.enable_mime(mimetype="vega"):
    ...
    display(chart)
```

When enabled, Altair charts will be automatically processed by VegaFusion when they are displayed. Here is an example of a 1 million row histogram that could not be displayed without a VegaFusion renderer:

```python
import pandas as pd
import altair as alt
import vegafusion as vf

vf.enable_mime(mimetype="vega")
flights = pd.read_parquet(
    "https://vegafusion-datasets.s3.amazonaws.com/vega/flights_1m.parquet"
)

alt.Chart(flights).mark_bar().encode(
    alt.X("delay", bin=alt.Bin(maxbins=30)),
    alt.Y("count()")
)
```
![Flight Delay Histogram](https://user-images.githubusercontent.com/15064365/209973961-948b9d10-4202-4547-bbc8-d1981dcc8c4e.png)

## Supported mimetypes
The mime renderer can display the resulting Vega spec using a variety of mimetypes

### `vega` (default)
When the `mimetype` argument to `vf.enable_mime()` is set to `"vega"` (the default), the resulting mime bundle will have type `"application/vnd.vega.v5+json"` and will contain the Vega spec. This approach works in JupyterLab, Visual Studio Code, Hex, and other compute environments that include built-in support for rendering Vega charts. No internet connection is required, but note that this mimetype is not supported by the classic Jupyter Notebook.

### `html`
When the `mimetype` argument is set to `"html"`, the resulting mime bundle will have type `"text/html"` and will contain an HTML snippet that loads several JavaScript dependencies from a CDN location and displays the Vega spec using [`vega-embed`](https://github.com/vega/vega-embed). This renderer is compatible with both the classic Jupyter Notebook and JupyterLab, but note that it does require an active internet connection.

### `html-colab`
The `"html-colab"` mimetype is a variant of `"html"` that is customized to work in [Google Colab](https://colab.research.google.com/). It can also be specified as `"colab"`.

### `html-kaggle`
The `"html-kaggle"` mimetype is a variant of `"html"` that is customized to work in [Kaggle Notebooks](https://www.kaggle.com/docs/notebooks). It can also be specified as `"kaggle"`.

### `svg`
When the `mimetype` argument is set to `"svg"`, the resulting mime bundle will have type `"image/svg+xml"` and will contain a static SVG image of the chart.

### `png`
When the `mimetype` argument is set to `"png"`, the resulting mime bundle will have type `"image/png"` and will contain a static PNG image of the chart.

## How it works
The mime renderer plugs into Altair's [data transformer](https://altair-viz.github.io/user_guide/data_transformers.html) and [renderer](https://altair-viz.github.io/user_guide/custom_renderers.html) frameworks to intercept requests to render the Vega-Lite specs produced by Altair and performs the following:

1. Inline pandas DataFrames are extracted and converted into Arrow tables
2. The Vega-Lite spec is compiled to Vega using [vl-convert](https://github.com/vega/vl-convert)
3. The Arrow tables from (1) and the Vega spec from (2) are fed into the VegaFusion runtime. The runtime evaluates transforms and identifies the subset of columns that are actually required by the visualization. The resulting data is inlined back into the Vega spec.
4. The Vega spec resulting from (3) is displayed using a Jupyter [mimetype bundle](https://docs.jupyter.org/en/latest/reference/mimetype.html)

Unlike the widget renderer, the mime renderer works entirely in Python and does not require any custom notebook extensions.  This makes 

## Inline Data Transformer
Unlike the VegaFusion widget renderer, the mime renderer does not require writing Chart DataFrames to files on disk. Instead, these DataFrames are converted to Arrow tables and passed directly to the VegaFusion runtime (bypassing JSON serialization).

This approach is implemented by the `"vegafusion-inline"` data transformer, which is automatically enabled by the `vegafusion.enable_mime()` function.