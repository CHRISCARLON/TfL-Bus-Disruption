import pandas as pd
import numpy as np
import streamlit as st


@st.cache_data
def read_parquet_and_ensure_list(file_path,
                                 column_name='lineStrings'):
    """
    Reads a Parquet file into a DataFrame and ensures that the specified column contains lists,
    while keeping all other columns intact.

    The lambda function turns the lineStrings column values from arrays to lists - this is because
    parquet files serialise lists of lists into individual arrays.

    :param file_path: The file path of the Parquet file
    :param column_name: The column to check and convert to lists if necessary
    :return: A pandas DataFrame with the specified column containing lists and all other columns unchanged
    """

    # Read the Parquet file
    df = pd.read_parquet(file_path)

    if column_name in df.columns:
        # Apply transformation to the specified column
        df[column_name] = df[column_name].apply(
            lambda x: [tuple(coord) for coord in x] if isinstance(x, np.ndarray) else x)
        return df
    else:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame.")


@st.cache_data
def merge_excel_with_df(df, excel_file_path, merge_column='id',
                        additional_column='sm_weighted_disruption_score'):
    """
    Merges an Excel file with final the street work disruption scores
    using the bus 'id' column.

    :param df: The existing DataFrame
    :param excel_file_path: The file path of the Excel file
    :param merge_column: The column to use for merging, defaults to 'id'
    :param additional_column: The additional column to pull over from the Excel file
    :return: A merged DataFrame
    """
    # Read the Excel file
    excel_df = pd.read_excel(excel_file_path)

    # Check if the merge column exists in both DataFrames
    if merge_column not in df.columns or merge_column not in excel_df.columns:
        raise ValueError(f"Merge column '{merge_column}' not found in one of the DataFrames.")

    # Check if the additional column exists in the Excel DataFrame
    if additional_column not in excel_df.columns:
        raise ValueError(f"Additional column '{additional_column}' not found in the Excel DataFrame.")

    # Merge the DataFrames on the specified column
    merged_df = pd.merge(df, excel_df[[merge_column, additional_column]], on=merge_column, how='left')

    print("Merge Complete")

    return merged_df
