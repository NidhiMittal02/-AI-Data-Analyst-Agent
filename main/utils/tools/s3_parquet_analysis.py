import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def query_s3_parquet(s3_path: str, sql_query: str) -> list:
    """
    Runs a SQL query on parquet files stored in S3 using DuckDB and returns the result as a list of dicts.
    
    Args:
        s3_path (str): S3 path to the parquet files (can include wildcards).
        sql_query (str): SQL query string, can reference the parquet path as 'data'.
    
    Returns:
        list: Query result as a list of dictionaries.
    """
    con = duckdb.connect()
    con.execute("INSTALL httpfs; LOAD httpfs; INSTALL parquet; LOAD parquet;")
    con.execute(f"CREATE VIEW data AS SELECT * FROM read_parquet('{s3_path}')")
    return con.execute(sql_query).fetchdf().to_dict(orient="records")


def regression_slope(df: pd.DataFrame, x_col: str, y_col: str) -> float:
    """
    Computes the regression slope between two numeric columns in a DataFrame.
    
    Args:
        df (pd.DataFrame): Data containing x_col and y_col.
        x_col (str): Column name for X-axis variable.
        y_col (str): Column name for Y-axis variable.
    
    Returns:
        float: Regression slope.
    """
    return df[y_col].cov(df[x_col]) / df[x_col].var()


def plot_scatter_with_regression(df: pd.DataFrame, x_col: str, y_col: str,
                                 x_label: str = None, y_label: str = None,
                                 title: str = None) -> str:
    """
    Plots a scatterplot of two columns with a regression line, returns image as base64 data URI.
    
    Args:
        df (pd.DataFrame): Data containing x_col and y_col.
        x_col (str): X-axis column.
        y_col (str): Y-axis column.
        x_label (str): Optional label for X-axis.
        y_label (str): Optional label for Y-axis.
        title (str): Optional plot title.
    
    Returns:
        str: Base64 data URI of the plot in webp format.
    """
    plt.figure(figsize=(6, 4))
    plt.scatter(df[x_col], df[y_col], label="Data Points", color="blue")

    slope = regression_slope(df, x_col, y_col)
    intercept = df[y_col].mean() - slope * df[x_col].mean()
    plt.plot(df[x_col], slope * df[x_col] + intercept, color="red", label="Regression Line")

    plt.xlabel(x_label or x_col)
    plt.ylabel(y_label or y_col)
    if title:
        plt.title(title)
    plt.legend()

    buf = BytesIO()
    plt.savefig(buf, format="webp")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()

    return f"data:image/webp;base64,{img_base64}"