import pandas as pd


_current_dataframe = None


def set_dataframe(df):
    """Store the currently uploaded DataFrame."""
    global _current_dataframe
    _current_dataframe = df


def get_dataframe():
    """Return the currently uploaded DataFrame."""
    if _current_dataframe is None:
        raise ValueError("No dataset has been uploaded yet.")

    return _current_dataframe