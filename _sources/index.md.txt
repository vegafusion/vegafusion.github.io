# VegaFusion

VegaFusion provides serverside scaling for the [Vega](https://vega.github.io/) visualization library. While not limited to Python, an initial application of VegaFusion is the scaling of the [Altair](https://altair-viz.github.io/) Python interface to [Vega-Lite](https://vega.github.io/vega-lite/).

As of version 1.0, VegaFusion is released under the same license as Vega, Vega-Lite, and Altair: [BSD-3](https://opensource.org/licenses/BSD-3-Clause).

**For more info on the future direction of the project, see the [Roadmap](./roadmap).**

```{toctree}
:maxdepth: 2
:hidden: true
:caption: "User Guide"
installation
supported_environments
mime_renderer
widget_renderer
widget
transformed_data
low_level
```

```{toctree}
:maxdepth: 1
:hidden: true
:caption: "Gallery"
example_gallery
```

```{toctree}
:maxdepth: 1
:hidden: true
:caption: "About"
background
how_it_works
architecture
technology
about_the_name
related_projects
license_overview
citation
```

```{toctree}
:maxdepth: 1
:hidden: true
:caption: "Future"
roadmap
```

```{toctree}
:maxdepth: 1
:hidden: true
:caption: "Community"
Source Code <https://github.com/hex-inc/vegafusion/>
Report an Issue <https://github.com/hex-inc/vegafusion/issues>
Start a Discussion <https://github.com/hex-inc/vegafusion/discussions>
```

```{toctree}
:maxdepth: 1
:hidden: true
:caption: "Blog"
blog
```

## Quickstart 1: Overcome `MaxRowsError` with VegaFusion
The VegaFusion mime renderer can be used to overcome the Altair [`MaxRowsError`](https://altair-viz.github.io/user_guide/faq.html#maxrowserror-how-can-i-plot-large-datasets) by performing data-intensive aggregations on the server and pruning unused columns from the source dataset.  First install the `vegafusion` Python package with the `embed` extras enabled

```bash
pip install "vegafusion[embed]"
```

Then open a Jupyter notebook (either the classic notebook or a notebook inside JupyterLab), and create an Altair histogram of a 1 million row flights dataset

```python
import pandas as pd
import altair as alt

flights = pd.read_parquet(
    "https://vegafusion-datasets.s3.amazonaws.com/vega/flights_1m.parquet"
)

delay_hist = alt.Chart(flights).mark_bar().encode(
    alt.X("delay", bin=alt.Bin(maxbins=30)),
    alt.Y("count()")
)
delay_hist
```
```
---------------------------------------------------------------------------
MaxRowsError                              Traceback (most recent call last)
...
MaxRowsError: The number of rows in your dataset is greater than the maximum allowed (5000). For information on how to plot larger datasets in Altair, see the documentation
```

This results in an Altair `MaxRowsError`, as by default Altair is configured to allow no more than 5,000 rows of data to be sent to the browser.  This is a safety measure to avoid crashing the user's browser.  The VegaFusion mime renderer can be used to overcome this limitation by performing data intensive transforms (e.g. filtering, binning, aggregation, etc.) in the Python kernel before the resulting data is sent to the web browser.

Run these two lines to import and enable the VegaFusion mime renderer

```python
import vegafusion as vf
vf.enable()
```

Now the chart displays quickly without errors 
```
delay_hist
```
![Flight Delay Histogram](https://user-images.githubusercontent.com/15064365/209973961-948b9d10-4202-4547-bbc8-d1981dcc8c4e.png)

## Quickstart 2: Extract transformed data
By default, data transforms in an Altair chart (e.g. filtering, binning, aggregation, etc.) are performed by the Vega JavaScript library running in the browser. This has the advantage of making the charts produced by Altair fully standalone, not requiring access to a running Python kernel to render properly. But it has the disadvantage of making it difficult to access the transformed data (e.g. the histogram bin edges and count values) from Python.  Since VegaFusion evaluates these transforms in the Python kernel, it's possible to access then from Python using the `vegafusion.transformed_data()` function.

For example, the following code demonstrates how to access the histogram bin edges and counts for the example above:

```python
import pandas as pd
import altair as alt
import vegafusion as vf

flights = pd.read_parquet(
    "https://vegafusion-datasets.s3.amazonaws.com/vega/flights_1m.parquet"
)

delay_hist = alt.Chart(flights).mark_bar().encode(
    alt.X("delay", bin=alt.Bin(maxbins=30)),
    alt.Y("count()")
)
vf.transformed_data(delay_hist)
```
|    |   bin_maxbins_30_delay |   bin_maxbins_30_delay_end |   __count |
|---:|-----------------------:|---------------------------:|----------:|
|  0 |                    -20 |                          0 |    419400 |
|  1 |                     80 |                        100 |     11000 |
|  2 |                      0 |                         20 |    392700 |
|  3 |                     40 |                         60 |     38400 |
|  4 |                     60 |                         80 |     21800 |
|  5 |                     20 |                         40 |     92700 |
|  6 |                    100 |                        120 |      5300 |
|  7 |                    -40 |                        -20 |      9900 |
|  8 |                    120 |                        140 |      3300 |
|  9 |                    140 |                        160 |      2000 |
| 10 |                    160 |                        180 |      1800 |
| 11 |                    320 |                        340 |       100 |
| 12 |                    180 |                        200 |       900 |
| 13 |                    240 |                        260 |       100 |
| 14 |                    -60 |                        -40 |       100 |
| 15 |                    260 |                        280 |       100 |
| 16 |                    200 |                        220 |       300 |
| 17 |                    360 |                        380 |       100 |

## Quickstart 3: Accelerate interactive charts
While the VegaFusion mime renderer works great for non-interactive Altair charts, it's not as well suited for [interactive](https://altair-viz.github.io/user_guide/interactions.html) charts visualizing large datasets. This is because the mime renderer does not maintain a live connection between the browser and the python kernel, so all the data that participates in an interaction must be sent to the browser.

To address this situation, VegaFusion provides a [Jupyter Widget](https://ipywidgets.readthedocs.io/en/stable/) based renderer that does maintain a live connection between the chart in the browser and the Python kernel. In this configuration, selection operations (e.g. filtering to the extents of a brush selection) can be evaluated interactively in the Python kernel, which eliminates the need to transfer the full dataset to the client in order to maintain interactivity.

The VegaFusion widget renderer is provided by the `vegafusion-jupyter` package.

```bash
pip install "vegafusion-jupyter[embed]"
```

Instead of enabling the mime render with `vf.enable()`, the widget renderer is enabled with `vf.enable_widget()`.  Here is a full example that uses the widget renderer to display an interactive Altair chart that implements linked histogram brushing for a 1 million row flights dataset.

```python
import pandas as pd
import altair as alt
import vegafusion as vf

vf.enable_widget()

flights = pd.read_parquet(
    "https://vegafusion-datasets.s3.amazonaws.com/vega/flights_1m.parquet"
)

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

Histogram binning, aggregation, and selection filtering are now evaluated in the Python kernel process with efficient parallelization, and only the aggregated data (one row per histogram bar) is sent to the browser.

You can see that the VegaFusion widget renderer maintains a live connection to the Python kernel by noticing that the Python [kernel is running](https://experienceleague.adobe.com/docs/experience-platform/data-science-workspace/jupyterlab/overview.html?lang=en#kernel-sessions) as the selection region is created or moved. You can also notice the VegaFusion logo in the dropdown menu button.

## Stewardship
The VegaFusion project was created by [Jon Mease](https://jonmmease.dev/) and is now stewarded by [Hex Technologies](https://hex.tech/), which uses VegaFusion in production to accelerate its Vega-Lite powered chart editor.  Hex is committed to supporting VegaFusion's ongoing development and is excited to collaborate with the community to make VegaFusion useful throughout the Vega ecosystem.

```{image} https://user-images.githubusercontent.com/15064365/213193272-b9617431-84a0-4733-8b58-1309d25e925b.svg
:alt: Hex Logo
:width: 200px
:align: center
:target: https://hex.tech
```

## Recent Posts

```{postlist} 10
:date: "%Y-%m-%d"
:format: "{date} - {title}"
```
