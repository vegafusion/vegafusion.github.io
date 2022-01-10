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

