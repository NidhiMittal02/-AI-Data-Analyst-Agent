import pandas as pd

def read_csv_url(url: str) -> list:
    """
    Reads a CSV file directly from a URL and returns its contents as a list of dictionaries.
    
    Args:
        url (str): The URL to the CSV file.
    
    Returns:
        list: List of rows as dictionaries.
    """
    df = pd.read_csv(url)
    return df.to_dict(orient="records")


def filter_rows(data: list, column: str, value) -> list:
    """
    Filters rows where a specific column matches a given value.
    
    Args:
        data (list): List of rows as dictionaries.
        column (str): Column name to filter on.
        value: Value to match.
    
    Returns:
        list: Filtered rows as dictionaries.
    """
    df = pd.DataFrame(data)
    return df[df[column] == value].to_dict(orient="records")


def sort_data(data: list, column: str, ascending: bool = True) -> list:
    """
    Sorts the data by a given column.
    
    Args:
        data (list): List of rows as dictionaries.
        column (str): Column to sort by.
        ascending (bool): Sort order. True for ascending, False for descending.
    
    Returns:
        list: Sorted rows as dictionaries.
    """
    df = pd.DataFrame(data)
    return df.sort_values(by=column, ascending=ascending).to_dict(orient="records")


def describe_data(data: list) -> dict:
    """
    Returns statistical summary of numeric columns.
    
    Args:
        data (list): List of rows as dictionaries.
    
    Returns:
        dict: Statistical summary as a dictionary.
    """
    df = pd.DataFrame(data)
    return df.describe().to_dict()


def select_columns(data: list, columns: list) -> list:
    """
    Selects only the specified columns from the dataset.
    
    Args:
        data (list): List of rows as dictionaries.
        columns (list): List of column names to select.
    
    Returns:
        list: Data with only the selected columns.
    """
    df = pd.DataFrame(data)
    return df[columns].to_dict(orient="records")