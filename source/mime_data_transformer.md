# Inline Data Transformer
Unlike the VegaFusion widget renderer, the mime renderer does not require writing Chart DataFrames to files on disk. Instead, these DataFrames are converted to Arrow tables and passed directly to the VegaFusion runtime (bypassing JSON serialization).

This approach is implemented by the `"vegafusion-inline"` data transformer, which is automatically enabled by the `vegafusion.enable_mime()` function.