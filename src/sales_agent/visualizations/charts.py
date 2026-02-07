"""Visualization module for creating charts and plots."""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, List, Union


# Set seaborn style for better-looking plots
sns.set_style("whitegrid")
sns.set_palette("husl")


def create_box_plot(
    df: pd.DataFrame,
    column: str,
    group_by: Optional[str] = None,
    title: Optional[str] = None,
    save_path: Optional[str] = None
) -> str:
    """
    Create a box plot for distribution analysis.
    
    Args:
        df: Input DataFrame
        column: Column to plot
        group_by: Optional column to group by
        title: Plot title
        save_path: Path to save the plot
        
    Returns:
        Path to saved plot
    """
    plt.figure(figsize=(10, 6))
    
    if group_by:
        sns.boxplot(data=df, x=group_by, y=column)
        plt.xticks(rotation=45, ha='right')
    else:
        sns.boxplot(data=df, y=column)
    
    plt.title(title or f'Box Plot: {column}')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Box plot saved: {save_path}")
        return save_path
    else:
        plt.show()
        return "displayed"


def create_scatter_plot(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    hue: Optional[str] = None,
    title: Optional[str] = None,
    save_path: Optional[str] = None
) -> str:
    """
    Create a scatter plot for correlation visualization.
    
    Args:
        df: Input DataFrame
        x_column: Column for x-axis
        y_column: Column for y-axis
        hue: Optional column for color coding
        title: Plot title
        save_path: Path to save the plot
        
    Returns:
        Path to saved plot
    """
    plt.figure(figsize=(10, 6))
    
    sns.scatterplot(data=df, x=x_column, y=y_column, hue=hue, s=100, alpha=0.6)
    
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(title or f'{y_column} vs {x_column}')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Scatter plot saved: {save_path}")
        return save_path
    else:
        plt.show()
        return "displayed"


def create_bar_chart(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    horizontal: bool = False,
    title: Optional[str] = None,
    save_path: Optional[str] = None
) -> str:
    """
    Create a bar chart for categorical comparisons.
    
    Args:
        df: Input DataFrame
        x_column: Column for categories (x-axis)
        y_column: Column for values (y-axis)
        horizontal: If True, create horizontal bar chart
        title: Plot title
        save_path: Path to save the plot
        
    Returns:
        Path to saved plot
    """
    plt.figure(figsize=(12, 6))
    
    if horizontal:
        sns.barplot(data=df, y=x_column, x=y_column, orient='h')
    else:
        sns.barplot(data=df, x=x_column, y=y_column)
        plt.xticks(rotation=45, ha='right')
    
    plt.xlabel(y_column if horizontal else x_column)
    plt.ylabel(x_column if horizontal else y_column)
    plt.title(title or f'{y_column} by {x_column}')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Bar chart saved: {save_path}")
        return save_path
    else:
        plt.show()
        return "displayed"


def create_pie_chart(
    df: pd.DataFrame,
    labels_column: str,
    values_column: str,
    title: Optional[str] = None,
    save_path: Optional[str] = None
) -> str:
    """
    Create a pie chart for proportion visualization.
    
    Args:
        df: Input DataFrame
        labels_column: Column for pie slice labels
        values_column: Column for slice values
        title: Plot title
        save_path: Path to save the plot
        
    Returns:
        Path to saved plot
    """
    plt.figure(figsize=(10, 8))
    
    # Aggregate data
    if len(df) > 10:
        # Take top 9 and group rest as "Others"
        df_sorted = df.nlargest(9, values_column)
        others_value = df[~df.index.isin(df_sorted.index)][values_column].sum()
        
        labels = df_sorted[labels_column].tolist() + ['Others']
        values = df_sorted[values_column].tolist() + [others_value]
    else:
        labels = df[labels_column].tolist()
        values = df[values_column].tolist()
    
    plt.pie(
        values,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette('husl', len(labels))
    )
    
    plt.title(title or f'{values_column} Distribution')
    plt.axis('equal')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Pie chart saved: {save_path}")
        return save_path
    else:
        plt.show()
        return "displayed"


def create_line_chart(
    df: pd.DataFrame,
    x_column: str,
    y_column: Union[str, List[str]],
    title: Optional[str] = None,
    save_path: Optional[str] = None
) -> str:
    """
    Create a line chart for time series or trend visualization.
    
    Args:
        df: Input DataFrame
        x_column: Column for x-axis (usually time/date)
        y_column: Column(s) for y-axis (can be list for multiple lines)
        title: Plot title
        save_path: Path to save the plot
        
    Returns:
        Path to saved plot
    """
    plt.figure(figsize=(12, 6))
    
    if isinstance(y_column, list):
        for col in y_column:
            plt.plot(df[x_column], df[col], marker='o', label=col, linewidth=2)
        plt.legend()
    else:
        plt.plot(df[x_column], df[y_column], marker='o', linewidth=2, markersize=6)
    
    plt.xlabel(x_column)
    plt.ylabel(y_column if isinstance(y_column, str) else 'Values')
    plt.title(title or f'{y_column} over {x_column}')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Line chart saved: {save_path}")
        return save_path
    else:
        plt.show()
        return "displayed"


def create_heatmap(
    df: pd.DataFrame,
    title: Optional[str] = None,
    save_path: Optional[str] = None
) -> str:
    """
    Create a heatmap (usually for correlation matrix).
    
    Args:
        df: Input DataFrame (correlation matrix or pivot table)
        title: Plot title
        save_path: Path to save the plot
        
    Returns:
        Path to saved plot
    """
    plt.figure(figsize=(10, 8))
    
    sns.heatmap(
        df,
        annot=True,
        fmt='.2f',
        cmap='coolwarm',
        center=0,
        linewidths=0.5,
        cbar_kws={'label': 'Correlation'}
    )
    
    plt.title(title or 'Correlation Heatmap')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Heatmap saved: {save_path}")
        return save_path
    else:
        plt.show()
        return "displayed"


if __name__ == "__main__":
    # Test with sample data
    np.random.seed(42)
    test_df = pd.DataFrame({
        'Category': ['A', 'B', 'C', 'D', 'E'] * 20,
        'Values': np.random.randint(100, 1000, 100),
        'Scores': np.random.randint(50, 100, 100)
    })
    
    print("📊 Visualization module ready!")
    print("Available functions:")
    print("  - create_box_plot()")
    print("  - create_scatter_plot()")
    print("  - create_bar_chart()")
    print("  - create_pie_chart()")
    print("  - create_line_chart()")
    print("  - create_heatmap()")
