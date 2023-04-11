# Saving Charts
VegaFusion 1.2 introduced a collection of functions to save Altair charts to files after pre-evaluating their data transformations and removing unused columns. For charts that reference large datasets, this results in faster save times and, in the case of HTML and JSON files, smaller file sizes. 

## Standard Altair save
Altair Chart objects provide a [`Chart.save()`](https://altair-viz.github.io/user_guide/saving_charts.html) method that may be used to save Altair charts to HTML, JSON (as Vega-Lite), or static image (PNG or SVG) files. When the chart references a pandas DataFrame, the full DataFrame is serialized to JSON and included in the chart specification that is saved.  As dataset sizes get larger, the time it takes to save these files increases rapidly, and for the case of HTML and JSON formats, the file size increases rapidly as well.

VegaFusion's save functions improve the situation by pre-applying data transformations and removing unused columns before inlining the resulting data in the chart specification for saving.

## HTML performance comparison
Here are two examples of the benefits of the VegaFusion `save_html` function compared to the standard Altair `Chart.save` method. 

### With aggregations
Consider the case of saving a one million row histogram to an HTML file. First create and display the histogram with the VegaFusion [Mime Renderer](./mime_renderer.md) enabled.

```
import pandas as pd
import altair as alt
import vegafusion as vf
vf.enable()

flights = pd.read_parquet(
    "https://vegafusion-datasets.s3.amazonaws.com/vega/flights_1m.parquet"
)

delay_hist = alt.Chart(flights).mark_bar().encode(
    alt.X("delay", bin=alt.Bin(maxbins=30)),
    alt.Y("count()")
)
delay_hist
```

![histogram](https://user-images.githubusercontent.com/15064365/230728055-64b05777-9925-4711-b7c4-3e4cc52e1c83.png)

Next, save the chart to an HTML file with the standard Altair `Chart.save` method.

```python
%%time
delay_hist.save("delay_hist_standard.html")
```
```
CPU times: user 5.72 s, sys: 388 ms, total: 6.11 s
Wall time: 6.18 s
```

This results in a ~116MB file, as all columns from the entire million row dataset are included in the HTML file. It also takes over 6 seconds to perform the save. Now, use VegaFusion's `save_html` function.

```python
%%time
vf.save_html(delay_hist, "delay_hist_vf.html")
```
```
CPU times: user 227 ms, sys: 119 ms, total: 347 ms
Wall time: 427 ms
```
The resulting file is now only ~5KB, because only ~30 rows have been included (one per histogram bin). It also takes under half a second to perform the save.

### Without aggregations
The benefits of VegaFusion's save functions are most dramatic for charts that use aggregations. Even so, VegaFusion's ability to remove unused columns still results in smaller file sizes for unaggregated charts, especially when the input datasets have many unused columns. 

Here's an example scatter chart using the Movies dataset, which has 3201 rows and 16 columns.

```python
import vegafusion as vf
import altair as alt
from vega_datasets import data

source = data.movies()

scatter_chart = alt.Chart(source).mark_point().encode(
    alt.X("IMDB_Rating:Q"),
    alt.Y("Rotten_Tomatoes_Rating:Q"),
)
scatter_chart
```
![movies scatter chart](https://user-images.githubusercontent.com/15064365/230728307-6d8a2c6c-e45e-483b-a207-3abf0c26449b.png)

Save the chart to an HTML file with Altair's standard `Chart.save` method.

```python
%%time
scatter_chart.save("scatter_standard.html")
```
```
CPU times: user 69.7 ms, sys: 14.7 ms, total: 84.4 ms
Wall time: 85 ms
```
This results in a 1.4MB file and takes ~80ms.

Now, save the file with VegaFusion's `save_html` function:

```python
%%time
vf.save_html(scatter_chart, "scatter_vf.html")
```
```
CPU times: user 59.8 ms, sys: 15.2 ms, total: 75 ms
Wall time: 57.1 ms
```

This results in a 125K file and takes under 60ms. The file is more than 10x smaller because it only includes data for the two columns that are referenced by the scatter plot.

## APIs
### save_html
`save_html(chart, file, embed_options, inline, full_html)`

    Save an Altair Chart to an HTML file after pre-applying data transformations 
    and removing unused columns:

    :param chart: alt.Chart
        The Altair chart to save
    :param file: str, pathlib.Path, or file-like object
        The file path to write the HTML file to, or a file-like object to write to
    :param embed_options: dict (default None)
        Dictionary of options to pass to vega-embed
    :param inline: boolean (default False)
        If False (default), the required JavaScript libraries are loaded from a
        CDN location. This results in a smaller file, but an internet connection
        is required to view the resulting HTML file.

        If True, all required JavaScript libraries are inlined.
        This results in a larger file, but no internet connection is required to view.
        inline=True requires Altair 5 and the altair_viewer package
    :param full_html: boolean (default True)
        If True, then a full html page is written. If False, then
        an HTML snippet that can be embedded into an HTML page is written.

### save_vega
`save_vega(chart, file, pretty=)`

    Save an Altair Chart to a Vega JSON file after pre-applying data transformations
    and removing unused columns

    :param chart: alt.Chart
        The Altair chart to save
    :param file: str, pathlib.Path, or file-like object
        The file path to write the Vega JSON file to, or a file-like object to write to
    :param pretty: boolean (default True)
        If True, pretty-print the resulting JSON file. If False, write the smallest file possible

### save_png
`save_png(chart, file, scale)`

    Save an Altair Chart to a static PNG image file after pre-applying data transformations
    and removing unused columns

    :param chart: alt.Chart
        The Altair chart to save
    :param file: str, pathlib.Path, or file-like object
        The file path to write the PNG file to, or a file-like object to write to
    :param scale: float (default 1)
        Image scale factor

### save_svg
`save_svg(chart, file)`

    Save an Altair Chart to a static SVG image file after pre-applying data transformations
    and removing unused columns

    :param chart: alt.Chart
        The Altair chart to save
    :param file: str, pathlib.Path, or file-like object
        The file path to write the SVG file to, or a file-like object to write to
