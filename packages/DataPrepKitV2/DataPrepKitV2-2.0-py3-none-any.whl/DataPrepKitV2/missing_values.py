import pandas as pd
from typing import Union


def remove_missing(
    data: pd.DataFrame,
    axis: {0, 1} = 0,
    how: {"all", "any"} = "any",
    subset: list = None,
    inplace: bool = False,
) -> Union[pd.DataFrame, None]:
    """
    Remove missing values.
    axis: {0 or ‘index’, 1 or ‘columns’}, default 0
    Determine if rows or columns which contain missing values are removed.

    0, or ‘index’ : Drop rows which contain missing values.

    1, or ‘columns’ : Drop columns which contain missing value.

    Only a single axis is allowed.

    how: {‘any’, ‘all’}, default ‘any’
    Determine if row or column is removed from DataFrame, when we have at least one NA or all NA.

    ‘any’ : If any NA values are present, drop that row or column.

    ‘all’ : If all values are NA, drop that row or column.

    subset: column label or sequence of labels, optional
    Labels along other axis to consider, e.g. if you are dropping rows these would be a list of columns to include.

    inplace: bool, default False
    Whether to modify the DataFrame rather than creating a new one.

    Returns:
    DataFrame or None
    DataFrame with NA entries dropped from it or None if inplace=True.
    """
    
    try:
        return data.dropna(
            axis=axis,
            how=how,
            subset=subset,
            inplace=inplace,
        )
    except Exception as e:
        print(f"Error: {e}")


def impute_missing(
    data: pd.DataFrame,
    strategy: {"mean", "median", "value"},
    value: {int, float, str, dict, pd.Series, pd.DataFrame} = None,
    axis: {0, 1} = 0,
    inplace: bool = False,
) -> Union[pd.DataFrame, pd.Series, None]:
    """
    Fill NA/NaN values using the specified method

    value: scalar, dict, Series, or DataFrame
    Value to use to fill holes (e.g. 0), alternately a dict/Series/DataFrame of values specifying which value to use for each index (for a Series) or column (for a DataFrame). Values not in the dict/Series/DataFrame will not be filled. This value cannot be a list.
    
    axis: {0 or ‘index’} for Series, {0 or ‘index’, 1 or ‘columns’} for DataFrame
    Axis along which to fill missing values. For Series this parameter is unused and defaults to 0.

    inplace: bool, default False
    If True, fill in-place. Note: this will modify any other views on this object (e.g., a no-copy slice for a column in a DataFrame).

    Returns:
    Series/DataFrame or None
    Object with missing values filled or None if inplace=True.
    """
    if strategy == "mean":
        return data.fillna(data.mean(), axis=axis, inplace=inplace)
    elif strategy == "median":
        return data.fillna(data.median(), axis=axis, inplace=inplace)
    elif strategy == "value":
        return data.fillna(value=value, axis=axis, inplace=inplace)
