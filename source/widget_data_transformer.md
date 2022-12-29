# Feather Data Transformer
The VegaFusion widget renderer provides a custom [data transformer](https://altair-viz.github.io/user_guide/data_transformers.html). When an Altair chart is created based on a pandas DataFrame, the `VegaFusionWidget`'s data transformer will extract the DataFrame and save it to a [feather file](https://arrow.apache.org/docs/python/feather.html) in a `_vegafusion_data` directory in the current directory.  The feather file's name is generated based on a hash of the DataFrame's contents, so new files will only be added to the directory when charts are created with new DataFrames.  Feel free to delete the directory when no interactive VegaFusion charts are currently being displayed, but deleting the directory while an interactive chart is being displayed may result in an error.

This approach is implemented by the `"vegafusion-feather"` data transformer, which is automatically enabled by the `vegafusion.enable_widget()` function or when using `VegaFusionWidget` directly.

## Customizing Feather File Directory
The directory that these feather files are written to can be customized...