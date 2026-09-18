import pandas as pd


def total(df, column):
    """Calculate the total of a numeric column."""
    return df[column].sum()


def average(df, column):
    """Calculate the average of a numeric column."""
    return df[column].mean()


def minimum(df, column):
    """Find the minimum value of a numeric column."""
    return df[column].min()


def maximum(df, column):
    """Find the maximum value of a numeric column."""
    return df[column].max()


def count_rows(df):
    """Count the number of rows in the dataset."""
    return len(df)


def count_unique(df, column):
    """Count unique values in a column."""
    return df[column].nunique()


def group_sum(df, group_column, value_column):
    """
    Calculate the sum of a numeric column
    grouped by another column.
    """

    result = (
        df.groupby(group_column)[value_column]
        .sum()
        .sort_values(ascending=False)
    )

    return result.to_dict()


def group_average(df, group_column, value_column):
    """
    Calculate the average of a numeric column
    grouped by another column.
    """

    result = (
        df.groupby(group_column)[value_column]
        .mean()
        .sort_values(ascending=False)
    )

    return result.round(2).to_dict()


def top_n(df, column, n=5):
    """Return the top N rows based on a numeric column."""

    result = (
        df.sort_values(by=column, ascending=False)
        .head(n)
    )

    return result.to_dict(orient="records")


def percentage_of_total(df, column, value):
    """
    Calculate what percentage a value represents
    of the total of a numeric column.
    """

    total_value = df[column].sum()

    if total_value == 0:
        return 0

    return (value / total_value) * 100