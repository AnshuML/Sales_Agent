"""Data manipulation module for adding columns and writing back to Excel."""

import pandas as pd
from pathlib import Path
from typing import Union, Callable, Any, Optional
import openpyxl


def add_column(
    df: pd.DataFrame,
    column_name: str,
    value: Any = None,
    formula: Optional[Callable] = None
) -> pd.DataFrame:
    """
    Add a new column to the DataFrame.
    
    Args:
        df: Input DataFrame
        column_name: Name of the new column
        value: Static value for all rows (if no formula provided)
        formula: Function to calculate values (receives row as input)
        
    Returns:
        DataFrame with new column
        
    Example:
        add_column(df, 'Profit', formula=lambda row: row['Revenue'] - row['Cost'])
    """
    df_copy = df.copy()
    
    if formula:
        df_copy[column_name] = df_copy.apply(formula, axis=1)
    else:
        df_copy[column_name] = value
    
    print(f"✅ Added column '{column_name}'")
    
    return df_copy


def populate_column(
    df: pd.DataFrame,
    column_name: str,
    values: Union[list, pd.Series, Any]
) -> pd.DataFrame:
    """
    Populate an existing or new column with values.
    
    Args:
        df: Input DataFrame
        column_name: Name of the column
        values: Values to populate (list, Series, or single value)
        
    Returns:
        DataFrame with populated column
    """
    df_copy = df.copy()
    df_copy[column_name] = values
    
    print(f"✅ Populated column '{column_name}'")
    
    return df_copy


def write_to_excel(
    df: pd.DataFrame,
    file_path: Union[str, Path],
    sheet_name: str = 'Sheet1',
    preserve_formatting: bool = True
) -> str:
    """
    Write DataFrame back to Excel file, optionally preserving formatting.
    
    Args:
        df: DataFrame to write
        file_path: Path to output Excel file
        sheet_name: Name of the sheet (default: 'Sheet1')
        preserve_formatting: If True and file exists, preserve formatting
        
    Returns:
        Path to written file
    """
    file_path = Path(file_path)
    
    try:
        if preserve_formatting and file_path.exists():
            # Load existing workbook and update data
            with pd.ExcelWriter(
                file_path,
                mode='a',
                engine='openpyxl',
                if_sheet_exists='replace'
            ) as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            # Create new file
            df.to_excel(file_path, sheet_name=sheet_name, index=False)
        
        print(f"✅ Written {len(df)} rows to '{file_path.name}'")
        return str(file_path)
        
    except Exception as e:
        # Fallback: create new file
        df.to_excel(file_path, sheet_name=sheet_name, index=False)
        print(f"✅ Created new file '{file_path.name}' with {len(df)} rows")
        return str(file_path)


def transform_column(
    df: pd.DataFrame,
    column_name: str,
    transformation: Callable
) -> pd.DataFrame:
    """
    Apply transformation to a column.
    
    Args:
        df: Input DataFrame
        column_name: Column to transform
        transformation: Function to apply
        
    Returns:
        DataFrame with transformed column
        
    Example:
        transform_column(df, 'Price', lambda x: x * 1.1)  # 10% increase
    """
    df_copy = df.copy()
    df_copy[column_name] = df_copy[column_name].apply(transformation)
    
    print(f"✅ Transformed column '{column_name}'")
    
    return df_copy


def create_derived_metrics(
    df: pd.DataFrame,
    revenue_col: str = 'Revenue',
    cost_col: str = 'Cost',
    quantity_col: Optional[str] = None
) -> pd.DataFrame:
    """
    Create common derived metrics (profit margin, unit price, etc.).
    
    Args:
        df: Input DataFrame
        revenue_col: Name of revenue column
        cost_col: Name of cost column
        quantity_col: Name of quantity column (optional)
        
    Returns:
        DataFrame with derived metrics
    """
    df_copy = df.copy()
    
    # Profit
    if revenue_col in df.columns and cost_col in df.columns:
        df_copy['Profit'] = df_copy[revenue_col] - df_copy[cost_col]
        df_copy['Profit_Margin_%'] = (df_copy['Profit'] / df_copy[revenue_col]) * 100
        print("✅ Added 'Profit' and 'Profit_Margin_%'")
    
    # Unit metrics
    if quantity_col and quantity_col in df.columns:
        if revenue_col in df.columns:
            df_copy['Unit_Price'] = df_copy[revenue_col] / df_copy[quantity_col]
            print("✅ Added 'Unit_Price'")
        
        if cost_col in df.columns:
            df_copy['Unit_Cost'] = df_copy[cost_col] / df_copy[quantity_col]
            print("✅ Added 'Unit_Cost'")
    
    return df_copy


def rename_columns(
    df: pd.DataFrame,
    rename_dict: dict
) -> pd.DataFrame:
    """
    Rename columns in DataFrame.
    
    Args:
        df: Input DataFrame
        rename_dict: Dictionary of old_name: new_name
        
    Returns:
        DataFrame with renamed columns
    """
    df_copy = df.copy()
    df_copy = df_copy.rename(columns=rename_dict)
    
    print(f"✅ Renamed {len(rename_dict)} columns")
    
    return df_copy


def drop_columns(
    df: pd.DataFrame,
    columns: Union[str, list]
) -> pd.DataFrame:
    """
    Drop columns from DataFrame.
    
    Args:
        df: Input DataFrame
        columns: Column name or list of column names to drop
        
    Returns:
        DataFrame with columns removed
    """
    df_copy = df.copy()
    
    if isinstance(columns, str):
        columns = [columns]
    
    df_copy = df_copy.drop(columns=columns, errors='ignore')
    
    print(f"✅ Dropped {len(columns)} columns")
    
    return df_copy
