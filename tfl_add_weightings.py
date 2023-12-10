import pandas as pd
import numpy as np


def add_usage_groups(df, usage_column='Usage recorded: 2022/23',
                     group_column='Usage_Group'):
    """
    Adds a new column to the DataFrame categorizing 'Usage recorded: 2022/23' into
    'No Data', 'Low', 'Low-Medium', 'Medium', 'Medium-High', and 'High' groups.

    :param df: DataFrame containing the 'Usage recorded: 2022/23' column
    :param usage_column: Name of the column with usage data
    :param group_column: Name of the new column to be added
    :return: DataFrame with the new group column added
    """
    # Handle missing or invalid data
    df[group_column] = 'No Data'  # Default assignment for all rows

    # Identify rows with valid usage data
    valid_data_indices = df[pd.to_numeric(df[usage_column], errors='coerce').notnull()].index

    # Define the quantiles and labels for valid data
    quantiles = [0, 0.2, 0.4, 0.6, 0.8, 1]  # Six quantiles for five bins
    labels = ['Low', 'Low-Medium', 'Medium', 'Medium-High', 'High']

    # Assign each valid data row to a percentile group
    df.loc[valid_data_indices, group_column] = pd.qcut(df.loc[valid_data_indices, usage_column],
                                                       q=quantiles,
                                                       labels=labels)

    return df


def add_deciles_for_disruption_score(df, score_column='sm_weighted_disruption_score',
                                     group_column='Score_Decile_Group'):
    """
    Adds a new column to the DataFrame categorizing 'sm_weighted_disruption_score' into deciles,
    and handles cases with missing or zero values.

    :param df: DataFrame containing the 'sm_weighted_disruption_score' column
    :param score_column: Name of the column with disruption scores
    :param group_column: Name of the new column to be added for deciles
    :return: DataFrame with the new deciles group column added
    """
    # Initialize the group_column with a default value
    df[group_column] = np.nan

    # Handle missing or zero scores
    df[group_column] = np.where(df[score_column].isna() | (df[score_column] == 0), 'No Data or Zero Impact Level '
                                                                                   'Calculated',
                                df[group_column])

    # Identify rows with valid, non-zero scores
    valid_scores_indices = df[(df[score_column].notna()) & (df[score_column] != 0)].index

    # Create deciles for valid scores
    df.loc[valid_scores_indices, group_column] = pd.qcut(df.loc[valid_scores_indices, score_column],
                                                         q=10,
                                                         labels=[f'Impact Level {i}' for i in range(1, 11)])

    return df
