# Supported Environments
VegaFusion Jupyter can display visualizations is the following contexts

## Classic Notebook
VegaFusion can display charts in version 6 of the [Jupyter Notebook](https://github.com/jupyter/notebook) (Sometimes referred to as the Classic Notebook since it predates JupyterLab).  The Classic Notebook extension containing the VegaFusion Jupyter Widget is included in the `vegafusion-jupyter` Python package, and it is enabled automatically when the package is installed. 

## JupyterLab
VegaFusion can display charts in version 3+ of [JupyterLab](https://github.com/jupyterlab/jupyterlab).  The JupyterLab extension containing the VegaFusion Jupyter Widget is included in the `vegafusion-jupyter` Python package, and it is enabled automatically when the package is installed.

## Voila
VegaFusion can display charts in the [Voila](https://github.com/voila-dashboards/voila) dashboard toolkit. This works with or without the [`enable_nbextensions`](https://voila.readthedocs.io/en/latest/using.html#using-third-party-widgets-with-voila) flag. 

## Dash / Streamlit / Panel
Extensions for Dash, Streamlit, and Panel are not yet supported. See the following roadmap entries:
 - {ref}`roadmap_dash`
 - {ref}`roadmap_streamlit`
 - {ref}`roadmap_panel`
