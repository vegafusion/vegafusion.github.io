# Low Level APIs
The VegaFusion mime and widget renderers are built from lower-level primitives that can be used to integrate VegaFusion in non-Jupyter, and non-Python, contexts. Documentation of these lower-level constructs is not yet complete, so in the meantime please [start a discussion](https://github.com/hex-inc/vegafusion/discussions) if you're interested in integrating VegaFusion somewhere new.

## Pre-transform Vega specifications
VegaFusion supports transforming Vega specifications into new Vega specifications that have had their data transformations already applied.  This is how the VegaFusion mime renderer works.  The pre-transform logic can be invoked directly using the `vegafusion.runtime.pre_transform_spec` function.

See the [pre_transform.ipynb](https://github.com/hex-inc/vegafusion-demos/blob/main/notebooks/pre_transform_vega/pre_transform.ipynb) notebook for more information.

## Pre-transform Vega datasets
VegaFusion supports evaluating select datasets in a Vega specification and returning the results as pandas DataFrames. This is how the `vegafusion.transformed_data` function extracts transformed data from an Altair Chart object.

See the [pre_transform_datasets.ipynb](https://github.com/hex-inc/vegafusion-demos/blob/main/notebooks/pre_transform_vega/pre_transform_datasets.ipynb) notebook for more information.

## Convert Vega-Lite to Vega
VegaFusion works with Vega specifications and has no support for working with Vega-Lite specifications directly.  The [VlConvert](https://github.com/vega/vl-convert) project was developed to make it easy to convert Vega-Lite to Vega without an external web browser or node.js runtime.  The VegaFusion mime renderer and the `transformed_data()` function both rely on the [`vl-convert-python`](https://pypi.org/project/vl-convert-python/) package to convert the Vega-Lite specifications produced by Altair into Vega specifications that are then processed by VegaFusion.

## Custom SQL Connections
VegaFusion's support for evaluating Vega transforms in [DuckDB](duckdb.md) is built on a more general foundation that will be extended to support other SQL query engines in the future.  The [vegafusion-sql](https://github.com/hex-inc/vegafusion/tree/main/vegafusion-sql) crate is responsible for generating dialect specific SQL, and already has initial support for the following SQL dialects:
 - Athena
 - BigQuery
 - ClickHouse
 - Databricks
 - DataFusion
 - DuckDB
 - MySql
 - Postgres
 - Redshift
 - Snowflake

Supporting an additional SQL database involves writing a new Python subclass of the [`SqlConnection`](https://github.com/hex-inc/vegafusion/blob/3210a9365a4ee5ab381316648bdf6ce26828cb0b/python/vegafusion/vegafusion/connection/__init__.py#L21) abstract class. An instance of this subclass may then be passed to the `vegafusion.runtime.set_connection` method.  If you're interested in using VegaFusion with a new SQL query engine, please [start a discussion](https://github.com/hex-inc/vegafusion/discussions).

## Standalone web app
The [`vegafusion-editor-grpc-web`](https://github.com/hex-inc/vegafusion-demos/tree/main/apps/vegafusion-editor-grpc-web) demo is an example of a simple web app that uses the [vegafusion-wasm](https://www.npmjs.com/package/vegafusion-wasm) and [vegafusion-embed](https://www.npmjs.com/package/vegafusion-embed) packages. It connects directly to an instance of the VegaFusion Server over [gRPC-Web](https://github.com/grpc/grpc-web).

The `vegafusion-wasm` and `vegafusion-embed` libraries are the foundation of the client portion of the [`VegaFusionWidget`](./widget.md). By leveraging [tonic's support for gRPC-Web](https://docs.rs/tonic-web/latest/tonic_web/), `vegafusion-wasm` is able to communicate with the VegaFusion server without an intermediary server or proxy. 
