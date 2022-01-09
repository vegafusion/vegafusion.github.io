# Altair Renderer and Data Transformer
## VegaFusion Renderer
As an alternative to using `VegaFusionWidget` directly, VegaFusion provides a custom [Altair renderer](https://altair-viz.github.io/user_guide/display_frontends.html). This uses the `VegaFusionWidget` for display, but it doesn't require explicit construction of a `VegaFusionWidget` instance.

## VegaFusion Data Transformer
VegaFusion also provides a custom [data transformer](https://altair-viz.github.io/user_guide/data_transformers.html). When an Altair chart is created based on a pandas DataFrame, the VegaFusion transformer will extract the DataFrame and save it to a feather file in the `_vegafusion_data` directory in the current directory

## Activating Renderer and Data Transformer
The VegaFusion renderer and data transformer can both be activated using the `activate` function from the `vegafusion-jupyter` package.

```python
import vegafusion_jupyter as vf
vf.activate()
```