# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'VegaFusion'
copyright = '2022, Jon Mease'
author = 'Jon Mease'

# The full version, including alpha/beta/rc tags
release = '0.1.0'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_parser",
    "ablog",
    "sphinx.ext.intersphinx",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# html_theme = "pydata_sphinx_theme"
# html_theme = "alabaster"
# html_theme = "bootstrap"
# html_theme = "karma_sphinx_theme"
# html_theme = 'sphinx_material'

# html_permalinks_icon = '§'
# html_theme = 'insipid'

# # Nice one
# html_theme = 'press'
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = [
    'css/site.css',
]
html_logo = "_static/VegaFusionLogo-Color.svg"
html_favicon = "_static/favicon.ico"

# -- Blog configuration ------------------------------------------------------
blog_post_pattern = "posts/*/*"
blog_path = "blog"
blog_title = "VegaFusion Blog"

# -- Theme options ----
html_theme_options = {
    'analytics_id': 'G-LVD2GWXRQZ',
}

_social_img = "https://vegafusion.io/_static/vegafusion_social.png"
_description = "VegaFusion provides serverside acceleration of the Vega visualization grammar"
_title = "VegaFusion"

myst_html_meta = {
    "description lang=en": _description,
    "property=og:title":  _title,
    "property=og:description":  _description,
    "property=og:locale":  "en_US",
    "property=og:url":  "https://vegafusion.io/",
    "property=og:image":  _social_img,
    "property=twitter:site": "@vegafusion_io",
    "property=twitter:image": _social_img,
    "property=twitter:card": "summary_large_image"
}
