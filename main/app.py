import io
import os
import base64

import pandas as pd

from flask import (
    Flask,
    request,
    jsonify,
    send_from_directory,
    render_template
)

from flask_cors import CORS
from flasgger import Swagger

from main.groq_client import Groq
from main.miscellaneous import ask_agent

from main.data_profiler import profile_dataframe

from main.data_context import (
    set_dataframe,
    get_dataframe
)

from main.analysis_engine import analyze_question

from main.visualization import create_bar_chart

# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..'
    )
)

UPLOAD_DIR = os.path.join(
    BASE_DIR,
    "uploads"
)


# ============================================================
# FLASK APP
# ============================================================

app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static'
)

CORS(app)

Swagger(app)


# ============================================================
# HOME PAGE
# ============================================================

@app.route('/')
def index():

    return render_template(
        'index.html'
    )


# ============================================================
# SERVE UPLOADED FILES
# ============================================================

@app.route(
    '/uploads/<path:filename>'
)
def serve_upload(filename):

    return send_from_directory(
        UPLOAD_DIR,
        filename
    )


# ============================================================
# SAVE FILE LOCALLY
# ============================================================

def save_locally(
    file_bytes,
    filename
):

    """
    Save an uploaded file locally.
    """

    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True
    )

    path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(
        path,
        "wb"
    ) as file:

        file.write(
            file_bytes
        )

    return (
        f"http://{request.host}"
        f"/uploads/{filename}"
    )


# ============================================================
# READ AND PROFILE DATASET
# ============================================================

def analyze_uploaded_file(
    filename,
    data
):

    """
    Read CSV or Excel files using Pandas.

    The resulting dataframe becomes the
    currently active dataframe.

    A profile is also generated for
    AI-based analysis.
    """

    try:

        filename_lower = (
            filename.lower()
        )


        # ----------------------------------------------------
        # CSV
        # ----------------------------------------------------

        if filename_lower.endswith(
            '.csv'
        ):

            df = pd.read_csv(
                io.BytesIO(data)
            )


        # ----------------------------------------------------
        # EXCEL
        # ----------------------------------------------------

        elif filename_lower.endswith(
            (
                '.xlsx',
                '.xls'
            )
        ):

            df = pd.read_excel(
                io.BytesIO(data)
            )


        # ----------------------------------------------------
        # UNSUPPORTED FILE
        # ----------------------------------------------------

        else:

            return None


        # ----------------------------------------------------
        # STORE CURRENT DATAFRAME
        # ----------------------------------------------------

        set_dataframe(
            df
        )


        # ----------------------------------------------------
        # PROFILE DATA
        # ----------------------------------------------------

        profile = profile_dataframe(
            df
        )


        quality = profile[
            "quality"
        ]


        # ----------------------------------------------------
        # CREATE DATASET DESCRIPTION
        # ----------------------------------------------------

        dataset_text = (

            f"\n\nDataset: {filename}\n"

            f"Rows: "
            f"{profile['rows']}\n"

            f"Columns: "
            f"{profile['columns']}\n"

            f"Column names: "
            f"{profile['column_names']}\n\n"

            f"Data types:\n"
            f"{profile['data_types']}\n\n"

            f"Missing values:\n"
            f"{profile['missing_values']}\n\n"

            f"Unique values:\n"
            f"{profile['unique_values']}\n\n"

            f"Data Quality Report:\n"

            f"Duplicate rows: "
            f"{quality['duplicate_rows']}\n"

            f"Total missing values: "
            f"{quality['total_missing_values']}\n"

            f"Empty columns: "
            f"{quality['empty_columns']}\n\n"

            f"Numeric summary:\n"
            f"{profile['numeric_summary']}\n\n"

            f"Raw data:\n"
            f"{df.to_string(index=False)}\n"

        )


        return dataset_text


    except Exception as e:

        raise ValueError(
            f"Could not read "
            f"{filename}: {str(e)}"
        )


# ============================================================
# ANALYZE ENDPOINT
# ============================================================

