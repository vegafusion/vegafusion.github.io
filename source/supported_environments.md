# Supported Environments
VegaFusion can display Altair visualizations is the following contexts

## Classic Notebook
Both the VegaFusion mime and widget renderers are compatible with version 6 of the [Jupyter Notebook](https://github.com/jupyter/notebook) (Sometimes referred to as the Classic Notebook since it predates JupyterLab). The Classic Notebook extension containing the VegaFusion widget is included in the `vegafusion-jupyter` Python package, and it is enabled automatically when the package is installed.

## JupyterLab
Both the VegaFusion mime and widget renderers are compatible with version 3+ of [JupyterLab](https://github.com/jupyterlab/jupyterlab).  The JupyterLab extension containing the VegaFusion widget is included in the `vegafusion-jupyter` Python package, and it is enabled automatically when the package is installed.

## Voila
Both the VegaFusion mime and widget renderers are compatible with the [Voila](https://github.com/voila-dashboards/voila) dashboard toolkit. This works with or without the [`enable_nbextensions`](https://voila.readthedocs.io/en/latest/using.html#using-third-party-widgets-with-voila) flag. 

## Visual Studio Code
Both the VegaFusion mime and widget renderers are compatible with Visual Studio Code [Python notebooks](https://code.visualstudio.com/docs/datascience/jupyter-notebooks). The widget extension will be downloaded automatically from a CDN location, so an active internet connection is required to use the widget renderer.

## Hex
The VegaFusion mime renderer is compatible with the [Hex notebook](https://hex.tech/). VegaFusion comes pre-installed and the mime renderer can be enabled as usual.

```python
import vegafusion as vf
vf.enable()
...
```

The widget renderer is not compatible with Hex.

## Colab
The VegaFusion mime renderer is compatible with [Google Colab](https://colab.research.google.com/):

```
%pip install vegafusion[embed]
```
```python
import vegafusion as vf
vf.enable()
...
```

The VegaFusion widget renderer is also compatible with [Google Colab](https://colab.research.google.com/) when the custom widget manager is enabled:

```
%pip install vegafusion-jupyter[embed]
```
```python
from google.colab import output
output.enable_custom_widget_manager()

import vegafusion as vf
vf.enable_widget()
...
```

## Kaggle
The VegaFusion mime renderer is compatible with [Kaggle Notebooks](https://www.kaggle.com/docs/notebooks):

```
%pip install vegafusion[embed]
```
```python
import vegafusion as vf
vf.enable()
...
```

The widget renderer is not currently compatible with Kaggle.

## Dash / Streamlit / Panel
Extensions for Dash, Streamlit, and Panel are not yet supported. See the following roadmap entries:
 - {ref}`roadmap_dash`
 - {ref}`roadmap_streamlit`
 - {ref}`roadmap_panel`
