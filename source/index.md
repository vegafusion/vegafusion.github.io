# VegaFusion

VegaFusion provides serverside acceleration for the [Vega](https://vega.github.io/) visualization grammar. While not limited to Python, an initial application of VegaFusion is the acceleration of the [Altair](https://altair-viz.github.io/) Python interface to [Vega-Lite](https://vega.github.io/vega-lite/).

The core VegaFusion algorithms are implemented in Rust. Python integration is provided using [PyO3](https://pyo3.rs/v0.15.1/) and JavaScript integration is provided using [wasm-bindgen](https://github.com/rustwasm/wasm-bindgen). 

**For more info on the future direction of the project, see the [Roadmap](./roadmap) and [Licensing and Funding](./license_overview) pages.**

```{toctree}
:maxdepth: 2
:hidden: true
:caption: "User Guide"
installation
supported_environments
widget
renderer
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
```

```{toctree}
:maxdepth: 1
:hidden: true
:caption: "Future"
license_overview
roadmap
```

```{toctree}
:maxdepth: 1
:hidden: true
:caption: "Community"
Source Code <https://github.com/vegafusion/vegafusion/>
Report an Issue <https://github.com/vegafusion/vegafusion/issues>
Start a Discussion <https://github.com/vegafusion/vegafusion/discussions>
```

```{toctree}
:maxdepth: 1
:hidden: true
:caption: "Blog"
blog
```



## Quickstart: Accelerate Altair in Jupyter
VegaFusion can be used to provide serverside acceleration for Altair visualizations when displayed in Jupyter contexts (Classic notebook, JupyterLab, and Voila). First, install the `vegafusion-jupyter` package, along with `vega-datasets` for the example below.

```bash
$ pip install "vegafusion-jupyter[embed]" vega-datasets
```

Then, open a jupyter notebook (either the classic notebook, or a notebook inside JupyterLab), and run these two lines to import and enable the VegaFusion Altair renderer.

```python
import vegafusion as vf
vf.jupyter.enable()
```
VegaFusion will now be used to accelerate any Altair chart. For example, here's the [interactive average](https://altair-viz.github.io/gallery/selection_layer_bar_month.html) Altair gallery example.

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

chart = alt.layer(bars, line, data=source)
chart
```

<video width="600" controls>
  <source src="https://user-images.githubusercontent.com/15064365/148408648-43a5cfd0-b0d8-456e-a77a-dd344d8d07df.mov" type="video/mp4">
This browser does not support the video tag.
</video>


Histogram binning, aggregation, selection filtering, and average calculations will now be evaluated in the Python kernel process with efficient parallelization, rather than in the single-threaded browser context.

You can see that VegaFusion acceleration is working by noticing that the Python [kernel is running](https://experienceleague.adobe.com/docs/experience-platform/data-science-workspace/jupyterlab/overview.html?lang=en#kernel-sessions) as the selection region is created or moved. You can also notice the VegaFusion logo in the dropdown menu button.

## Recent Posts

```{postlist} 10
:date: "%Y-%m-%d"
:format: "{date} - {title}"
```
