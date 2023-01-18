# VegaFusion Roadmap
This page contains an assortment of capabilities that we would like to add to VegaFusion over time.  These are not necessarily in chronological or priority order. If you are interested in collaborating on any of these items, please [get in touch!](mailto:jon@vegafusion.io)

## Python Dashboard Environments

The VegaFusion Jupyter Widget was intentionally designed to push as much logic as possible into the `vegafusion-wasm` package.  The logic that is left in the Jupyter Widget extension is primarily related to client-server communication, and html layout.  With this approach, it shouldn't require a substantial amount of additional code in order to support alternative dashboard environments. 

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

### Provide Selection Access from Python
The current state of Altair [selections](https://altair-viz.github.io/user_guide/interactions.html#selections-building-blocks-of-interactions) could be made available through the `VegaFusionWidget`.  This would make it possible to register custom Python logic to run in response to user interaction events. It would also make it possible to synchronize selections across Charts displayed in different notebook output cells.

## Serverside Rendering
The initial focus of VegaFusion is to accelerate data processing operations by running them on a server with efficient parallelization rather than in a single-threaded browser context. This can provide significant benefit for chart specifications that make use of aggregation to reduce the size of a dataset before transferring it to the client for rendering by the Vega JavaScript library.  A histogram is the canonical example of this kind of visualization, where the binning and aggregation are performed on the server and only the bin edges and heights of the bars are transferred from the server to the client. 

This approach is not particularly helpful for charts that include a large number of mark instances. A scatter plot is the canonical example of this kind of visualization, where currently the entire dataset must be transferred to the client for rendering with the Vega JavaScript library.

To improve the performance of scatter-plot style charts, we could extend the VegaFusion runtime to include support for rendering a subset of the Vega [marks](https://vega.github.io/vega/docs/marks/).  One approach to investigate is the possibility of using the VegaFusion Planner to replace a large mark (e.g. a [symbol](https://vega.github.io/vega/docs/marks/symbol/) mark with 10 million points) with an [image](https://vega.github.io/vega/docs/marks/image/) mark. Then the VegaFusion runtime would render the symbol mark to a PNG image, and send the image (rather than the full dataset) to the client.

## Standalone gRPC Server
The VegaFusion Runtime is currently embedded in Python in the `vegafusion-python` package. As an alternative, the Runtime could operate as a standalone [gRPC](https://grpc.io/) server.  The Runtime interface is already defined in terms of protocol buffer messages, so very little refactoring will be required to accomplish this.

The advantage of using this server architecture is that multiple clients will be able to share the same runtime. This can substantially reduce memory usage if the same dashboard is being served to many individual users.  It also opens up the possibility for the server to run on a separate machine.

A prototype of this approach has been developed as [`vegafusion-server`](https://github.com/hex-inc/vegafusion/tree/main/vegafusion-server), but it hasn't been fully proved out with a specific use case.

## JavaScript API / Business Intelligence Architecture
The VegaFusion client logic is currently compiled to WebAssembly and embedded in a Jupyter Widget extension.  Once the VegaFusion Runtime is available as a standalone gRPC server, it will be possible to embed the VegaFusion WebAssembly client library into custom web applications.  The client library would then communicate with a VegaFusion Runtime using [gRPC-Web](https://github.com/grpc/grpc-web).

A motivating use-case for this architecture is a web-based Business Intelligence tool that generates Vega/Vega-Lite specifications.  Such a tool could operate entirely in the browser for small to medium sized datasets, and then use VegaFusion to provide optional server-side acceleration for large datasets.  Thanks to the server architecture described above, a single gRPC server could support many simultaneous user sessions.

Here's what this architecture might look like

<img width="895" alt="Screen Shot 2022-01-19 at 3 57 32 PM" src="https://user-images.githubusercontent.com/15064365/150212638-5a4d6e74-926b-4426-8310-4ebbb9244b0c.png"> 

## Elastic Scaling and High Availability

When the anticipated user load surpasses the capabilities of a single server, a pool of VegaFusion gRPC servers could run behind a load-balancer.  Thanks to VegaFusion's state model and the gRPC architecture, it would be possible to freely move a user session between servers without losing the user's session state.  This architectural feature is the key to providing reliable implementations of elastic scaling (adjusting the server pool size based on the current user load) and High Availability (recovering from the failure of a single server without disrupting active user sessions).

(roadmap_external_data_providers)=
## External Data Providers
Support will eventually be added to the Runtime for compiling Vega transforms into SQL for evaluation in external data providers like PostgreSQL, OmniSci, Spark, and Dask (through [DaskSQL](https://dask-sql.readthedocs.io/en/latest/)).

## Edge Runtime
A subset of the Runtime (in particular the cache) could be compiled to [WASI](https://wasi.dev/) and run on edge services like Fastly's [compute@edge](https://www.fastly.com/products/edge-compute/serverless) or Cloudflare's [Cloudfare workers](https://workers.cloudflare.com/).  A user session would connect directly to an edge Runtime. The edge runtime would perform cheap computations itself to minimize latency and delegate expensive computations to a server Runtime running on a powerful VM from a traditional cloud provider. The edge Runtime would use the regular VegaFusion caching mechanism to cache the results of calculations performed by the server, and share that cache across all user sessions sharing that edge node.

Here's what an architecture the combines the Edge Runtime and External Data Providers might look like

<img width="584" alt="Screen Shot 2022-01-19 at 4 00 03 PM" src="https://user-images.githubusercontent.com/15064365/150212960-2da194db-05e7-4d38-96cc-69c293689f44.png">
