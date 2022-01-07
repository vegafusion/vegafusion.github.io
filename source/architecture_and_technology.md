# Architecture and Technologies
## VegaFusion Architecture
The Planner runs entirely in the browser.  The responsibilities of the Runtime are split between the client and the server.  The client portion of the runtime is responsible for compiling the server specification into an efficient task graph representation.  As the root values of the task graph change (typically in response to user interaction events), the client runtime traverses the graph and compares the nodes in the traversal with the communication plan to determine which node values to request from the server.

The client runtime serializes the task graph and the query node ids and sends them as a request to the server runtime.  The server runtime receives the request, and checks whether the requested nodes are already available in its cache. If not it recursively traverses the ancestors of the query nodes until it finds a node value that is in the cache, or an inline root value of the Task Graph specification. It then traverses back down the task graph, evaluating the task functions as it goes. These newly computed task values are stored in the cache, and finally the requested node values are sent to the client.

### Architecture Advantages
This architecture is more complex than what would be required for only the Jupyter Widget scenario.  A characteristic of Jupyter Widgets is that there is a one-to-one correspondence between the widget state stored in the browser and the state stored on the server. So it would be fine for the task graph specification and the task graph values to be one data structure that is mirrored between the client and server.

This was actually the initial design. But it was soon apparent that this approach would not scale well to support future client server scenarios where one server process needs to support many clients. For example, when VegaFusion eventually supports Dash and custom client server configurations.  In these scenarios, it's not desirable for the server to maintain the full state of every visualization for every user.  This is especially wasteful when many users are viewing nearly identical visualizations.

With the VegaFusion runtime architecture, the server memory usage is independent of the number of simultaneous clients.  Each client request contains the full specification of the task graph, so the server doesn't need to remember the exact previous state of a client.  At the same time, it would be very inefficient if the server always had to compute every value in the full task graph on each request.  This inefficiency is addressed with precise caching.  The caching is "precise" in that each node of the task graph has a cache key that is generated from both its internal specification and that of all of its parents.  This means that common subgraphs across requests will have a shared cache entry even if the downstream tasks are different.

Another advantage of the approach is that a single client can freely change its task graph without having to notify the server runtime.  For example, a Vega editor backed by VegaFusion could send a slightly different task graph to the server as the spec is modified, but the cache will remain valid for the portions of the task graph that were not modified.  This effectively provides a hot reload capability.

## VegaFusion technology stack
VegaFusion uses a fairly diverse technology stack. The planner and runtime are both implemented in Rust.

In the context of `vegafusion-jupyter`, both the Planner and the client portion of the Runtime are compiled to WebAssembly using [wasm-pack](https://github.com/rustwasm/wasm-pack) and wrapped in a TypeScript API using [wasm-bindgen](https://github.com/rustwasm/wasm-bindgen).  This TypeScript API is used to integrate the WebAssembly library into the VegaFusion Jupyter Widget.

The server portion of the Runtime is wrapped in a Python API using [PyO3](https://github.com/PyO3/pyo3), resulting in the `vegafusion-python` package.  The `vegafusion-jupyter` package is used to integrate vegafusion-python with Altair and the Python portion of VegaFusion Jupyter Widget.

The Task Graph specifications are defined as protocol buffer messages. The [prost](https://github.com/tokio-rs/prost) library is used to generate Rust data structures from these protocol buffer messages.  When Arrow tables appear as task graph root values, they are serialized inside the protocol buffer specification using the [Apache Arrow IPC format](https://arrow.apache.org/docs/format/Columnar.html#serialization-and-interprocess-communication-ipc).  The binary representation of the task graph protocol buffer message is what is transferred across the Jupyter Comms protocol.

<img width="749" alt="VegaFusion Jupyter Architecture Diagram" src="https://user-images.githubusercontent.com/15064365/148417030-19420ef2-50de-40cf-bd42-c39e1147049c.png">

## DataFusion integration
Apache Arrow DataFusion is an SQL compatible query engine that integrates with the Rust implementation of Apache Arrow.  VegaFusion uses DataFusion to implement many of the Vega transforms, and it compiles the Vega expression language directly into the DataFusion expression language.  In addition to being really fast, a particularly powerful characteristic of DataFusion is that it provides many interfaces that can be extended with your own custom Rust logic.  For example, VegaFusion defines many custom UDFs that are designed to implement the precise semantics of the Vega expression language and the Vega expression functions.
