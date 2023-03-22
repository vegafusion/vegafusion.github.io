# DuckDB

[DuckDB](https://duckdb.org/) is an in-process SQL OLAP query engine and database that provides bindings for a wide variety of languages, including Python.  The VegaFusion Python library includes two forms of integration with DuckDB. First, it can use DuckDB in place of DataFusion to power Vega transforms over the pandas DataFrames that are referenced by Altair charts. Second, VegaFusion makes it possible to reference externally defined DuckDB tables and views in Altair charts.

To get started, install the `duckdb` package using pip...

```
pip install "duckdb>=0.7"
```

or conda
```
conda install -c conda-forge "python-duckdb>=0.7"
```

## Vega transforms with DuckDB

VegaFusion can be configured to evaluate Vega transforms using the DuckDB Python library by calling `vegafusion.runtime.set_connection("duckdb")`.

Once the DuckDB connection is enabled, pandas DataFrames referenced by Altair charts are automatically registered with DuckDB and Vega transforms are translated into DuckDB SQL queries. Here is a full example, adapted from the [2D Histogram Heatmap](https://altair-viz.github.io/gallery/histogram_heatmap.html) Altair gallery example.

```python
import vegafusion as vf
import pandas as pd
import altair as alt

# Configure DuckDB connection
vf.runtime.set_connection("duckdb")

# Enable Mime Renderer
vf.enable()

# Load 201k row version of the Vega movies dataset with pandas
movies = pd.read_parquet(
    "https://vegafusion-datasets.s3.amazonaws.com/vega/movies_201k.parquet"
)

# Create an Altair chart from the pandas DataFrame as usual.
# Binning and aggregation will be evaluated against the DataFrame with DuckDB
chart = alt.Chart(movies).mark_rect().encode(
    alt.X('IMDB_Rating:Q', bin=alt.Bin(maxbins=60)),
    alt.Y('Rotten_Tomatoes_Rating:Q', bin=alt.Bin(maxbins=40)),
    alt.Color('count():Q', scale=alt.Scale(scheme='greenblue'))
)
chart
```
![2D Histogram Heatmap](https://user-images.githubusercontent.com/15064365/226609213-2eba5e0b-1377-47d1-9ca9-32dc8f43fb8c.png)

The [transformed data](../../transformed_data.md) can be extracted as usual:
```python
vf.transformed_data(chart, row_limit=5).T
```
|                                           |    0 |     1 |     2 |      3 |      4 |
|:------------------------------------------|-----:|------:|------:|-------:|-------:|
| bin_maxbins_60_IMDB_Rating                |  3.4 |   5.8 |   7   |    7   |    7.4 |
| bin_maxbins_60_IMDB_Rating_end            |  3.6 |   6   |   7.2 |    7.2 |    7.6 |
| bin_maxbins_40_Rotten_Tomatoes_Rating     | 60   |  25   |  85   |   80   |   80   |
| bin_maxbins_40_Rotten_Tomatoes_Rating_end | 65   |  30   |  90   |   85   |   85   |
| __count                                   | 63   | 441   | 504   | 1260   | 1134   |

The default DataFusion connection can be re-enabled by calling `vegafusion.runtime.set_connection("datafusion")`

## Access DuckDB tables
VegaFusion also supports integration with external DuckDB connections, making it possible to reference DuckDB tables and views from Altair charts.  To begin, import `duckdb` and create a new connection.

```python
import duckdb
conn = duckdb.connect()
```

Pass this DuckDB connection to `vegafusion.runtime.set_connection` (instead of the string `"duckdb"` as in the previous example).

```python
vf.runtime.set_connection(conn)
```

Next, use the DuckDB connection to create a table or view. Here, the DuckDB `read_parquet` method is used to load the 201k row movies dataset, and a DuckDB query is used to filter NULL values. The result of this query is registered as a table named `movies`.

```python
relation = conn.read_parquet(
    "https://vegafusion-datasets.s3.amazonaws.com/vega/movies_201k.parquet"
)

relation.query("tbl", """
    SELECT * FROM tbl 
    WHERE Rotten_Tomatoes_Rating IS NOT NULL AND Imdb_Rating IS NOT NULL
""").to_table("movies")
```

DuckDB tables and views registered with `conn` may be referenced from Altair charts with a special URL syntax using `table://` as the prefix. To reference the DuckDB table named `movies`, the Altair chart should be passed the url string `"table://movies"`. Here is a full example

```python
import duckdb
import vegafusion as vf
import pandas as pd
import altair as alt

# Create DuckDB connection
conn = duckdb.connect()

# Pass DuckDB connection to VegaFusion's set_connection method
vf.runtime.set_connection(conn)

# Enable Mime Renderer
vf.enable()

# Read parquet file using the DuckDB connection
relation = conn.read_parquet(
    "https://vegafusion-datasets.s3.amazonaws.com/vega/movies_201k.parquet"
)

# Filter NULL values and register the result as a table named "movies"
relation.query("tbl", """
    SELECT * FROM tbl 
    WHERE Rotten_Tomatoes_Rating IS NOT NULL AND Imdb_Rating IS NOT NULL
""").to_table("movies")

# Create an Altair chart that references the registered DuckDB table
chart = alt.Chart("table://movies").mark_rect().encode(
    alt.X('IMDB_Rating:Q', bin=alt.Bin(maxbins=60)),
    alt.Y('Rotten_Tomatoes_Rating:Q', bin=alt.Bin(maxbins=40)),
    alt.Color('count():Q', scale=alt.Scale(scheme='greenblue'))
)
chart
```
![2D Histogram Heatmap](https://user-images.githubusercontent.com/15064365/226609213-2eba5e0b-1377-47d1-9ca9-32dc8f43fb8c.png)

Note, it's important that the DuckDB connection that's passed to `vegafusion.runtime.set_connection` is used to read the parquet file and register the table named `"movies"`.  The above example would not work if the parquet file were loaded with `duckdb.read_parquet` instead of `conn.read_parquet`. 

## Configuration options
The VegaFusion DuckDB connection provides a few configuration options which are available using the `vegafusion.connection.duckdb.DuckDbConnection` class. 

### Fallback
By default, VegaFusion will fallback to the default DataFusion connection when Vega transform features are encountered that aren't supported by the DuckDB connection. This behavior can be disabled by setting the `fallback` option to `False`. In this case, an error will be raised when unsupported features are required.

### Verbose
When the `verbose` option is set to `True`, VegaFusion will print out the DuckDB queries as they are evaluated.

### Example
Here is an example that sets `fallback` to `False` and `verbose` to `True`.

```python
import vegafusion as vf
from vegafusion.connection.duckdb import DuckDbConnection
import duckdb

# Create DuckDB connection
conn = duckdb.connect()

# Wrap DuckDB connection in a VegaFusion DuckDbConnection instance
# with fallback=False and verbose=True
vf.runtime.set_connection(DuckDbConnection(conn, fallback=False, verbose=True))

# Enable Mime Renderer
vf.enable()

# Read parquet file using the DuckDB connection
relation = conn.read_parquet(
    "https://vegafusion-datasets.s3.amazonaws.com/vega/movies_201k.parquet"
)

# Filter NULL values and register the result as a table named "movies"
relation.query("tbl", """
    SELECT * FROM tbl 
    WHERE Rotten_Tomatoes_Rating IS NOT NULL AND Imdb_Rating IS NOT NULL
""").to_table("movies")

# Create an Altair chart that references the registered DuckDB table
chart = alt.Chart("table://movies").mark_rect().encode(
    alt.X('IMDB_Rating:Q', bin=alt.Bin(maxbins=60)),
    alt.Y('Rotten_Tomatoes_Rating:Q', bin=alt.Bin(maxbins=40)),
    alt.Color('count():Q', scale=alt.Scale(scheme='greenblue'))
)
```
```
DuckDB Query:
WITH movies_0 AS (SELECT "index", "Title", "US_Gross", "Worldwide_Gross", "US_DVD_Sales", "Production_Budget", "Release_Date", "MPAA_Rating", "Running_Time_min", "Distributor", "Source", "Major_Genre", "Creative_Type", "Director", "Rotten_Tomatoes_Rating", "IMDB_Rating", "IMDB_Votes" FROM "movies"), movies_1 AS (SELECT row_number() OVER () AS "_vf_order", * FROM movies_0), movies_2 AS (SELECT "_vf_order" AS "_vf_order", "index" AS "index", "Title" AS "Title", "US_Gross" AS "US_Gross", "Worldwide_Gross" AS "Worldwide_Gross", "US_DVD_Sales" AS "US_DVD_Sales", "Production_Budget" AS "Production_Budget", "Release_Date" AS "Release_Date", "MPAA_Rating" AS "MPAA_Rating", "Running_Time_min" AS "Running_Time_min", "Distributor" AS "Distributor", "Source" AS "Source", "Major_Genre" AS "Major_Genre", "Creative_Type" AS "Creative_Type", "Director" AS "Director", "Rotten_Tomatoes_Rating" AS "Rotten_Tomatoes_Rating", "IMDB_Rating" AS "IMDB_Rating", "IMDB_Votes" AS "IMDB_Votes" FROM movies_1) SELECT min("IMDB_Rating") AS "__min_val", max("IMDB_Rating") AS "__max_val" FROM movies_2

DuckDB Query:
WITH movies_0 AS (SELECT "index", "Title", "US_Gross", "Worldwide_Gross", "US_DVD_Sales", "Production_Budget", "Release_Date", "MPAA_Rating", "Running_Time_min", "Distributor", "Source", "Major_Genre", "Creative_Type", "Director", "Rotten_Tomatoes_Rating", "IMDB_Rating", "IMDB_Votes" FROM "movies"), movies_1 AS (SELECT row_number() OVER () AS "_vf_order", * FROM movies_0), movies_2 AS (SELECT "_vf_order" AS "_vf_order", "index" AS "index", "Title" AS "Title", "US_Gross" AS "US_Gross", "Worldwide_Gross" AS "Worldwide_Gross", "US_DVD_Sales" AS "US_DVD_Sales", "Production_Budget" AS "Production_Budget", "Release_Date" AS "Release_Date", "MPAA_Rating" AS "MPAA_Rating", "Running_Time_min" AS "Running_Time_min", "Distributor" AS "Distributor", "Source" AS "Source", "Major_Genre" AS "Major_Genre", "Creative_Type" AS "Creative_Type", "Director" AS "Director", "Rotten_Tomatoes_Rating" AS "Rotten_Tomatoes_Rating", "IMDB_Rating" AS "IMDB_Rating", "IMDB_Votes" AS "IMDB_Votes" FROM movies_1), movies_3 AS (SELECT *, FLOOR(((("IMDB_Rating" - 1.6) / 0.2) + 0.00000000000001)) AS "__bin_index" FROM movies_2), movies_4 AS (SELECT "_vf_order", "index", "Title", "US_Gross", "Worldwide_Gross", "US_DVD_Sales", "Production_Budget", "Release_Date", "MPAA_Rating", "Running_Time_min", "Distributor", "Source", "Major_Genre", "Creative_Type", "Director", "Rotten_Tomatoes_Rating", "IMDB_Rating", "IMDB_Votes", "__bin_index", CASE WHEN ("__bin_index" < 0.0) THEN CAST('-inf' AS DOUBLE) WHEN (abs(("IMDB_Rating" - 9.4)) < 0.00000000000001) THEN 9.200000000000001 WHEN ("__bin_index" >= 39) THEN CAST('inf' AS DOUBLE) ELSE (("__bin_index" * 0.2) + 1.6) END AS "bin_maxbins_60_IMDB_Rating" FROM movies_3), movies_5 AS (SELECT "_vf_order", "index", "Title", "US_Gross", "Worldwide_Gross", "US_DVD_Sales", "Production_Budget", "Release_Date", "MPAA_Rating", "Running_Time_min", "Distributor", "Source", "Major_Genre", "Creative_Type", "Director", "Rotten_Tomatoes_Rating", "IMDB_Rating", "IMDB_Votes", "bin_maxbins_60_IMDB_Rating", ("bin_maxbins_60_IMDB_Rating" + 0.2) AS "bin_maxbins_60_IMDB_Rating_end" FROM movies_4) SELECT min("Rotten_Tomatoes_Rating") AS "__min_val", max("Rotten_Tomatoes_Rating") AS "__max_val" FROM movies_5

DuckDB Query:
WITH movies_0 AS (SELECT "index", "Title", "US_Gross", "Worldwide_Gross", "US_DVD_Sales", "Production_Budget", "Release_Date", "MPAA_Rating", "Running_Time_min", "Distributor", "Source", "Major_Genre", "Creative_Type", "Director", "Rotten_Tomatoes_Rating", "IMDB_Rating", "IMDB_Votes" FROM "movies"), movies_1 AS (SELECT row_number() OVER () AS "_vf_order", * FROM movies_0), movies_2 AS (SELECT "_vf_order" AS "_vf_order", "index" AS "index", "Title" AS "Title", "US_Gross" AS "US_Gross", "Worldwide_Gross" AS "Worldwide_Gross", "US_DVD_Sales" AS "US_DVD_Sales", "Production_Budget" AS "Production_Budget", "Release_Date" AS "Release_Date", "MPAA_Rating" AS "MPAA_Rating", "Running_Time_min" AS "Running_Time_min", "Distributor" AS "Distributor", "Source" AS "Source", "Major_Genre" AS "Major_Genre", "Creative_Type" AS "Creative_Type", "Director" AS "Director", "Rotten_Tomatoes_Rating" AS "Rotten_Tomatoes_Rating", "IMDB_Rating" AS "IMDB_Rating", "IMDB_Votes" AS "IMDB_Votes" FROM movies_1), movies_3 AS (SELECT *, FLOOR(((("IMDB_Rating" - 1.6) / 0.2) + 0.00000000000001)) AS "__bin_index" FROM movies_2), movies_4 AS (SELECT "_vf_order", "index", "Title", "US_Gross", "Worldwide_Gross", "US_DVD_Sales", "Production_Budget", "Release_Date", "MPAA_Rating", "Running_Time_min", "Distributor", "Source", "Major_Genre", "Creative_Type", "Director", "Rotten_Tomatoes_Rating", "IMDB_Rating", "IMDB_Votes", "__bin_index", CASE WHEN ("__bin_index" < 0.0) THEN CAST('-inf' AS DOUBLE) WHEN (abs(("IMDB_Rating" - 9.4)) < 0.00000000000001) THEN 9.200000000000001 WHEN ("__bin_index" >= 39) THEN CAST('inf' AS DOUBLE) ELSE (("__bin_index" * 0.2) + 1.6) END AS "bin_maxbins_60_IMDB_Rating" FROM movies_3), movies_5 AS (SELECT "_vf_order", "index", "Title", "US_Gross", "Worldwide_Gross", "US_DVD_Sales", "Production_Budget", "Release_Date", "MPAA_Rating", "Running_Time_min", "Distributor", "Source", "Major_Genre", "Creative_Type", "Director", "Rotten_Tomatoes_Rating", "IMDB_Rating", "IMDB_Votes", "bin_maxbins_60_IMDB_Rating", ("bin_maxbins_60_IMDB_Rating" + 0.2) AS "bin_maxbins_60_IMDB_Rating_end" FROM movies_4), movies_6 AS (SELECT *, FLOOR(((("Rotten_Tomatoes_Rating" - 0.0) / 5.0) + 0.00000000000001)) AS "__bin_index" FROM movies_5), movies_7 AS (SELECT "_vf_order", "index", "Title", "US_Gross", "Worldwide_Gross", "US_DVD_Sales", "Production_Budget", "Release_Date", "MPAA_Rating", "Running_Time_min", "Distributor", "Source", "Major_Genre", "Creative_Type", "Director", "Rotten_Tomatoes_Rating", "IMDB_Rating", "IMDB_Votes", "bin_maxbins_60_IMDB_Rating", "bin_maxbins_60_IMDB_Rating_end", "__bin_index", CASE WHEN ("__bin_index" < 0.0) THEN CAST('-inf' AS DOUBLE) WHEN (abs(("Rotten_Tomatoes_Rating" - 100.0)) < 0.00000000000001) THEN 95.0 WHEN ("__bin_index" >= 20) THEN CAST('inf' AS DOUBLE) ELSE (("__bin_index" * 5.0) + 0.0) END AS "bin_maxbins_40_Rotten_Tomatoes_Rating" FROM movies_6), movies_8 AS (SELECT "_vf_order", "index", "Title", "US_Gross", "Worldwide_Gross", "US_DVD_Sales", "Production_Budget", "Release_Date", "MPAA_Rating", "Running_Time_min", "Distributor", "Source", "Major_Genre", "Creative_Type", "Director", "Rotten_Tomatoes_Rating", "IMDB_Rating", "IMDB_Votes", "bin_maxbins_60_IMDB_Rating", "bin_maxbins_60_IMDB_Rating_end", "bin_maxbins_40_Rotten_Tomatoes_Rating", ("bin_maxbins_40_Rotten_Tomatoes_Rating" + 5.0) AS "bin_maxbins_40_Rotten_Tomatoes_Rating_end" FROM movies_7), movies_9 AS (SELECT count(0) AS "__count", min("_vf_order") AS "_vf_order", "bin_maxbins_60_IMDB_Rating", "bin_maxbins_60_IMDB_Rating_end", "bin_maxbins_40_Rotten_Tomatoes_Rating", "bin_maxbins_40_Rotten_Tomatoes_Rating_end" FROM movies_8 GROUP BY "bin_maxbins_60_IMDB_Rating", "bin_maxbins_60_IMDB_Rating_end", "bin_maxbins_40_Rotten_Tomatoes_Rating", "bin_maxbins_40_Rotten_Tomatoes_Rating_end"), movies_10 AS (SELECT "_vf_order", "bin_maxbins_60_IMDB_Rating", "bin_maxbins_60_IMDB_Rating_end", "bin_maxbins_40_Rotten_Tomatoes_Rating", "bin_maxbins_40_Rotten_Tomatoes_Rating_end", "__count" FROM movies_9), movies_11 AS (SELECT * FROM movies_10 WHERE coalesce(((("bin_maxbins_60_IMDB_Rating" IS NOT NULL AND isfinite("bin_maxbins_60_IMDB_Rating")) AND "bin_maxbins_40_Rotten_Tomatoes_Rating" IS NOT NULL) AND isfinite("bin_maxbins_40_Rotten_Tomatoes_Rating")), false)), movies_12 AS (SELECT "_vf_order", "__count", "bin_maxbins_40_Rotten_Tomatoes_Rating", "bin_maxbins_40_Rotten_Tomatoes_Rating_end", "bin_maxbins_60_IMDB_Rating", "bin_maxbins_60_IMDB_Rating_end" FROM movies_11), movies_13 AS (SELECT * FROM movies_12 ORDER BY "_vf_order" ASC NULLS LAST) SELECT "__count", "bin_maxbins_40_Rotten_Tomatoes_Rating", "bin_maxbins_40_Rotten_Tomatoes_Rating_end", "bin_maxbins_60_IMDB_Rating", "bin_maxbins_60_IMDB_Rating_end" FROM movies_13

DuckDB Query:
WITH arrow_d1f7607d_83e8_4826_a706_b57d6a475687_0 AS (SELECT "_vf_order", "__count", "bin_maxbins_40_Rotten_Tomatoes_Rating", "bin_maxbins_40_Rotten_Tomatoes_Rating_end", "bin_maxbins_60_IMDB_Rating", "bin_maxbins_60_IMDB_Rating_end" FROM "arrow_d1f7607d_83e8_4826_a706_b57d6a475687"), arrow_d1f7607d_83e8_4826_a706_b57d6a475687_1 AS (SELECT "_vf_order", "__count" AS "__count", "bin_maxbins_40_Rotten_Tomatoes_Rating", "bin_maxbins_40_Rotten_Tomatoes_Rating_end", "bin_maxbins_60_IMDB_Rating", "bin_maxbins_60_IMDB_Rating_end" FROM arrow_d1f7607d_83e8_4826_a706_b57d6a475687_0), arrow_d1f7607d_83e8_4826_a706_b57d6a475687_2 AS (SELECT min("__count") AS "min", max("__count") AS "max", min("_vf_order") AS "_vf_order" FROM arrow_d1f7607d_83e8_4826_a706_b57d6a475687_1), arrow_d1f7607d_83e8_4826_a706_b57d6a475687_3 AS (SELECT "_vf_order", "min", "max" FROM arrow_d1f7607d_83e8_4826_a706_b57d6a475687_2), arrow_d1f7607d_83e8_4826_a706_b57d6a475687_4 AS (SELECT * FROM arrow_d1f7607d_83e8_4826_a706_b57d6a475687_3 ORDER BY "_vf_order" ASC NULLS LAST) SELECT "min", "max" FROM arrow_d1f7607d_83e8_4826_a706_b57d6a475687_4
```
![2D Histogram Heatmap](https://user-images.githubusercontent.com/15064365/226609213-2eba5e0b-1377-47d1-9ca9-32dc8f43fb8c.png)

The four DuckDB queries required to render this chart are displayed above.