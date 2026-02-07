"""Statistical analysis and period calculations for sales data."""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import calendar


def calculate_quarter_sales(
    df: pd.DataFrame,
    sales_column: str,
    date_column: str,
    months: List[int]
) -> float:
    """
    Calculate total sales for specific months (e.g., quarter).
    
    Args:
        df: Sales DataFrame
        sales_column: Name of the sales/revenue column
        date_column: Name of the date column
        months: List of month numbers (e.g., [11, 12, 1] for Nov, Dec, Jan)
        
    Returns:
        Total sales for specified months
        
    Example:
        calculate_quarter_sales(df, 'Sales', 'Date', [11, 12, 1])
    """
    # Ensure date column is datetime
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        df[date_column] = pd.to_datetime(df[date_column])
    
    # Ensure sales column is numeric
    df = df.copy()  # Avoid SettingWithCopyWarning
    df[sales_column] = pd.to_numeric(df[sales_column], errors='coerce').fillna(0)
    
    # Ensure sales column is numeric
    df = df.copy()  # Avoid SettingWithCopyWarning
    df[sales_column] = pd.to_numeric(df[sales_column], errors='coerce').fillna(0)
    
    # Filter by months
    mask = df[date_column].dt.month.isin(months)
    quarter_df = df[mask]
    
    total_sales = quarter_df[sales_column].sum()
    
    month_names = [calendar.month_abbr[m] for m in months]
    print(f"✅ Quarter sales ({', '.join(month_names)}): {total_sales:,.2f}")
    
    return total_sales


def add_quarter_sales_column(
    df: pd.DataFrame,
    sales_column: str,
    date_column: str,
    months: List[int],
    new_column_name: str = 'Quarter_Sales'
) -> pd.DataFrame:
    """
    Add a column with quarter sales for each row.
    
    Args:
        df: Sales DataFrame
        sales_column: Name of the sales/revenue column
        date_column: Name of the date column
        months: List of month numbers for the quarter
        new_column_name: Name for the new column
        
    Returns:
        DataFrame with new quarter sales column
    """
    df_copy = df.copy()
    
    # Ensure date column is datetime
    if not pd.api.types.is_datetime64_any_dtype(df_copy[date_column]):
        df_copy[date_column] = pd.to_datetime(df_copy[date_column])
    
    # Calculate total quarter sales
    quarter_total = calculate_quarter_sales(df_copy, sales_column, date_column, months)
    
    # Add as a new column (same value for all rows)
    df_copy[new_column_name] = quarter_total
    
    print(f"✅ Added column '{new_column_name}' with value: {quarter_total:,.2f}")
    
    return df_copy


def calculate_period_aggregation(
    df: pd.DataFrame,
    date_column: str,
    value_column: str,
    period: str = 'M'
) -> pd.DataFrame:
    """
    Aggregate data by time period (daily, weekly, monthly, quarterly, yearly).
    
    Args:
        df: Input DataFrame
        date_column: Name of the date column
        value_column: Column to aggregate
        period: Period code ('D'=daily, 'W'=weekly, 'M'=monthly, 'Q'=quarterly, 'Y'=yearly)
        
    Returns:
        Aggregated DataFrame by period
    """
    df_copy = df.copy()
    
    if not pd.api.types.is_datetime64_any_dtype(df_copy[date_column]):
        df_copy[date_column] = pd.to_datetime(df_copy[date_column])
    
    df_copy = df_copy.set_index(date_column)
    aggregated = df_copy[value_column].resample(period).sum().reset_index()
    
    period_names = {'D': 'Daily', 'W': 'Weekly', 'M': 'Monthly', 'Q': 'Quarterly', 'Y': 'Yearly'}
    print(f"✅ {period_names.get(period, period)} aggregation complete: {len(aggregated)} periods")
    
    return aggregated


def calculate_growth_rate(
    df: pd.DataFrame,
    value_column: str,
    date_column: str,
    period: str = 'M'
) -> pd.DataFrame:
    """
    Calculate growth rates (MoM, QoQ, YoY).
    
    Args:
        df: Input DataFrame with time series data
        value_column: Column to calculate growth for
        date_column: Date column
        period: 'M' for MoM, 'Q' for QoQ, 'Y' for YoY
        
    Returns:
        DataFrame with growth rate column added
    """
    df_copy = df.copy()
    
    if not pd.api.types.is_datetime64_any_dtype(df_copy[date_column]):
        df_copy[date_column] = pd.to_datetime(df_copy[date_column])
    
    df_copy = df_copy.sort_values(date_column)
    
    # Calculate percentage change
    df_copy[f'{value_column}_Growth_%'] = df_copy[value_column].pct_change() * 100
    
    growth_type = {'M': 'MoM', 'Q': 'QoQ', 'Y': 'YoY'}
    print(f"✅ {growth_type.get(period, 'Growth')} rate calculated")
    
    return df_copy


def calculate_descriptive_stats(
    df: pd.DataFrame,
    column: str
) -> Dict[str, float]:
    """
    Calculate descriptive statistics for a column.
    
    Args:
        df: Input DataFrame
        column: Column to analyze
        
    Returns:
        Dictionary of statistics
    """
    stats = {
        'mean': df[column].mean(),
        'median': df[column].median(),
        'mode': df[column].mode()[0] if not df[column].mode().empty else None,
        'std_dev': df[column].std(),
        'min': df[column].min(),
        'max': df[column].max(),
        'Q1': df[column].quantile(0.25),
        'Q3': df[column].quantile(0.75),
        'IQR': df[column].quantile(0.75) - df[column].quantile(0.25),
    }
    
    return stats


def calculate_moving_average(
    df: pd.DataFrame,
    column: str,
    window: int = 3
) -> pd.DataFrame:
    """
    Calculate moving average.
    
    Args:
        df: Input DataFrame
        column: Column to calculate moving average for
        window: Window size (default: 3)
        
    Returns:
        DataFrame with moving average column
    """
    df_copy = df.copy()
    df_copy[f'{column}_MA_{window}'] = df_copy[column].rolling(window=window).mean()
    
    print(f"✅ {window}-period moving average calculated for '{column}'")
    
    return df_copy


def detect_outliers(
    df: pd.DataFrame,
    column: str,
    method: str = 'iqr'
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Detect outliers using IQR or Z-score method.
    
    Args:
        df: Input DataFrame
        column: Column to check for outliers
        method: 'iqr' or 'zscore'
        
    Returns:
        Tuple of (outliers DataFrame, clean DataFrame)
    """
    if method == 'iqr':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        clean = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
        
    elif method == 'zscore':
        from scipy import stats
        z_scores = np.abs(stats.zscore(df[column]))
        threshold = 3
        
        outliers = df[z_scores > threshold]
        clean = df[z_scores <= threshold]
    
    else:
        raise ValueError("Method must be 'iqr' or 'zscore'")
    
    print(f"✅ Detected {len(outliers)} outliers using {method.upper()} method")
    
    return outliers, clean


def calculate_correlation(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Calculate correlation matrix for numeric columns.
    
    Args:
        df: Input DataFrame
        columns: List of columns to include (default: all numeric)
        
    Returns:
        Correlation matrix
    """
    if columns:
        corr_matrix = df[columns].corr()
    else:
        corr_matrix = df.select_dtypes(include=[np.number]).corr()
    
    print(f"✅ Correlation matrix calculated for {len(corr_matrix.columns)} columns")
    
    return corr_matrix
