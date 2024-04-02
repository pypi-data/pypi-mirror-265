import pandas as pd
import pytest
from .missing_values import remove_missing, impute_missing


@pytest.fixture
def sample_dataframe():
    data = {
        "A": [1, 2, None, 4, 19],
        "B": [None, 6, 7, 8, 18],
        "C": [9, 10, 11, None, 17],
        "D": [12, 13, 14, 15, 16],
    }
    return pd.DataFrame(data)


# Test remove_missing function
def test_remove_missing(sample_dataframe):

    # Call the remove_missing function
    result = remove_missing(sample_dataframe)
    assert isinstance(result, pd.DataFrame)
    # Check if the missing values are removed
    assert result.isnull().sum().sum() == 0


# Test remove_missing function with axis=0, streategy = "mean", how = "any", inplace = False
def test_impute_missing(sample_dataframe):
    # Call the impute_missing function with mean strategy
    result = impute_missing(sample_dataframe, strategy="mean")
    assert isinstance(result, pd.DataFrame)
    # check if the missing values are imputed with the mean value
    assert result.isnull().sum().sum() == 0
    assert result["A"].mean() == pytest.approx(6.5, abs=0.001)
    assert result["B"].mean() == pytest.approx(9.75, abs=0.001)
    assert result["C"].mean() == pytest.approx(11.75, abs=0.001)
    assert result["D"].mean() == pytest.approx(14, abs=0.001)


# Test remove_missing function with axis=0, streategy = "value", value = 0, inplace = False
def test_impute_missing_value(sample_dataframe):
    # Call the impute_missing function with value strategy
    result = impute_missing(sample_dataframe, strategy="value", value=0)
    assert isinstance(result, pd.DataFrame)
    # check if the missing values are imputed with the specified value
    assert result.isnull().sum().sum() == 0
    assert (result["A"].unique() == [1, 2, 0, 4, 19]).all()
    assert (result["B"].unique() == [0, 6, 7, 8, 18]).all()
    assert (result["C"].unique() == [9, 10, 11, 0, 17]).all()
    assert (result["D"].unique() == [12, 13, 14, 15, 16]).all()


# Test impute_missing function with axis=0, strategy = "median", inplace = False
def test_impute_missing_median(sample_dataframe):
    # Call the impute_missing function with median strategy
    result = impute_missing(sample_dataframe, strategy="median", axis=0, inplace=False)
    assert isinstance(result, pd.DataFrame)
    # Check if the missing values are removed
    assert result.isnull().sum().sum() == 0
    assert result["A"].median() == 3.0
    assert result["B"].median() == 7.5
    assert result["C"].median() == 10.5
    assert result["D"].median() == 14.0

