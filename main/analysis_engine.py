from data_context import get_dataframe

import re

from utils.tools.analysis_tools import (
    calculate_total,
    calculate_average,
    calculate_minimum,
    calculate_maximum,
    calculate_row_count,
    calculate_unique_count,
    calculate_group_sum,
    calculate_group_average,
)


def analyze_question(question):
    """
    Convert a natural-language analytical question
    into a reliable Pandas calculation.

    Supported operations:

    1. Total
    2. Average
    3. Minimum
    4. Maximum
    5. Row count
    6. Unique count
    7. Grouped totals
    8. Grouped averages
    9. Top-N groups
    10. Highest-performing group

    The calculations themselves are performed using
    Pandas analysis tools.
    """

    # ========================================================
    # GET CURRENT DATAFRAME
    # ========================================================

    df = get_dataframe()

    question_lower = (
        question.lower().strip()
    )


    # ========================================================
    # DATAFRAME COLUMNS
    # ========================================================

    all_columns = list(
        df.columns
    )

    numeric_columns = list(
        df.select_dtypes(
            include="number"
        ).columns
    )


    # ========================================================
    # COLUMN ALIASES
    # ========================================================
    #
    # This allows users to use common business words.
    #
    # Example:
    #
    # revenue -> Sales
    # amount  -> Sales
    #
    # Only use an alias when the corresponding
    # actual dataframe column exists.
    # ========================================================

    def find_column(
        text,
        columns
    ):

        # ----------------------------------------------------
        # First try exact column names.
        # ----------------------------------------------------

        for column in columns:

            if column.lower() in text:

                return column


        # ----------------------------------------------------
        # Common aliases
        # ----------------------------------------------------

        aliases = {

            "sales": [
                "sales",
                "sale",
                "revenue",
                "revenues",
                "amount",
                "income"
            ],

            "quantity": [
                "quantity",
                "qty",
                "units",
                "unit"
            ],

            "product": [
                "product",
                "products",
                "item",
                "items"
            ],

            "customer": [
                "customer",
                "customers",
                "client",
                "clients"
            ],

            "category": [
                "category",
                "categories",
                "type"
            ]

        }


        # ----------------------------------------------------
        # Check aliases against actual columns
        # ----------------------------------------------------

        for column in columns:

            column_lower = (
                column.lower()
            )


            for canonical_name, words in (
                aliases.items()
            ):

                if column_lower == canonical_name:

                    for word in words:

                        if word in text:

                            return column


        return None


    # ========================================================
    # FIND GROUP COLUMN
    # ========================================================

    def find_group_column(text):

        # ----------------------------------------------------
        # First check actual categorical columns.
        # ----------------------------------------------------

        for column in all_columns:

            if column in numeric_columns:

                continue


            if column.lower() in text:

                return column


        # ----------------------------------------------------
        # Then check common business aliases.
        # ----------------------------------------------------

        return find_column(
            text,
            [
                column
                for column in all_columns
                if column not in numeric_columns
            ]
        )


    # ========================================================
    # DETECT VALUE COLUMN
    # ========================================================

    def find_value_column(text):

        return find_column(
            text,
            numeric_columns
        )


    # ========================================================
    # TOP N
    # ========================================================
    #
    # Examples:
    #
    # Show top 2 products by Sales
    # Show top 3 products
    # Give me the top 5 products by revenue
    # What are the top 3 products?
    # ========================================================

    top_match = re.search(
        r"\btop\s+(\d+)\b",
        question_lower
    )


    if top_match:

        n = int(
            top_match.group(1)
        )


        # Prevent extremely large requests.

        n = min(
            n,
            20
        )


        value_column = (
            find_value_column(
                question_lower
            )
        )


        group_column = (
            find_group_column(
                question_lower
            )
        )


        # ----------------------------------------------------
        # If the question says "top 3 products"
        # but doesn't explicitly mention Sales,
        # use the first numeric column when there is
        # only one numeric column.
        # ----------------------------------------------------

        if (
            value_column is None
            and len(numeric_columns) == 1
        ):

            value_column = (
                numeric_columns[0]
            )


        # ----------------------------------------------------
        # If no group column is explicitly mentioned,
        # use the first categorical column when
        # there is only one.
        # ----------------------------------------------------

        categorical_columns = [

            column
            for column in all_columns
            if column not in numeric_columns

        ]


        if (
            group_column is None
            and len(categorical_columns) == 1
        ):

            group_column = (
                categorical_columns[0]
            )


        if (
            value_column
            and group_column
        ):

            grouped_result = (
                calculate_group_sum(
                    group_column,
                    value_column
                )
            )


            top_groups = dict(
                list(
                    grouped_result.items()
                )[:n]
            )


            return {

                "type":
                    "grouped_calculation",

                "operation":
                    "top_groups",

                "group_column":
                    group_column,

                "value_column":
                    value_column,

                "n":
                    n,

                "result":
                    top_groups

            }


    # ========================================================
    # HIGHEST / MOST / LARGEST
    # ========================================================
    #
    # Examples:
    #
    # Which product has the highest sales?
    # Which product made the most sales?
    # Which product generated the most revenue?
    # What is the largest product by sales?
    # ========================================================

    highest_words = [

        "highest",
        "most",
        "maximum",
        "largest",
        "best performing",
        "top performing"

    ]


    if any(
        word in question_lower
        for word in highest_words
    ):

        value_column = (
            find_value_column(
                question_lower
            )
        )


        group_column = (
            find_group_column(
                question_lower
            )
        )


        # If there is only one numeric column,
        # it can safely be used as the value column.

        if (
            value_column is None
            and len(numeric_columns) == 1
        ):

            value_column = (
                numeric_columns[0]
            )


        # If there is only one categorical column,
        # use it as the grouping column.

        categorical_columns = [

            column
            for column in all_columns
            if column not in numeric_columns

        ]


        if (
            group_column is None
            and len(categorical_columns) == 1
        ):

            group_column = (
                categorical_columns[0]
            )


        if (
            value_column
            and group_column
        ):

            grouped_result = (
                calculate_group_sum(
                    group_column,
                    value_column
                )
            )


            highest_group = max(
                grouped_result,
                key=grouped_result.get
            )


            highest_value = (
                grouped_result[
                    highest_group
                ]
            )


            return {

                "type":
                    "grouped_calculation",

                "operation":
                    "highest_group",

                "group_column":
                    group_column,

                "value_column":
                    value_column,

                "group":
                    highest_group,

                "result":
                    highest_value,

                "all_groups":
                    grouped_result

            }


    # ========================================================
    # GROUPED AVERAGE
    # ========================================================
    #
    # Examples:
    #
    # Average sales by product
    # Average sales for each product
    # Mean sales per product
    # Give me average revenue for every product
    # ========================================================

    is_average_question = (

        "average" in question_lower

        or

        "mean" in question_lower

    )


    has_grouping_words = (

        "by" in question_lower

        or

        "each" in question_lower

        or

        "per" in question_lower

        or

        "across" in question_lower

        or

        "for every" in question_lower

    )


    if (
        is_average_question
        and has_grouping_words
    ):

        value_column = (
            find_value_column(
                question_lower
            )
        )


        group_column = (
            find_group_column(
                question_lower
            )
        )


        # Single numeric column fallback.

        if (
            value_column is None
            and len(numeric_columns) == 1
        ):

            value_column = (
                numeric_columns[0]
            )


        # Single categorical column fallback.

        categorical_columns = [

            column
            for column in all_columns
            if column not in numeric_columns

        ]


        if (
            group_column is None
            and len(categorical_columns) == 1
        ):

            group_column = (
                categorical_columns[0]
            )


        if (
            value_column
            and group_column
        ):

            return {

                "type":
                    "grouped_calculation",

                "operation":
                    "group_average",

                "group_column":
                    group_column,

                "value_column":
                    value_column,

                "result":
                    calculate_group_average(
                        group_column,
                        value_column
                    )

            }


    # ========================================================
    # GROUPED TOTAL
    # ========================================================
    #
    # Examples:
    #
    # Show total sales by product
    # Sales by product
    # Total sales for each product
    # Compare sales across products
    # ========================================================

    has_grouping_words = (

        "by" in question_lower

        or

        "each" in question_lower

        or

        "per" in question_lower

        or

        "across" in question_lower

        or

        "for every" in question_lower

        or

        "compare" in question_lower

    )


    if has_grouping_words:

        value_column = (
            find_value_column(
                question_lower
            )
        )


        group_column = (
            find_group_column(
                question_lower
            )
        )


        # Single numeric column fallback.

        if (
            value_column is None
            and len(numeric_columns) == 1
        ):

            value_column = (
                numeric_columns[0]
            )


        # Single categorical column fallback.

        categorical_columns = [

            column
            for column in all_columns
            if column not in numeric_columns

        ]


        if (
            group_column is None
            and len(categorical_columns) == 1
        ):

            group_column = (
                categorical_columns[0]
            )


        if (
            value_column
            and group_column
        ):

            return {

                "type":
                    "grouped_calculation",

                "operation":
                    "group_sum",

                "group_column":
                    group_column,

                "value_column":
                    value_column,

                "result":
                    calculate_group_sum(
                        group_column,
                        value_column
                    )

            }


    # ========================================================
    # TOTAL
    # ========================================================
    #
    # Examples:
    #
    # What is the total sales?
    # How much did we sell in total?
    # Give me the overall sales.
    # What is total revenue?
    # ========================================================

    total_words = (

        "total" in question_lower

        or

        "sum" in question_lower

        or

        "overall" in question_lower

        or

        "how much" in question_lower

        or

        "in total" in question_lower

    )


    if total_words:

        value_column = (
            find_value_column(
                question_lower
            )
        )


        # If only one numeric column exists,
        # use it automatically.

        if (
            value_column is None
            and len(numeric_columns) == 1
        ):

            value_column = (
                numeric_columns[0]
            )


        if value_column:

            return {

                "type":
                    "calculation",

                "operation":
                    "total",

                "column":
                    value_column,

                "result":
                    calculate_total(
                        value_column
                    )

            }


    # ========================================================
    # AVERAGE
    # ========================================================

    if (

        "average" in question_lower

        or

        "mean" in question_lower

    ):

        value_column = (
            find_value_column(
                question_lower
            )
        )


        if (
            value_column is None
            and len(numeric_columns) == 1
        ):

            value_column = (
                numeric_columns[0]
            )


        if value_column:

            return {

                "type":
                    "calculation",

                "operation":
                    "average",

                "column":
                    value_column,

                "result":
                    calculate_average(
                        value_column
                    )

            }


    # ========================================================
    # MINIMUM
    # ========================================================

    if (

        "minimum" in question_lower

        or

        "lowest" in question_lower

        or

        "smallest" in question_lower

        or

        "least" in question_lower

    ):

        value_column = (
            find_value_column(
                question_lower
            )
        )


        if (
            value_column is None
            and len(numeric_columns) == 1
        ):

            value_column = (
                numeric_columns[0]
            )


        if value_column:

            return {

                "type":
                    "calculation",

                "operation":
                    "minimum",

                "column":
                    value_column,

                "result":
                    calculate_minimum(
                        value_column
                    )

            }


    # ========================================================
    # MAXIMUM
    # ========================================================

    if (

        "maximum" in question_lower

        or

        "highest" in question_lower

        or

        "largest" in question_lower

    ):

        value_column = (
            find_value_column(
                question_lower
            )
        )


        if (
            value_column is None
            and len(numeric_columns) == 1
        ):

            value_column = (
                numeric_columns[0]
            )


        if value_column:

            return {

                "type":
                    "calculation",

                "operation":
                    "maximum",

                "column":
                    value_column,

                "result":
                    calculate_maximum(
                        value_column
                    )

            }


    # ========================================================
    # ROW COUNT
    # ========================================================

    row_count_words = (

        "how many rows" in question_lower

        or

        "row count" in question_lower

        or

        "number of rows" in question_lower

        or

        "how many records" in question_lower

        or

        "number of records" in question_lower

        or

        "how many entries" in question_lower

        or

        "number of entries" in question_lower

    )


    if row_count_words:

        return {

            "type":
                "calculation",

            "operation":
                "row_count",

            "result":
                calculate_row_count()

        }


    # ========================================================
    # UNIQUE COUNT
    # ========================================================
    #
    # Examples:
    #
    # How many unique products are there?
    # Number of distinct products
    # How many different products?
    # ========================================================

    unique_words = (

        "unique" in question_lower

        or

        "distinct" in question_lower

        or

        "different" in question_lower

    )


    if unique_words:

        column = find_column(
            question_lower,
            all_columns
        )


        # If no column is explicitly mentioned
        # and there is only one categorical column,
        # use that column.

        if column is None:

            categorical_columns = [

                column_name
                for column_name in all_columns
                if column_name not in numeric_columns

            ]


            if len(
                categorical_columns
            ) == 1:

                column = (
                    categorical_columns[0]
                )


        if column:

            return {

                "type":
                    "calculation",

                "operation":
                    "unique_count",

                "column":
                    column,

                "result":
                    calculate_unique_count(
                        column
                    )

            }


    # ========================================================
    # NO MATCH
    # ========================================================

    return None