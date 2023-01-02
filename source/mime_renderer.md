# Mime Renderer

The VegaFusion mime renderer makes it possible to display Altair charts that reference large datasets in a wide variety of Python notebook and compute environments.  

**Note:** While the mime renderer is compatible with both static and interactive charts, the [widget renderer](./widget.md) is better suited for interactive charts that reference large datasets.

## Installation
The mime renderer is included in the `vegafusion` Python package:

```bash
pip install "vegafusion[embed]"
```

## Activation
The VegaFusion mime renderer is enabled using the `vegafusion.enable()` function. For example:

```python
import vegafusion as vf
vf.enable()
...
chart
```

The mime renderer can also be enabled temporarily by using `vegafusion.enable()` as a context manager:

```python
import vegafusion as vf
from IPython.display import display
with vf.enable():
    ...
    display(chart)
```

When enabled, Altair charts will be automatically processed by VegaFusion when they are displayed. Here is an example of a 1 million row histogram that could not be displayed without a VegaFusion renderer:

```python
import pandas as pd
import altair as alt
import vegafusion as vf

vf.enable()
flights = pd.read_parquet(
    "https://vegafusion-datasets.s3.amazonaws.com/vega/flights_1m.parquet"
)

alt.Chart(flights).mark_bar().encode(
    alt.X("delay", bin=alt.Bin(maxbins=30)),
    alt.Y("count()")
)
```
![Flight Delay Histogram](https://user-images.githubusercontent.com/15064365/209973961-948b9d10-4202-4547-bbc8-d1981dcc8c4e.png)

## Row Limit
Charts of large datasets that do not perform any form of aggregation (e.g. Scatter Plots) can still result in very large chart specification that risk crashing the web browser they are displayed in. To protect against this, the VegaFusion mime renderer supports an optional `row_limit` argument to the `enable()` function.  Unlike the default Altair row limit, this row limit is enforced _after_ all supported data transformations have been applied. For example, in the case of a histogram there will be one row per histogram bin after transforms are applied. 

The default `row_limit` is 10,000, but it can be customized like this:

```python
import vegafusion as vf
vf.enable(row_limit=50000)
```

The row limit check can be disabled by setting the `row_limit` argument to `None` as follows:

```python
import vegafusion as vf
vf.enable(row_limit=None)
```

## Supported mimetypes
The mime renderer can display the resulting Vega spec using a variety of mimetypes

### `html` (default)
When the `mimetype` argument is set to `"html"` (the default), the resulting mime bundle will have type `"text/html"` and will contain an HTML snippet that loads several JavaScript dependencies from a CDN location and displays the Vega spec using [`vega-embed`](https://github.com/vega/vega-embed). This renderer is compatible with the classic Jupyter Notebook, JupyterLab, Visual Studio Code, Colab, Hex, Kaggle, and others.

**Note:** The `html` mimetype requires an active internet connection.

### `vega` 
When the `mimetype` argument to `vf.enable()` is set to `"vega"`, the resulting mime bundle will have type `"application/vnd.vega.v5+json"` and will contain the Vega spec. This approach works in JupyterLab, Visual Studio Code, Hex, and other compute environments that include built-in support for rendering Vega charts. No internet connection is required, but note that this mimetype is not supported by the classic Jupyter Notebook.

### `svg`
When the `mimetype` argument is set to `"svg"`, the resulting mime bundle will have type `"image/svg+xml"` and will contain a static SVG image of the chart.

### `png`
When the `mimetype` argument is set to `"png"`, the resulting mime bundle will have type `"image/png"` and will contain a static PNG image of the chart.

## Local timezone
The behavior of certain Vega/Vega-Lite transforms and expression functions depends on the local timezone of the chart. The [Time Unit](https://vega.github.io/vega-lite/docs/timeunit.html) transform is one such example. When transforms are evaluated in the Vega JavaScript library, the chart's local timezone is set to the local timezone of the web browser.

When the VegaFusion mime renderer evaluates Vega transforms in the Python kernel, it does not have access to the browser's local timezone.  Instead, it uses the local timezone of the Python kernel (as determined by VlConvert's `vl_convert.get_local_tz()` function).  When the Python kernel and web browser are running on the same machine (as is the case when running Jupyter locally), the charts produced by the VegaFusion mime renderer will look identical to those processed by Vega entirely in the web browser.   However, if Jupyter is running on a remote VM (as is the case when using Colab or Binder) then the kernel's local timezone may not match the browser's local timezone.

In this case, it's possible to override VegaFusion's local timezone using the `vegafusion.set_local_tz()` function. For example:

```python
import vegafusion as vf
vf.set_local_tz("America/New_York")
```

**Note:** The `set_local_tz` configuration affects only the mime renderer. The VegaFusion widget renderer maintains a two-way connection between the Python kernel and the browser, so it is able to use the browser's local timezone directly.

## How it works
The mime renderer plugs into Altair's [data transformer](https://altair-viz.github.io/user_guide/data_transformers.html) and [renderer](https://altair-viz.github.io/user_guide/custom_renderers.html) frameworks to intercept requests to render the Vega-Lite specs produced by Altair and performs the following:

1. Inline pandas DataFrames are extracted and converted into Arrow tables
2. The Vega-Lite spec is compiled to Vega using [VlConvert](https://github.com/vega/vl-convert)
3. The Arrow tables from (1) and the Vega spec from (2) are fed into the VegaFusion runtime. The runtime evaluates transforms and identifies the subset of columns that are actually required by the visualization. The resulting data is inlined back into the Vega spec.
4. The Vega spec resulting from (3) is displayed using a Jupyter [mimetype bundle](https://docs.jupyter.org/en/latest/reference/mimetype.html)

Unlike the widget renderer, the mime renderer works entirely in Python and does not require any custom notebook extensions. 

## Inline Data Transformer
Unlike the VegaFusion widget renderer, the mime renderer does not require writing Chart DataFrames to files on disk. Instead, these DataFrames are converted to Arrow tables and passed directly to the VegaFusion runtime (bypassing JSON serialization).

This approach is implemented by the `"vegafusion-inline"` data transformer, which is automatically enabled by the `vegafusion.enable()` function.