@app.route(
    '/analyze',
    methods=['POST']
)
def analyze():

    # --------------------------------------------------------
    # REQUEST DATA
    # --------------------------------------------------------

    uploaded_files = request.files

    user_question = (
        request.form
        .get(
            'prompt',
            ''
        )
        .strip()
    )


    # --------------------------------------------------------
    # TEXT FOR AI FALLBACK
    # --------------------------------------------------------

    statement_text = user_question


    if statement_text:

        statement_text += "\n"


    # --------------------------------------------------------
    # IMAGE STORAGE
    # --------------------------------------------------------

    images_b64 = []


    # ========================================================
    # PROCESS UPLOADED FILES
    # ========================================================

    for filename, file_storage in (
        uploaded_files.items()
    ):

        if not filename:

            continue


        extension = (
            filename.lower()
        )


        data = (
            file_storage.read()
        )


        # ====================================================
        # TXT / MARKDOWN
        # ====================================================

        if extension.endswith(
            (
                '.txt',
                '.md'
            )
        ):

            try:

                statement_text += (

                    data.decode(
                        'utf-8',
                        errors='ignore'
                    )

                    + "\n"

                )


            except Exception as e:

                return jsonify({

                    "error":
                        f"Could not read "
                        f"{filename}: {str(e)}"

                }), 400


        # ====================================================
        # IMAGES
        # ====================================================

        elif extension.endswith(
            (
                '.png',
                '.jpg',
                '.jpeg',
                '.gif'
            )
        ):

            try:

                image_format = (
                    extension
                    .split('.')[-1]
                )


                b64_str = (
                    base64
                    .b64encode(data)
                    .decode('utf-8')
                )


                images_b64.append(

                    f"data:image/"
                    f"{image_format};base64,"
                    f"{b64_str}"

                )


            except Exception as e:

                return jsonify({

                    "error":
                        f"Could not process "
                        f"{filename}: {str(e)}"

                }), 400


        # ====================================================
        # CSV / EXCEL
        # ====================================================

        elif extension.endswith(
            (
                '.csv',
                '.xlsx',
                '.xls'
            )
        ):

            try:

                dataset_text = (
                    analyze_uploaded_file(
                        filename,
                        data
                    )
                )


                if dataset_text:

                    statement_text += (
                        dataset_text
                    )


            except ValueError as e:

                return jsonify({

                    "error":
                        str(e)

                }), 400


    # ========================================================
    # ADD IMAGES
    # ========================================================

    if images_b64:

        statement_text += (

            "\n\nAttached Images:\n"

            + "\n".join(
                images_b64
            )

        )


    # ========================================================
    # VALIDATE REQUEST
    # ========================================================

    if not statement_text.strip():

        return jsonify({

            "error":
                "Please enter an analysis "
                "question or upload a file."

        }), 400


    print(
        "\n========================================"
    )

    print(
        "Question received by backend:"
    )

    print(
        user_question
    )

    print(
        "========================================"
    )


    # ========================================================
    # PRIMARY OUTPUT
    # ========================================================

    output = None


    # ========================================================
    # DETERMINISTIC PANDAS ANALYSIS
    # ========================================================

    try:

        # IMPORTANT:
        #
        # Only the actual user question is sent
        # to the deterministic analysis engine.
        #
        # The dataset profile is NOT sent here.
        #
        # This prevents words such as "average"
        # or "maximum" inside the dataset profile
        # from confusing the parser.

        calculation = analyze_question(
            user_question
        )


        if calculation:

            print(
                "\nPandas analysis result:"
            )

            print(
                calculation
            )


            operation = (
                calculation[
                    "operation"
                ]
            )


            result = (
                calculation[
                    "result"
                ]
            )


            column = (
                calculation.get(
                    "column"
                )
            )


            # =================================================
            # GROUP SUM
            # =================================================

            if operation == "group_sum":

                output = (

                    f"Total "
                    f"{calculation['value_column']} "
                    f"by "
                    f"{calculation['group_column']}:\n"

                )


                for group, value in (
                    result.items()
                ):

                    output += (

                        f"{group}: "
                        f"{value:,.0f}\n"

                    )


                # ---------------------------------------------
                # CREATE FULL GROUP CHART
                # ---------------------------------------------

                chart_path = (
                    create_bar_chart(
                        get_dataframe(),
                        calculation[
                            "group_column"
                        ],
                        calculation[
                            "value_column"
                        ]
                    )
                )


                output += (
                    f"\nChart: "
                    f"{chart_path}"
                )


            # =================================================
            # TOP N GROUPS
            # =================================================

            elif operation == "top_groups":

                output = (

                    f"Top "
                    f"{calculation['n']} "
                    f"{calculation['group_column']} "
                    f"by "
                    f"{calculation['value_column']}:\n"

                )


                for group, value in (
                    result.items()
                ):

                    output += (

                        f"{group}: "
                        f"{value:,.0f}\n"

                    )


                # ---------------------------------------------
                # CREATE TOP-N CHART
                # ---------------------------------------------

                chart_path = (
                    create_bar_chart(
                        get_dataframe(),
                        calculation[
                            "group_column"
                        ],
                        calculation[
                            "value_column"
                        ],
                        limit=calculation[
                            "n"
                        ]
                    )
                )


                output += (
                    f"\nChart: "
                    f"{chart_path}"
                )


            # =================================================
            # GROUP AVERAGE
            # =================================================

            elif operation == "group_average":

                output = (

                    f"Average "
                    f"{calculation['value_column']} "
                    f"by "
                    f"{calculation['group_column']}:\n"

                )


                for group, value in (
                    result.items()
                ):

                    output += (

                        f"{group}: "
                        f"{value:,.2f}\n"

                    )


            # =================================================
            # HIGHEST GROUP
            # =================================================

            elif operation == "highest_group":

                group_column = (
                    calculation[
                        "group_column"
                    ]
                )


                value_column = (
                    calculation[
                        "value_column"
                    ]
                )


                group = (
                    calculation[
                        "group"
                    ]
                )


                output = (

                    f"Highest "
                    f"{value_column}: "
                    f"{group} — "
                    f"{result:,.0f}"

                )


            # =================================================
            # TOTAL
            # =================================================

            elif operation == "total":

                output = (

                    f"Total "
                    f"{column}: "
                    f"{result:,.0f}"

                )


            # =================================================
            # AVERAGE
            # =================================================

            elif operation == "average":

                output = (

                    f"Average "
                    f"{column}: "
                    f"{result:,.2f}"

                )


            # =================================================
            # MINIMUM
            # =================================================

            elif operation == "minimum":

                output = (

                    f"Minimum "
                    f"{column}: "
                    f"{result:,.0f}"

                )


            # =================================================
            # MAXIMUM
            # =================================================

            elif operation == "maximum":

                output = (

                    f"Maximum "
                    f"{column}: "
                    f"{result:,.0f}"

                )


            # =================================================
            # ROW COUNT
            # =================================================

            elif operation == "row_count":

                output = (

                    f"Total Rows: "
                    f"{result:,}"

                )


            # =================================================
            # UNIQUE COUNT
            # =================================================

            elif operation == "unique_count":

                output = (

                    f"Unique "
                    f"{column} values: "
                    f"{result:,}"

                )


            # =================================================
            # UNKNOWN OPERATION
            # =================================================

            else:

                output = str(
                    result
                )


    except Exception as e:

        print(
            f"Analysis engine failed: {e}"
        )


    # ========================================================
    # GROQ FALLBACK
    # ========================================================

    if not output:

        try:

            print(
                "\nSending request to Groq..."
            )


            output = Groq.run(
                statement_text
            )


            print(
                "Groq request completed."
            )


        except Exception as e:

            print(
                f"Groq failed: {e}"
            )


    # ========================================================
    # LANGCHAIN FALLBACK
    # ========================================================

    if not output:

        try:

            print(
                "Trying fallback LangChain agent..."
            )


            output = ask_agent(
                statement_text
            )


        except Exception as e:

            print(
                f"Fallback agent failed: {e}"
            )


            return jsonify({

                "error":
                    "Both the primary AI model "
                    "and fallback agent failed.",

                "details":
                    str(e)

            }), 500


    # ========================================================
    # RETURN RESULT DIRECTLY
    # ========================================================
    #
    # IMPORTANT:
    #
    # Do NOT send deterministic Pandas results
    # through formatter.py.
    #
    # Otherwise an LLM may turn:
    #
    #     Total Sales: 205,000
    #
    # into:
    #
    #     205000
    #
    # or change the wording/numbers.
    #
    # Pandas already calculated the answer,
    # so return it directly.
    # ========================================================

    return output


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == '__main__':

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )