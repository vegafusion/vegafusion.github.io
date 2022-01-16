# Construction
A `VegaFusionWidget` can be constructed from:
 1. A Altair `Chart` instance
 2. A Python dict representing a Vega or Vega-Lite JSON specification
 3. A String containing a Vega or Vega-Lite JSON specification

These values may be passed to the `VegaFusionWidget` as the sole positional argument, or as the `spec` keyword argument

## Construct from an Altair Chart

```python
import vegafusion_jupyter as vf
import altair as alt
from vega_datasets import data

source = data.movies.url

chart = alt.Chart(source).mark_bar().encode(
    alt.X("IMDB_Rating:Q", bin=True),
    y='count()',
)
vf.VegaFusionWidget(chart)
```
<img width="519" alt="Histogram" src="https://user-images.githubusercontent.com/15064365/148783521-81c5d183-0a6f-41ca-a0c1-0c76e23d65df.png">

## Construct from a Vega-Lite Specification Dictionary

```python
import vegafusion_jupyter as vf
import altair as alt

vegalite_spec = {
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": {"url": "data/seattle-weather.csv"},
  "mark": "bar",
  "encoding": {
    "x": {
      "timeUnit": "month",
      "field": "date",
      "type": "ordinal",
      "title": "Month of the year"
    },
    "y": {
      "aggregate": "count",
      "type": "quantitative"
    },
    "color": {
      "field": "weather",
      "type": "nominal",
      "scale": {
        "domain": ["sun", "fog", "drizzle", "rain", "snow"],
        "range": ["#e7ba52", "#c7c7c7", "#aec7e8", "#1f77b4", "#9467bd"]
      },
      "title": "Weather type"
    }
  }
}
vf.VegaFusionWidget(vegalite_spec)
```
<img width="424" alt="Screen Shot 2022-01-10 at 9 39 23 AM" src="https://user-images.githubusercontent.com/15064365/148783961-8106bc35-f584-42de-ac9e-fb1a8d2af637.png">

## Construct from a Vega Specification String

```python
import vegafusion_jupyter as vf
import altair as alt

vega_spec = r"""
{
  "$schema": "https://vega.github.io/schema/vega/v5.json",
  "description": "A binned scatter plot example showing aggregate counts per binned cell.",
  "width": 200,
  "height": 200,
  "padding": 5,
  "autosize": "pad",

  "data": [
    {
      "name": "source",
      "url": "data/cars.json",
      "transform": [
        {
          "type": "filter",
          "expr": "datum['Horsepower'] != null && datum['Miles_per_Gallon'] != null && datum['Acceleration'] != null"
        }
      ]
    },
    {
      "name": "summary",
      "source": "source",
      "transform": [
        {
          "type": "extent", "field": "Horsepower",
          "signal": "hp_extent"
        },
        {
          "type": "bin", "field": "Horsepower", "maxbins": 10,
          "extent": {"signal": "hp_extent"},
          "as": ["hp0", "hp1"]
        },
        {
          "type": "extent", "field": "Miles_per_Gallon",
          "signal": "mpg_extent"
        },
        {
          "type": "bin", "field": "Miles_per_Gallon", "maxbins": 10,
          "extent": {"signal": "mpg_extent"},
          "as": ["mpg0", "mpg1"]
        },
        {
          "type": "aggregate",
          "groupby": ["hp0", "hp1", "mpg0", "mpg1"]
        }
      ]
    }
  ],

  "scales": [
    {
      "name": "x",
      "type": "linear",
      "round": true,
      "nice": true,
      "zero": true,
      "domain": {"data": "source", "field": "Horsepower"},
      "range": "width"
    },
    {
      "name": "y",
      "type": "linear",
      "round": true,
      "nice": true,
      "zero": true,
      "domain": {"data": "source", "field": "Miles_per_Gallon"},
      "range": "height"
    },
    {
      "name": "size",
      "type": "linear",
      "zero": true,
      "domain": {"data": "summary", "field": "count"},
      "range": [0,360]
    }
  ],

  "axes": [
    {
      "scale": "x",
      "grid": true,
      "domain": false,
      "orient": "bottom",
      "tickCount": 5,
      "title": "Horsepower"
    },
    {
      "scale": "y",
      "grid": true,
      "domain": false,
      "orient": "left",
      "titlePadding": 5,
      "title": "Miles_per_Gallon"
    }
  ],

  "legends": [
    {
      "size": "size",
      "title": "Count",
      "format": "s",
      "symbolFillColor": "#4682b4",
      "symbolStrokeColor": "transparent",
      "symbolType": "circle"
    }
  ],

  "marks": [
    {
      "name": "marks",
      "type": "symbol",
      "from": {"data": "summary"},
      "encode": {
        "update": {
          "x": {"scale": "x", "signal": "(datum.hp0 + datum.hp1) / 2"},
          "y": {"scale": "y", "signal": "(datum.mpg0 + datum.mpg1) / 2"},
          "size": {"scale": "size", "field": "count"},
          "shape": {"value": "circle"},
          "fill": {"value": "#4682b4"}
        }
      }
    }
  ]
}
"""

vf.VegaFusionWidget(vega_spec)
```

<img width="360" alt="Screen Shot 2022-01-10 at 10 03 15 AM" src="https://user-images.githubusercontent.com/15064365/148787878-675daf43-f228-4486-96ad-788481e3315d.png">
