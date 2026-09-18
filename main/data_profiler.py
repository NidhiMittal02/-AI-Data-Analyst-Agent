import pandas as pd


def profile_dataframe(df):
    """
    Generate a basic profile and data quality report
    for a Pandas DataFrame.
    """

    # -----------------------------
    # Basic dataset information
    # -----------------------------

    profile = {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "data_types": {},
        "missing_values": {},
        "unique_values": {},
        "numeric_summary": {},
        "quality": {
            "duplicate_rows": 0,
            "empty_columns": [],
            "total_missing_values": 0
        }
    }

    # -----------------------------
    # Data types
    # -----------------------------

    for column in df.columns:
        profile["data_types"][column] = str(
            df[column].dtype
        )

    # -----------------------------
    # Missing values
    # -----------------------------

    for column in df.columns:

        missing_count = int(
            df[column].isna().sum()
        )

        profile["missing_values"][column] = missing_count

        profile["quality"]["total_missing_values"] += (
            missing_count
        )

    # -----------------------------
    # Unique values
    # -----------------------------

    for column in df.columns:

        profile["unique_values"][column] = int(
            df[column].nunique()
        )

    # -----------------------------
    # Duplicate rows
    # -----------------------------

    profile["quality"]["duplicate_rows"] = int(
        df.duplicated().sum()
    )

    # -----------------------------
    # Empty columns
    # -----------------------------

    for column in df.columns:

        if df[column].isna().all():
            profile["quality"]["empty_columns"].append(
                column
            )

    # -----------------------------
    # Numeric statistics
    # -----------------------------

    numeric_df = df.select_dtypes(
        include="number"
    )

    if not numeric_df.empty:

        profile["numeric_summary"] = (
            numeric_df.describe()
            .round(2)
            .to_dict()
        )

    return profile