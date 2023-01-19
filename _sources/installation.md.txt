# Installation

## pip
The VegaFusion package that provides the mime renderer can be installed into a Python environment using pip with
```bash
pip install "vegafusion[embed]"
```

The VegaFusion widget renderer is provided by the `vegafusion-jupyter` package
```bash
pip install "vegafusion-jupyter[embed]"
```

## conda
VegaFusion can also be installed using conda from conda-forge

```bash
conda install -c conda-forge vegafusion vegafusion-python-embed vegafusion-jupyter
```

**Note:** Conda packages for the `osx-arm64` (aka Apple Silicon, M1) architecture are not yet available. See https://github.com/hex-inc/vegafusion/issues/199. This architecture is already supported by the PyPI packages installable using pip.
