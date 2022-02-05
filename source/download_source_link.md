(download_source_link)=
# Download Source Link

VegaFusion is released under the [AGPLv3](https://www.gnu.org/licenses/agpl-3.0.en.html) license.  A requirement of this license is that the source code (and build instructions) of an application using VegaFusion must be made available to users who interact the application over a network.

If you're only using VegaFusion in a Jupyter Notebook to look at plots and save them as images, the AGPLv3 license does not impose any additional requirements.  The source code requirement would only be triggered if you use VegaFusion in a dashboard setting like Voila. In this case, the source code of the dashboard must be made available to any users who has the ability to view it.

To make it as easy as possible to comply with the terms of the license, the VegaFusion drop-down menu can be configured with a link to the dashboard's source code (e.g. a public GitHub repository). This link can be provided as the `download_source_link` keyword argument to the `VegaFusionWidget` (or as a keyword argument to the `vf.enable` function).

If no such link is provided (the default), then the dropdowm menu will display a message informing the user of their right to download the application's source code.  

```python
import vegafusion as vf
import altair as alt
from vega_datasets import data

source = data.movies.url

chart = alt.Chart(source).mark_bar().encode(
    alt.X("IMDB_Rating:Q", bin=True),
    y='count()',
)
vf.jupyter.VegaFusionWidget(chart)
```
<img width="529" alt="Dropdown menu with requirement message" src="https://user-images.githubusercontent.com/15064365/148812890-d2a51d88-8f79-47d9-800c-9d456ae56eb1.png">

When the link is provided, a `Download Source` entry is added to the menu that will navigate to the link location.

```python
import vegafusion as vf
import altair as alt
from vega_datasets import data

source = data.movies.url

chart = alt.Chart(source).mark_bar().encode(
    alt.X("IMDB_Rating:Q", bin=True),
    y='count()',
)
vf.jupyter.VegaFusionWidget(
    chart,
    download_source_link="https://github.com/vegafusion/vegafusion.github.io"
)
```

<img width="517" alt="Dropdown menu with Download Source link" src="https://user-images.githubusercontent.com/15064365/148812910-cfe3379b-3963-4b6e-aa0f-24c73a80d9b1.png">
