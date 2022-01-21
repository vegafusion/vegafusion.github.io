# VegaFusion Roadmap
This page contains an assortment of capabilities that we would like to add to VegaFusion over time.  These are not necessarily in chronological or priority order. If you are interested in contributing time and/or funding to help prioritise these items, please [get in touch!](mailto:jon@vegafusion.io)

## Packaging

(roadmap_conda_forge_packages)=
### conda-forge packages
The `vegafusion-python` and `vegafusion-jupyter` packages could be submitted to conda-forge.  `vegafusion-python` is written in Rust and must be compiled to each supported operating systema and Python version individually.  `vegafusion-jupyter` will be a `noarch` package that depends on `vegafusion-jupyter`.

## Non-Jupyter Notebook Environments

### Colab
Colab supports custom JupyterWidgets, so it should be possible to support `vegafusion-jupyter` in Colab. For unknown reasons, it does not work today. See [vegafusion#55](https://github.com/vegafusion/vegafusion/issues/55).

## Python Dashboard Environments

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


## Altair Integration

(roadmap_extract_data)=
### Extracting Data from Altair Chart
The [Extracting Data](https://github.com/altair-viz/altair-transform#example-extracting-data) workflow supported by `altair-transform` could be implemented. This would involve directly converting Altair transforms into Vega transforms without using Vega-Lite in the browser. The transforms are nearly identical, so this shouldn't present a major challenge.

(roadmap_pre_agg)=
### Pre-Aggregating Large Datasets in Altair Chart
The [Pre-Aggregating Large Datasets](https://github.com/altair-viz/altair-transform#example-pre-aggregating-large-datasets) workflow from `altair-transform` could be implemented. As above, this would involve directly converting Altair transforms into Vega transforms without using Vega-Lite in the browser.

### Provide Selection Access from Python
The current state of Altair [selections](https://altair-viz.github.io/user_guide/interactions.html#selections-building-blocks-of-interactions) could be made available through the `VegaFusionWidget`.  This would make it possible to register custom Python logic to run in response to user interaction events. It would also make it possible to synchronize selections across Charts displayed in different notebook output cells.

## Beyond Python
### Standalone gRPC Server
The VegaFusion Runtime is currently embedded in Python in the `vegafusion-python` package. As an alternative, the Runtime could operate as a standalone [gRPC](https://grpc.io/) server.  The Runtime interface is already defined in terms of protocol buffer messages, so very little refactoring will be required to accomplish this.

The advantage of using this server architecture is that multiple clients will be able to share the same runtime. This can substantially reduce memory usage if the same dashboard is being served to many individual users.  It also opens up the possibility for the server to run on a separate machine.

### JavaScript API / Business Intelligence Architecture
The VegaFusion client logic is currently compiled to WebAssembly and embedded in a Jupyter Widget extension.  Once the VegaFusion Runtime is available as a standalone gRPC server, it will be possible to embed the VegaFusion WebAssembly client library into custom web applications.  The client library would then communicate with a VegaFusion Runtime using [gRPC-Web](https://github.com/grpc/grpc-web).

A motivating use-case for this architecture is a web-based Business Intelligence tool that generates Vega/Vega-Lite specifications.  Such a tool could operate entirely in the browser for small to medium sized datasets, and then use VegaFusion to provide optional server-side acceleration for large datasets.  Thanks to the server architecture described above, a single gRPC server could support many simultaneous user sessions.

Here's what this architecture might look like

<img width="895" alt="Screen Shot 2022-01-19 at 3 57 32 PM" src="https://user-images.githubusercontent.com/15064365/150212638-5a4d6e74-926b-4426-8310-4ebbb9244b0c.png"> 

### Elastic Scaling and High Availability

When the anticipated user load surpasses the capabilities of a single server, a pool of VegaFusion gRPC servers could run behind a load-balancer.  Thanks to Vega Fusion's state model and the gRPC architecture, it would be possible to freely move a user session between servers without losing the user's session state.  This architectural feature is the key to providing reliable implementations of elastic scaling (adjusting the server pool size based on the current user load) and High Availability (recovering from the failure of a single server without disrupting active user sessions).

(roadmap_external_data_providers)=
## External Data Providers
Specialized runtimes could be written for particular data providers like PostgreSQL, OmniSci, Spark, and Dask.  These runtimes could support a small subset of transforms and expression language functions and allow the Planner to determine what work to assign to the runtime.

Here's what an architecture with external Data Providers might look like


<img width="584" alt="Screen Shot 2022-01-19 at 4 00 03 PM" src="https://user-images.githubusercontent.com/15064365/150212960-2da194db-05e7-4d38-96cc-69c293689f44.png">
