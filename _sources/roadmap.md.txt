# VegaFusion Roadmap

## Packaging

(roadmap_conda_forge_packages)=
### conda-forge packages
The `vegafusion-python` and `vegafusion-jupyter` packages could be submitted to conda-forge.  `vegafusion-python` is written in Rust and must be compiled to each supported operating systema and Python version individually.  `vegafusion-jupyter` will be a `noarch` package that depends on `vegafusion-jupyter`.

(roadmap_widget_npm_packages)=
### NPM packages
The `vegafusion-wasm` and `vegafusion-jupyter` packages could be published as npm packages.  This will enable compatibility with Voila without the [`enable_nbextensions`](https://voila.readthedocs.io/en/latest/using.html#using-third-party-widgets-with-voila) flag.  It should also enable compatibility with Google Colab and other non-Jupyter environments that provide support for Jupyter Widgets.

## Environments

The VegaFusion Jupyter Widget was intentionally designed to push as much logic as possible into the `vegafusion-wasm` package.  The logic that is left in the Jupyter Widget extension is primarily related to client-server communication, and html layout.  With this approach, it shouldn't require a substantial amount of addition code in order to support alternative dashboard environments. 

(roadmap_dash)=
### Dash support
A Dash component for VegaFusion could be written.\
See [dash.plotly.com/plugins](https://dash.plotly.com/plugins).

(roadmap_streamlit)=
### Streamlit support
A Streamlit component for VegaFusion could be written.\
See [docs.streamlit.io/library/components/create](https://docs.streamlit.io/library/components/create).

(roadmap_panel)=
### Panel support
A Panel component for VegaFusion could be written.\
See [panel.holoviz.org/user_guide/Custom_Components.html](https://panel.holoviz.org/user_guide/Custom_Components.html)

## Demos
(roadmap_voila_gallery)=
### Create Hosted gallery examples with Voila
Gallery examples could be written as Voila dashboards and hosted using Binder or Heroku

## Altair Integration

(roadmap_extract_data)=
### Extracting Data from Altair Chart
The [Extracting Data](https://github.com/altair-viz/altair-transform#example-extracting-data) workflow supported by `altair-transform` could be implemented. This would involve directly converting Altair transforms into Vega transforms without using Vega-Lite in the browser. The transforms are nearly identical, so this shouldn't present a major challenge.

(roadmap_pre_agg)=
### Pre-Aggregating Large Datasets in Altair Chart
The [Pre-Aggregating Large Datasets](https://github.com/altair-viz/altair-transform#example-pre-aggregating-large-datasets) workflow from `altair-transform` could be implemented. As above, this would involve directly converting Altair transforms into Vega transforms without using Vega-Lite in the browser.

(roadmap_external_data_providers)=
## External Data Providers
Specialized runtimes could be written for particular data providers like PostgreSQL, OmniSci, Spark, and Dask.  These runtimes could support a small subset of transforms and expression language functions and allow the Planner to determine what work to assign to the runtime.