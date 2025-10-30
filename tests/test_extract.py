import requests
from utils import extract
import pandas as pd
from unittest.mock import Mock, patch

sample_html = """
<div class="collection-card">
    <div style="position: relative;">
        <img src="https://picsum.photos/280/350?random=1" class="collection-image" alt="Unknown Product">
    </div>
    <div class="product-details">
        <h3 class="product-title">T-Shirt A</h3>
        <div class="price-container"><span class="price">$12</span></div>
        <p style="font-size: 14px; color: #777;">Rating: ⭐ 4.8 / 5</p>
        <p style="font-size: 14px; color: #777;">3 Colors</p>
        <p style="font-size: 14px; color: #777;">Size: M</p>
        <p style="font-size: 14px; color: #777;">Gender: Unisex</p>
    </div>
</div>
"""

@patch("requests.Session.get")
def test_scrape_page(mock_get):
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.text = sample_html
    mock_get.return_value = mock_resp

    df = extract.scrape_page(requests.Session(), page=1)

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert df.iloc[0]["Title"] == "T-Shirt A"
    assert df.iloc[0]["Price"] == "$12"
