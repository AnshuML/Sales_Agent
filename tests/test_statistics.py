"""Tests for statistics module."""

import pytest
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from sales_agent.functions.statistics import (
    calculate_quarter_sales,
    add_quarter_sales_column,
    calculate_growth_rate,
)


@pytest.fixture
def sample_sales_data():
    """Create sample sales data with dates."""
    return pd.DataFrame({
        'Date': pd.to_datetime([
            '2024-11-10', '2024-11-20', '2024-12-05', 
            '2024-12-15', '2025-01-10', '2025-01-20'
        ]),
        'Sales': [1000, 1500, 2000, 2500, 1800, 2200]
    })


def test_calculate_quarter_sales(sample_sales_data):
    """Test quarter sales calculation."""
    total = calculate_quarter_sales(
        sample_sales_data,
        'Sales',
        'Date',
        [11, 12, 1]  # Nov, Dec, Jan
    )
    expected = 1000 + 1500 + 2000 + 2500 + 1800 + 2200  # 11,000
    assert total == expected


def test_add_quarter_sales_column(sample_sales_data):
    """Test adding quarter sales column."""
    df_with_quarter = add_quarter_sales_column(
        sample_sales_data.copy(),
        'Sales',
        'Date',
        [11, 12, 1],
        'Q4_Sales'
    )
    assert 'Q4_Sales' in df_with_quarter.columns
    assert df_with_quarter['Q4_Sales'].iloc[0] == 11000


def test_calculate_growth_rate():
    """Test growth rate calculation."""
    growth = calculate_growth_rate(1000, 1200)
    assert growth == 20.0
    
    decline = calculate_growth_rate(1200, 1000)
    assert decline == pytest.approx(-16.67, abs=0.01)


if __name__ == "__main__":
    pytest.main([__file__])
