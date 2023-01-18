# Low Level Integration
The VegaFusion mime and widget renderers are built from lower-level primitives that can be used to integrate VegaFusion in non-Jupyter, and non-Python, contexts. Documentation of these lower-level constructs is not yet complete, so in the meantime please [start a discussion](https://github.com/hex-inc/vegafusion/discussions) if you're interested in integrating VegaFusion somewhere new.

## Pre-transform Vega specifications
VegaFusion supports transforming Vega specifications into new Vega specifications that have had their data transformations already applied.  This is how the VegaFusion mime renderer works.  The pre-transform logic can be invoked directly using the `vegafusion.runtime.pre_transform_spec` function.

See the [pre_transform.ipynb](https://github.com/hex-inc/vegafusion-demos/blob/main/notebooks/pre_transform_vega/pre_transform.ipynb) notebook for more information.

## Pre-transform Vega datasets
VegaFusion supports evaluating select datasets in a Vega specification and returning the results as pandas DataFrames. This is how the `vegafusion.transformed_data` function extracts transformed data from an Altair Chart object.

See the [pre_transform_datasets.ipynb](https://github.com/hex-inc/vegafusion-demos/blob/main/notebooks/pre_transform_vega/pre_transform_datasets.ipynb) notebook for more information.

## Convert Vega-Lite to Vega
VegaFusion works with Vega specifications and has no support for working with Vega-Lite specifications directly.  The [VlConvert](https://github.com/vega/vl-convert) project was developed to make it easy to convert Vega-Lite to Vega without an external web browser or node.js runtime.  The VegaFusion mime renderer and the `transformed_data()` function both rely on the [`vl-convert-python`](https://pypi.org/project/vl-convert-python/) package to convert the Vega-Lite specifications produced by Altair into Vega specifications that are then processed by VegaFusion.


