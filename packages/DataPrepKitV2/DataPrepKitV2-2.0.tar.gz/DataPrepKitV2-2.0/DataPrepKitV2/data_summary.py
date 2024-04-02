import pandas as pd
from typing import Union


def summary(
    data: pd.DataFrame,
    percentile: list = None,
    include: {"all", list, None} = None,
    exclude: {list, None} = None,
) -> Union[pd.Series,pd.DataFrame]:
    """
    Generate descriptive statistics.

    Descriptive statistics include those that summarize the central tendency, dispersion and shape of a dataset’s distribution, excluding NaN values.

    Analyzes both numeric and object series, as well as DataFrame column sets of mixed data types. The output will vary depending on what is provided. Refer to the notes below for more detail.

    Parameters:
    percentiles
    list-like of numbers, optional
    The percentiles to include in the output. All should fall between 0 and 1. The default is [.25, .5, .75], which returns the 25th, 50th, and 75th percentiles.

    include
    ‘all’, list-like of dtypes or None (default), optional
    A white list of data types to include in the result. Ignored for Series. Here are the options:

    ‘all’ : All columns of the input will be included in the output.

    A list-like of dtypes : Limits the results to the provided data types. To limit the result to numeric types submit numpy.number. To limit it instead to object columns submit the numpy.object data type. Strings can also be used in the style of select_dtypes (e.g. df.describe(include=['O'])). To select pandas categorical columns, use 'category'

    None (default) : The result will include all numeric columns.

    exclude
    list-like of dtypes or None (default), optional,
    A black list of data types to omit from the result. Ignored for Series. Here are the options:

    A list-like of dtypes : Excludes the provided data types from the result. To exclude numeric types submit numpy.number. To exclude object columns submit the data type numpy.object. Strings can also be used in the style of select_dtypes (e.g. df.describe(exclude=['O'])). To exclude pandas categorical columns, use 'category'

    None (default) : The result will exclude nothing.

    Returns:
    Series or DataFrame
    Summary statistics of the Series or Dataframe provided.
    """
    try:
        return data.describe(percentiles=percentile, include=include, exclude=exclude)
    except Exception as e:
        print(f"Error: {e}")


def count(
    data: pd.DataFrame, axis: {0, 1} = 0, numeric_only: bool = False
) -> pd.Series:
    """
    Count non-NA cells for each column or row.

    The values None, NaN, NaT, pandas.NA are considered NA.

    Parameters:
    axis
    {0 or ‘index’, 1 or ‘columns’}, default 0
    If 0 or ‘index’ counts are generated for each column. If 1 or ‘columns’ counts are generated for each row.

    numeric_only
    bool, default False
    Include only float, int or boolean data.

    Returns:
    Series
    For each column/row the number of non-NA/null entries.
    """
    try:
        return data.count(axis=axis, numeric_only=numeric_only)
    except Exception as e:
        print(f"Error: {e}")


def mean(
    data: pd.DataFrame,
    axis: {0, 1} = 0,
    skipna: bool = True,
    numeric_only: bool = False,
) -> Union[pd.Series, int, float]:
    """
    Return the mean of the values over the requested axis.

    Parameters:
    axis{index (0), columns (1)}
    Axis for the function to be applied on. For Series this parameter is unused and defaults to 0.

    For DataFrames, specifying axis=None will apply the aggregation across both axes.

    New in version 2.0.0.

    skipnabool, default True
    Exclude NA/null values when computing the result.

    numeric_onlybool, default False
    Include only float, int, boolean columns. Not implemented for Series.

    Returns:
    Series or scalar
    """
    try:
        return data.mean(axis=axis, skipna=skipna, numeric_only=numeric_only)
    except Exception as e:
        print(f"Error: {e}")


def median(
    data: pd.DataFrame,
    axis: {0, 1} = 0,
    skipna: bool = True,
    numeric_only: bool = False,
) -> Union[pd.Series, int, float]:
    """
    Return the median of the values over the requested axis.

    Parameters:
    axis{index (0), columns (1)}
    Axis for the function to be applied on. For Series this parameter is unused and defaults to 0.

    For DataFrames, specifying axis=None will apply the aggregation across both axes.

    New in version 2.0.0.

    skipnabool, default True
    Exclude NA/null values when computing the result.

    numeric_onlybool, default False
    Include only float, int, boolean columns. Not implemented for Series.

    Returns:
    Series or scalar
    """
    try:
        return data.median(axis=axis, skipna=skipna, numeric_only=numeric_only)
    except Exception as e:
        print(f"Error: {e}")


def mode(
    data: pd.DataFrame,
    axis: {0, 1} = 0,
    numeric_only: bool = False,
    dropna: bool = True,
) -> pd.DataFrame:
    """
    Get the mode(s) of each element along the selected axis.

    The mode of a set of values is the value that appears most often. It can be multiple values.

    Parameters
    :
    axis
    {0 or ‘index’, 1 or ‘columns’}, default 0
    The axis to iterate over while searching for the mode:

    0 or ‘index’ : get mode of each column

    1 or ‘columns’ : get mode of each row.

    numeric_only
    bool, default False
    If True, only apply to numeric columns.

    dropna
    bool, default True
    Don’t consider counts of NaN/NaT.

    Returns
    :
    DataFrame
    The modes of each column or row.
    """
    try:
        return data.mode(axis=axis, numeric_only=numeric_only, dropna=dropna)
    except Exception as e:
        print(f"Error: {e}")
