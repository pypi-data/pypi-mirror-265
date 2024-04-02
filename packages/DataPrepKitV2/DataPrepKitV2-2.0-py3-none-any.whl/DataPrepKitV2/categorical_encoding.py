import pandas as pd


def one_hot_encoding(data: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    """
    Convert categorical variable into dummy/indicator variables.

    Each variable is converted in as many 0/1 variables as there are different values. Columns in the output are each named after a value; if the input is a DataFrame, the name of the original variable is prepended to the value.

    Parameters:
    data:
    array-like, Series, or DataFrame
    Data of which to one hot encoding.
    columns:
    list-like, default None
    Column names in the DataFrame to be encoded. If columns is None then all the columns with object, string, or category dtype will be converted.

    Returns:
    DataFrame
    Dummy-coded data. If data contains other columns than the dummy-coded one(s), these will be prepended, unaltered, to the result.
    """
    try:
        return pd.get_dummies(data, columns=columns)
    except Exception as e:
        print(f"Error: {e}")


def label_encoding(data: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    """
    Performs label encoding on categorical columns of a Pandas DataFrame.

    Parameters:
    data: a DataFrame
    Data of which to get the label encoding.
    columns:
    list-like, default None (optional)
    is a list of column names to encode. If not provided (None by default), the function will encode all categorical columns in the DataFrame.

    Returns:
    a Pandas DataFrame after performing label encoding.
    """
    if columns is None:
        categorical_cols = data.select_dtypes(include=["object", "category"]).columns
    else:
        categorical_cols = columns

    for col in categorical_cols:
        data[col] = data[col].astype("category").cat.codes

    try:
        return data
    except Exception as e:
        print(f"Error: {e}")
