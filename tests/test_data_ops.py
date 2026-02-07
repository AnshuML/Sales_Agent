"""Tests for data operations module."""

import pytest
import pandas as pd
from pathlib import Path
import sys

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from sales_agent.functions.data_ops import (
    read_sales_data,
    filter_data,
    group_and_aggregate,
    calculate_insights,
)


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame({
        'Date': pd.date_range('2024-01-01', periods=10),
        'Product': ['A', 'B', 'C'] * 3 + ['A'],
        'Sales': [100, 200, 150, 300, 250, 180, 220, 190, 280, 210],
        'Quantity': [10, 20, 15, 30, 25, 18, 22, 19, 28, 21]
    })


def test_filter_data(sample_dataframe):
    """Test data filtering."""
    filtered = filter_data(sample_dataframe, {'Product': 'A'})
    assert len(filtered) == 4
    assert all(filtered['Product'] == 'A')


def test_group_and_aggregate(sample_dataframe):
    """Test grouping and aggregation."""
    grouped = group_and_aggregate(
        sample_dataframe,
        'Product',
        {'Sales': 'sum', 'Quantity': 'mean'}
    )
    assert len(grouped) == 3
    assert 'Sales' in grouped.columns
    assert 'Quantity' in grouped.columns


def test_calculate_insights(sample_dataframe):
    """Test insights calculation."""
    insights = calculate_insights(sample_dataframe)
    assert 'total_rows' in insights
    assert 'total_columns' in insights
    assert insights['total_rows'] == 10
    assert insights['total_columns'] == 4


if __name__ == "__main__":
    pytest.main ([__file__])
