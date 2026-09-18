from main.data_context import get_dataframe


def calculate_total(column):
    """Calculate the total of a numeric column."""
    df = get_dataframe()
    return df[column].sum()


def calculate_average(column):
    """Calculate the average of a numeric column."""
    df = get_dataframe()
    return df[column].mean()


def calculate_minimum(column):
    """Find the minimum value of a numeric column."""
    df = get_dataframe()
    return df[column].min()


def calculate_maximum(column):
    """Find the maximum value of a numeric column."""
    df = get_dataframe()
    return df[column].max()


def calculate_row_count():
    """Count the number of rows in the dataset."""
    df = get_dataframe()
    return len(df)


def calculate_unique_count(column):
    """Count the number of unique values in a column."""
    df = get_dataframe()
    return df[column].nunique()


def calculate_group_sum(group_column, value_column):
    """Calculate the sum of a numeric column grouped by another column."""
    df = get_dataframe()

    result = (
        df.groupby(group_column)[value_column]
        .sum()
        .sort_values(ascending=False)
    )

    return result.to_dict()


def calculate_group_average(group_column, value_column):
    """Calculate the average of a numeric column grouped by another column."""
    df = get_dataframe()

    result = (
        df.groupby(group_column)[value_column]
        .mean()
        .sort_values(ascending=False)
    )

    return result.round(2).to_dict()

def get_top_n(column, n=5):
    """Return the top N rows based on a numeric column."""
    df = get_dataframe()

    result = (
        df.sort_values(by=column, ascending=False)
        .head(n)
    )

    return result.to_dict(orient="records")