"""User input forms for the correlation analysis."""

import streamlit as st


def user_inputs_corr_matrix(dvc_step_key: str, columns: list[str]) -> tuple[bool, list[str]]:
    """Display the user inputs form and return the submitted values for correlation matrix.

    Args:
        dvc_step_key (str): The key for the DVC step.
        columns (list[str]): The list of column names.

    Returns:
        tuple[bool, list[str]]: A tuple containing a boolean value indicating whether the form was submitted
        and a list of selected features for the correlation matrix.
    """
    st.subheader("Correlation matrix (𝜙k  coefficient).")
    form = st.form(key=f"corr_matrix_form_{dvc_step_key}", border=False)
    with form:
        options = sorted(columns)
        corr_matrix_fields = st.multiselect(
            "Select the features of interest:",
            options=options,
            default=[],
            key=f"y_corr_cols_{dvc_step_key}",
        )

    # submit the form
    submitted = form.form_submit_button(label="Execute")

    return submitted, corr_matrix_fields


def user_input_corr_table(dvc_step_key: str, columns: list[str]) -> tuple[bool, str]:
    """Display the user inputs form and return the submitted values for correlation table.

    Args:
    - dvc_step_key (str): The key for the DVC step.
    - columns (list[str]): The list of column names.

    Returns:
    - tuple[bool, str]: A tuple containing a boolean value indicating whether the form was submitted and the user-selected feature for the correlation table.
    """
    st.subheader("Ranked correlation table for input feature (Pearson  coefficient and Mutual Information).")
    form = st.form(key=f"corr_table_form_{dvc_step_key}", border=False)
    with form:
        options = sorted(columns)
        selected_feature = st.selectbox(
            "Select a feature to explore its correlation coefficients with all other variables.",
            options=options,
            index=0,
            key=f"y_corr_col_{dvc_step_key}",
        )

    # submit the form
    submitted = form.form_submit_button(label="Execute")

    return submitted, selected_feature
