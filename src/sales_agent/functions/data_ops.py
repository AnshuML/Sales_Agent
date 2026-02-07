"""Data operations module for reading, filtering, and manipulating sales data."""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union, List, Dict, Any, Optional


def read_sales_data(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Read sales data from various file formats.
    
    Args:
        file_path: Path to the data file (CSV, Excel, JSON)
        
    Returns:
        DataFrame containing the sales data
        
    Raises:
        ValueError: If file format is not supported
        FileNotFoundError: If file doesn't exist
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    suffix = file_path.suffix.lower()
    
    try:
        if suffix == '.csv':
            df = pd.read_csv(file_path)
        elif suffix in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif suffix == '.json':
            df = pd.read_json(file_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
        
        print(f"✅ Loaded {len(df)} rows from {file_path.name}")
        return df
        
    except Exception as e:
        raise ValueError(f"Error reading file {file_path}: {str(e)}")


def filter_data(
    df: pd.DataFrame,
    conditions: Dict[str, Any]
) -> pd.DataFrame:
    """
    Filter DataFrame based on conditions.
    
    Args:
        df: Input DataFrame
        conditions: Dictionary of column:value pairs for filtering
        
    Returns:
        Filtered DataFrame
        
    Example:
        filter_data(df, {'Region': 'North', 'Product': 'Laptop'})
    """
    filtered_df = df.copy()
    
    for column, value in conditions.items():
        if column not in df.columns:
            print(f"⚠️  Column '{column}' not found, skipping")
            continue
        
        if isinstance(value, list):
            filtered_df = filtered_df[filtered_df[column].isin(value)]
        else:
            filtered_df = filtered_df[filtered_df[column] == value]
    
    print(f"✅ Filtered to {len(filtered_df)} rows (from {len(df)})")
    return filtered_df


def group_and_aggregate(
    df: pd.DataFrame,
    group_by: Union[str, List[str]],
    agg_dict: Dict[str, Union[str, List[str]]]
) -> pd.DataFrame:
    """
    Group data and apply aggregations.
    
    Args:
        df: Input DataFrame
        group_by: Column(s) to group by
        agg_dict: Dictionary of column:aggregation_function pairs
        
    Returns:
        Grouped and aggregated DataFrame
        
    Example:
        group_and_aggregate(df, 'Product', {'Sales': 'sum', 'Quantity': 'mean'})
    """
    grouped = df.groupby(group_by).agg(agg_dict).reset_index()
    
    # Flatten multi-level column names if any
    if isinstance(grouped.columns, pd.MultiIndex):
        grouped.columns = ['_'.join(col).strip('_') for col in grouped.columns.values]
    
    print(f"✅ Grouped by {group_by}, resulting in {len(grouped)} groups")
    return grouped


def pivot_data(
    df: pd.DataFrame,
    index: str,
    columns: str,
    values: str,
    aggfunc: str = 'sum'
) -> pd.DataFrame:
    """
    Create a pivot table from the data.
    
    Args:
        df: Input DataFrame
        index: Column to use as row index
        columns: Column to use as column headers
        values: Column to aggregate
        aggfunc: Aggregation function (default: 'sum')
        
    Returns:
        Pivot table DataFrame
    """
    pivot = pd.pivot_table(
        df,
        index=index,
        columns=columns,
        values=values,
        aggfunc=aggfunc,
        fill_value=0
    )
    
    print(f"✅ Created pivot table with shape {pivot.shape}")
    return pivot


def merge_datasets(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    on: Union[str, List[str]],
    how: str = 'inner'
) -> pd.DataFrame:
    """
    Merge two datasets.
    
    Args:
        df1: First DataFrame
        df2: Second DataFrame
        on: Column(s) to join on
        how: Type of join ('inner', 'outer', 'left', 'right')
        
    Returns:
        Merged DataFrame
    """
    merged = pd.merge(df1, df2, on=on, how=how)
    print(f"✅ Merged datasets: {len(merged)} rows")
    return merged


def calculate_insights(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Auto-generate key insights from sales data.
    
    Args:
        df: Sales DataFrame
        
    Returns:
        Dictionary of insights
    """
    insights = {}
    
    # Try to identify common column names
    sales_cols = [col for col in df.columns if 'sales' in col.lower() or 'revenue' in col.lower()]
    quantity_cols = [col for col in df.columns if 'quantity' in col.lower() or 'qty' in col.lower()]
    date_cols = [col for col in df.columns if 'date' in col.lower()]
    
    if sales_cols:
        sales_col = sales_cols[0]
        insights['total_sales'] = df[sales_col].sum()
        insights['average_sales'] = df[sales_col].mean()
        insights['max_sales'] = df[sales_col].max()
        insights['min_sales'] = df[sales_col].min()
    
    if quantity_cols:
        qty_col = quantity_cols[0]
        insights['total_quantity'] = df[qty_col].sum()
        insights['average_quantity'] = df[qty_col].mean()
    
    insights['total_records'] = len(df)
    insights['columns'] = list(df.columns)
    
    return insights


def get_top_n(
    df: pd.DataFrame,
    column: str,
    n: int = 10,
    ascending: bool = False
) -> pd.DataFrame:
    """
    Get top N rows by a specific column.
    
    Args:
        df: Input DataFrame
        column: Column to sort by
        n: Number of top rows to return
        ascending: Sort ascending (default: False for top values)
        
    Returns:
        Top N rows
    """
    return df.nlargest(n, column) if not ascending else df.nsmallest(n, column)
