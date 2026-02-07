import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, Optional

def unsafe_operations_check(code: str) -> bool:
    """
    Basic check for unsafe operations in generated code.
    Allowed: pandas, numpy, math operations, plotting.
    Blocked: system calls, file deletions, network requests.
    """
    unsafe_keywords = [
        "os.", "sys.", "subprocess.", "eval(", "exec(", 
        "open(", "import os", "import sys", "shutil", 
        "requests.", "urllib.", "input("
    ]
    
    for keyword in unsafe_keywords:
        if keyword in code:
            print(f"🚫 Secrity Alert: Code contains unsafe keyword '{keyword}'")
            return False
    return True

def execute_pandas_code(df: pd.DataFrame, code: str) -> Dict[str, Any]:
    """
    Execute generated Pandas code in a controlled environment.
    
    Args:
        df: The pandas DataFrame to operate on (variable name 'df')
        code: The python code string to execute
        
    Returns:
        Dictionary containing results (text, dataframe, plot path)
    """
    if not unsafe_operations_check(code):
        return {"success": False, "error": "Unsafe code detected"}
        
    # Local variables for execution
    local_vars = {
        "df": df,
        "pd": pd,
        "np": np,
        "plt": plt,
        "sns": sns,
        "result": None
    }
    
    try:
        # Execute the code
        exec(code, {}, local_vars)
        
        # Capture result
        result = local_vars.get("result")
        
        return {
            "success": True,
            "result": result,
            "modified_df": local_vars.get("df") # In case df was modified
        }
        
    except Exception as e:
        return {
            "success": False, 
            "error": str(e)
        }
