import os

import matplotlib

# Use a non-GUI backend because Flask runs requests
# outside the main Matplotlib thread.
matplotlib.use("Agg")

import matplotlib.pyplot as plt


def create_bar_chart(
    df,
    category_column,
    value_column,
    limit=None
):
    """
    Create a bar chart showing total values by category.

    If limit is provided, only the top N categories
    are displayed.
    """

    # Group the data
    grouped = (
        df.groupby(category_column)[value_column]
        .sum()
        .sort_values(ascending=False)
    )

    # Keep only the top N groups when requested
    if limit is not None:
        grouped = grouped.head(limit)

    # Create chart
    plt.figure(figsize=(8, 5))

    grouped.plot(kind="bar")

    plt.title(
        f"{value_column} by {category_column}"
    )

    plt.xlabel(category_column)

    plt.ylabel(value_column)

    plt.xticks(rotation=45)

    plt.tight_layout()

    # Make sure chart directory exists
    chart_directory = os.path.join(
        "static",
        "charts"
    )

    os.makedirs(
        chart_directory,
        exist_ok=True
    )

    # Create filename
    if limit is not None:
        filename = (
            f"{category_column}_"
            f"{value_column}_"
            f"top_{limit}_bar.png"
        )
    else:
        filename = (
            f"{category_column}_"
            f"{value_column}_"
            f"bar.png"
        )

    chart_path = os.path.join(
        chart_directory,
        filename
    )

    # Save chart
    plt.savefig(
        chart_path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()

    return chart_path