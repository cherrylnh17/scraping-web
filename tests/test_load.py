import pandas as pd
from utils import load
import os

def test_save_csv(tmp_path):
    df = pd.DataFrame({"A": [1,2,3]})
    path = tmp_path / "out.csv"
    res = load.save_csv(df, path=str(path))
    assert os.path.exists(res)
    df2 = pd.read_csv(res)
    assert df2.shape == df.shape
