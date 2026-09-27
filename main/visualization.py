import io
import base64

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

    The chart is returned as a base64 data URL
    so it works in serverless environments such as Vercel.
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

    # Store the image in memory instead of saving it
    # to the Vercel filesystem.
    image_buffer = io.BytesIO()

    plt.savefig(
        image_buffer,
        format="png",
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()

    # Move to the beginning of the buffer
    image_buffer.seek(0)

    # Convert image bytes to base64
    image_base64 = base64.b64encode(
        image_buffer.getvalue()
    ).decode("utf-8")

    # Return a browser-ready image
    return (
        "data:image/png;base64,"
        + image_base64
    )