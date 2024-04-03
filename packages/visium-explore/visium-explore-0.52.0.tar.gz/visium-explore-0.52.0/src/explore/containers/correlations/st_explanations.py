"""Display explanations and warnings for the correlation coefficients using streamlit."""

import pandas as pd
import streamlit as st


def st_correlation_matrix_explanation() -> None:
    """Display the explanation for the 𝜙k correlation coefficient.

    This function displays the explanation for the correlation coefficients using a Streamlit expander.
    The explanation includes details about the 𝜙k correlation coefficient, its suitability for different types of variables,
    and the range of values it can take. It also provides a link to a research paper for further reading.
    """
    with st.expander("See explanations for the correlation coefficients"):
        st.write(
            "- **𝜙k correlation coefficient**: Suitable for all categorical, ordinal and continuous variables. Captures linear and non-linear relationships. The coefficient ranges from 0 to 1, where 0 indicates no association and 1 indicates a perfect association. https://arxiv.org/pdf/1811.11440.pdf"
        )


def st_correlation_matrix_phik_disclaimer() -> None:
    """Display the warnings and explanation for the 𝜙k correlation coefficient.

    This function displays a warning and explanation for the correlation coefficients used in the correlation matrix.
    It provides information about the computation time and potential issues with certain features.
    """
    st.write(
        "- **Warning:** Due to the computational intensity of calculating the 𝜙k correlation coefficient, it's recommended to limit the analysis to approximately 10 features to ensure manageable computation times.."
    )
    st.write(
        "- If one or more features you have selected are not displayed in the correlation matrix this may be due either to the feature having only null values or not enough unique values to compute the 𝜙k correlation coefficient."
    )


def st_correlation_table_explanation() -> None:
    """Display the explanation for the correlation coefficients.

    This function uses Streamlit's `expander` widget to display explanations for the correlation coefficients.
    It provides information about the Pearson correlation coefficient and the Mutual Information coefficient.
    """
    with st.expander("See explanations for the correlation coefficients"):
        st.write(
            "- **Pearson correlation coefficient**: Only suitable for continuous variables. Captures linear relationships. The coefficient ranges from -1 to 1, where -1 indicates a perfect negative linear relationship, 0 indicates no linear relationship, and 1 indicates a perfect positive linear relationship. https://pubmed.ncbi.nlm.nih.gov/29481436/"
        )
        st.write(
            "- **Mutual Information**: Suitable for all categorical, ordinal and continuous variables. Captures linear and non-linear relationships. The coefficient ranges from 0 to an upper bound which is determined by the minimum between the entropy of the target and the entropy of the feature: min[H(x), H(y)]. The higher the value the more the feature can explain about the target. Conversely a value of 0 indicates that the two features are completely independent. In this analysis, mutual information is computed using scikit-learn, with each feature-target pair evaluated independently. This pairwise approach allows for a detailed assessment of the unique relationship each feature has with the target, rather than aggregating all features. Please note that theoretically, mutual information (MI) is commutative, meaning I(X; Y) = I(Y; X). However, in practice, particularly with numerical approximations like those used in scikit-learn, MI may not perfectly follow this property. https://link.springer.com/article/10.1007/s00145-010-9084-8"
        )
