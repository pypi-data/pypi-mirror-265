import pandas as pd
import pytest
from .categorical_encoding import one_hot_encoding, label_encoding


@pytest.fixture
def sample_data():
    data = pd.DataFrame(
        {
            "A": ["a", "b", "a", "c"],
            "B": ["x", "y", "z", "x"],
            "C": ["p", "q", "r", "s"],
        }
    )
    return data


# Test one_hot_encoding function
def test_one_hot_encoding(sample_data):

    # Perform one-hot encoding
    encoded_data = one_hot_encoding(sample_data)

    # Check if the encoded_data has the expected columns
    assert "A_a" in encoded_data.columns
    assert "A_b" in encoded_data.columns
    assert "A_c" in encoded_data.columns
    assert "B_x" in encoded_data.columns
    assert "B_y" in encoded_data.columns
    assert "B_z" in encoded_data.columns
    assert "C_p" in encoded_data.columns
    assert "C_q" in encoded_data.columns
    assert "C_r" in encoded_data.columns
    assert "C_s" in encoded_data.columns


# Test one_hot_encoding function while passing certain column names
def test_one_hot_encoding_with_columns(sample_data):

    # Perform one-hot encoding
    encoded_data = one_hot_encoding(sample_data, columns=["A", "B"])

    # Check if the encoded_data has the expected columns
    assert "A_a" in encoded_data.columns
    assert "A_b" in encoded_data.columns
    assert "A_c" in encoded_data.columns
    assert "B_x" in encoded_data.columns
    assert "B_y" in encoded_data.columns
    assert "B_z" in encoded_data.columns
    assert "C" in encoded_data.columns


def test_label_encoding(sample_data,columns=["A", "B", "C"]):

    # Perform label encoding
    encoded_data = label_encoding(sample_data)

    # Check if the encoded_data has the expected values
    assert encoded_data["A"].tolist() == [0, 1, 0, 2]
    assert encoded_data["B"].tolist() == [0, 1, 2, 0]
    assert encoded_data["C"].tolist() == [0, 1, 2, 3]
