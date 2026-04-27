import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from src.data_loader import load_country_data

def test_load_country_data():
    """Test that data loading works correctly."""
    # Create a sample dataframe to simulate CSV
    sample_data = {
        'YEAR': [2015, 2015, 2015],
        'DOY': [1, 2, 3],
        'T2M': [20.0, -999, 22.0],
        'T2M_MAX': [25.0, 26.0, 27.0],
        'T2M_MIN': [15.0, 16.0, 17.0],
        'T2M_RANGE': [10.0, 10.0, 10.0],
        'PRECTOTCORR': [0.0, 5.0, 0.0],
        'RH2M': [60.0, 65.0, 70.0],
        'WS2M': [2.0, 2.5, 3.0],
        'WS2M_MAX': [4.0, 5.0, 6.0],
        'PS': [77.0, 77.1, 77.2],
        'QV2M': [8.0, 9.0, 10.0]
    }
    df = pd.DataFrame(sample_data)
    df.to_csv('/tmp/test_country.csv', index=False)
    result = load_country_data('/tmp/test_country.csv', 'TestCountry')
    assert result['Country'].iloc[0] == 'TestCountry'
    assert result['T2M'].isna().sum() == 1
    assert 'Date' in result.columns
    assert 'Month' in result.columns
    print("✅ test_load_country_data passed!")

if __name__ == "__main__":
    test_load_country_data()
