import pandas as pd
import pytest
from .data_summary import summary, count, mean, median, mode


@pytest.fixture
def sample_dataframe():
    data = {
        "A": [1, 2, 3, 4, 5],
        "B": [10, 20, 30, 40, 50],
        "C": [100, 200, 300, 400, 500],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_series():
    data = [1, 2, 3, 4, 5]
    return pd.Series(data)


def test_summary_dataframe(sample_dataframe):
    result = summary(sample_dataframe)
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (8, 3)


def test_summary_series(sample_series):
    result = summary(sample_series)
    assert isinstance(result, pd.Series)
    assert result.shape == (8,)


def test_count(sample_dataframe):
    result = count(sample_dataframe)
    assert isinstance(result, pd.Series)
    assert result.dtype == "int64"
    assert result.tolist() == [5, 5, 5]


def test_count_axis(sample_dataframe):
    result = count(sample_dataframe, axis=1)
    assert isinstance(result, pd.Series)
    assert result.dtype == "int64"
    assert result.tolist() == [3, 3, 3, 3, 3]


def test_mean(sample_dataframe):
    result = mean(sample_dataframe)
    assert isinstance(result, pd.Series)
    assert result.dtype == "float64"
    assert result.tolist() == [3.0, 30.0, 300.0]


def test_median(sample_dataframe):
    result = median(sample_dataframe)
    assert isinstance(result, pd.Series)
    assert result.dtype == "float64"
    assert result.tolist() == [3.0, 30.0, 300.0]


def test_mode(sample_dataframe):
    result = mode(sample_dataframe)
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (5, 3)
