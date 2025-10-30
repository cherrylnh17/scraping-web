import pandas as pd
from utils import transform

def sample_raw_df():
    return pd.DataFrame([
        {
            "Title": "T-Shirt A",
            "Price": "$10",
            "Rating": "4.5 / 5",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Unisex",
            "timestamp": "2025-01-01T00:00:00"
        },
        {
            "Title": "Unknown Product",
            "Price": "$5",
            "Rating": "Invalid Rating",
            "Colors": "Red,Blue",
            "Size": "Size: L",
            "Gender": "Gender: Men",
            "timestamp": "2025-01-01T00:00:00"
        },
        {
            "Title": "Jacket B",
            "Price": "Price Unavailable",
            "Rating": "4",
            "Colors": "2",
            "Size": "M",
            "Gender": "Women",
            "timestamp": "2025-01-01T00:00:00"
        },
    ])

def test_transform_basic():
    df = sample_raw_df()
    out = transform.transform(df)
    assert not out.empty
    assert "T-Shirt A" in out["Title"].values
    assert out.iloc[0]["Price"] == 10 * 16000
    assert isinstance(out.iloc[0]["Rating"], float)
    assert int(out.iloc[0]["Colors"]) == 3
    assert out.iloc[0]["Size"] == "M"
    assert out.iloc[0]["Gender"] == "Unisex"
