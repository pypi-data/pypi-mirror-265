"""A module containing some util functions to clean the data for input into the rca function"""

import pandas as pd
from typing import Optional, Union


def filter_df_based_on_dict(
    df_to_filter: pd.DataFrame, filter_dict: dict
) -> pd.DataFrame:
    df = df_to_filter.copy()
    for filter_column, values_to_filter in filter_dict.items():
        df = df[df[filter_column].isin(values_to_filter)]
    return df.reset_index(drop=True)


def subset_df(df_to_subset: pd.DataFrame, column_list: list[str]) -> pd.DataFrame:
    df = df_to_subset.copy()
    return df[column_list].reset_index(drop=True)


def multiply_column_value(
    df: pd.DataFrame, column_to_multiply: str, factor: Union[float, int]
) -> pd.DataFrame:
    df_to_alter = df.copy()
    df_to_alter[column_to_multiply] = df_to_alter[column_to_multiply] * factor
    return df_to_alter


def create_mapping_dictionary_from_df(
    df: pd.DataFrame, key_column: str, value_column: str
):
    df_to_map = df.copy().dropna()
    return dict(zip(df_to_map[key_column], df_to_map[value_column]))


def map_new_column(
    df: pd.DataFrame,
    mapping_dict: dict,  # dependencies must come first
    column_to_map: str,
    new_column_name: Optional[str] = None,
    drop_na: Optional[bool] = True,
) -> pd.DataFrame:
    if new_column_name is None:
        new_column_name = column_to_map
    df_to_map = df.copy()
    df_to_map[new_column_name] = df_to_map[column_to_map].map(mapping_dict)
    if drop_na:
        return df_to_map.dropna().reset_index(drop=True)
    return df_to_map


def map_multiple_columns(df: pd.DataFrame, mapping_dict: dict) -> pd.DataFrame:
    df_to_map = df.copy()
    for column, column_mapping in mapping_dict.items():
        df_to_map = map_new_column(df_to_map, column, column_mapping)
    return df_to_map


def rename_columns(df, renaming_dict) -> pd.DataFrame:
    df_to_rename = df.copy()
    return df_to_rename.rename(columns=renaming_dict)


def melt_frame(df):
    pass


def drop_columns(
    df: pd.DataFrame, column_to_drop: Union[str, list[str]]
) -> pd.DataFrame:
    df_to_alter = df.copy()
    df_to_alter.drop(columns=column_to_drop, inplace=True)
    return df_to_alter
