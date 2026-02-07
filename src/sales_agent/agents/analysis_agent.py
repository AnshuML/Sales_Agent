"""Analysis Agent - utilizing Dynamic Code Generation for 'Excel Expert' capabilities."""

import pandas as pd
import numpy as np
import re
from typing import Dict, Any, List, Optional
from pathlib import Path

# Config and LLM
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from sales_agent.utils.config import (
    GOOGLE_API_KEY, GROQ_API_KEY, 
    LLM_MODEL, LLM_TEMPERATURE, LLM_PROVIDER
)

# Code Execution (Using local import path)
from sales_agent.utils.code_executor import execute_pandas_code
from sales_agent.functions.data_ops import read_sales_data, calculate_insights

class AnalysisAgent:
    """
    Advanced Sales Analysis Agent.
    
    Instead of hardcoded functions, this agent acts as an 'Excel Expert' 
    by generating and executing Pandas code to solve ANY user query.
    """
    
    def __init__(self):
        """Initialize the analysis agent with LLM."""
        if LLM_PROVIDER == "groq":
            if not GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY is not set.")
            self.llm = ChatGroq(
                model_name=LLM_MODEL,
                groq_api_key=GROQ_API_KEY,
                temperature=0  # Zero temperature for precise code generation
            )
            print(f"Initialized Groq LLM: {LLM_MODEL} (Code Gen Mode)")
            
        else:
            if not GOOGLE_API_KEY:
                raise ValueError("GOOGLE_API_KEY is not set.")
            self.llm = ChatGoogleGenerativeAI(
                model=LLM_MODEL,
                google_api_key=GOOGLE_API_KEY,
                temperature=0
            )
            print(f"Initialized Gemini LLM: {LLM_MODEL} (Code Gen Mode)")
            
        self.df = None
        self.file_path = None
    
    def load_data(self, file_path: str) -> bool:
        """Load data and perform initial auto-analysis."""
        try:
            self.df = read_sales_data(file_path)
            self.file_path = file_path
            print(f"\n Data loaded: {len(self.df)} rows, {len(self.df.columns)} columns")
            
            # Initial proactive insights
            self._proactive_analysis()
            
            return True
        except Exception as e:
            print(f" Error loading data: {e}")
            return False
            
    def _proactive_analysis(self):
        """Automatically detect key trends and stats on load."""
        try:
            insights = calculate_insights(self.df)
            print("\n  **Auto-Discovery:**")
            print(f"   • Total Sales: {insights.get('total_sales', 'N/A'):,.2f}")
            print(f"   • Records: {insights.get('total_records', 0)}")
            print(f"   • Key Columns: {', '.join(insights.get('columns', [])[:5])}...")
        except Exception:
            pass

    def execute_analysis(self, query: str) -> Dict[str, Any]:
        """
        Main entry point:
        1. Understand query -> Generate Python Code
        2. Execute Code -> Get Result
        3. Explain Result -> Return to User
        """
        if self.df is None:
            return {"error": "No data loaded"}

        print(f"\n Thinking about: '{query}'...")
        
        # 1. Generate Code
        code = self._generate_code(query)
        if not code:
            return {"success": False, "message": "Failed to generate analysis code."}
            
        # print(f" Generated Code:\n{'-'*20}\n{code}\n{'-'*20}")
        
        # 2. Execute Code
        exec_result = execute_pandas_code(self.df, code)
        
        if not exec_result["success"]:
            return {
                "success": False, 
                "message": f" Code Execution Failed: {exec_result['error']}"
            }
            
        result_data = exec_result["result"]
        
        # 3. Format/Explain Output
        final_response = self._format_result(query, result_data)
        
        return {
            "success": True,
            "message": final_response,
            "data": result_data
        }

    def _generate_code(self, query: str) -> str:
        """Use LLM to interpret query and write Pandas code."""
        
        # Prepare context (schema info)
        import io
        buffer = io.StringIO()
        self.df.info(buf=buffer)
        schema_info = buffer.getvalue()
        # Handle cases where .info() prints to stdout instead of buffer in older pandas
        if not schema_info: 
             schema_info = str(self.df.dtypes)
             
        head_info = self.df.head(3).to_string()
        
        prompt = f"""
You are an expert Python Data Analyst. 
You have a pandas DataFrame named 'df'.

USER QUERY: "{query}"

DATA SCHEMA:
{schema_info}

SAMPLE DATA:
{head_info}

INSTRUCTIONS:
1. Write Python code to answer the query using 'df'.
2. IMPORTANT: Handle data types! 
   - Convert numeric columns: `pd.to_numeric(df['col'], errors='coerce')`
   - Clean categorical columns: `df['col'] = df['col'].astype(str).str.strip()` to remove whitespace.
3. PRE-PLOTTING CHECK:
   - If grouping by a column, DROP rows where that column is 'nan', 'None', or empty BEFORE plotting.
   - Do NOT plot "Unknown" values unless explicitly asked.
4. Save the final result to a variable named `result`.
   - If the result is a number/text, `result = ...`
   - If the result is a filtered dataframe, `result = filtered_df`
   - If the user asks for a plot/chart:
     - Use `matplotlib.pyplot` or `seaborn`.
     - Save figure to 'temp_downloads/chart.png'.
     - Set `result = "Chart saved to temp_downloads/chart.png"`.
5. Output ONLY the Python code. No markdown, no comments.
"""
        try:
            response = self.llm.invoke(prompt)
            code = response.content.strip()
            # Clean markdown code blocks
            code = re.sub(r'```python', '', code)
            code = re.sub(r'```', '', code)
            return code.strip()
            
        except Exception as e:
            print(f"Error generating code: {e}")
            return None

    def _format_result(self, query: str, result: Any) -> str:
        """Format the raw result into a nice natural language response."""
        
        if isinstance(result, (int, float, np.number)):
             return f"**Result:** {result:,.2f}"
             
        elif isinstance(result, pd.DataFrame):
            # If dataframe is huge, just show head
            if len(result) > 10:
                return f"**Result DataFrame (Top 10 rows):**\n\n{result.head(10).to_string()}"
            return f"**Result DataFrame:**\n\n{result.to_string()}"
            
        elif isinstance(result, str):
            return f"**Result:** {result}"
            
        elif isinstance(result, list):
             return f"**Result:** {', '.join(map(str, result))}"
             
        else:
            return str(result)

if __name__ == "__main__":
    import sys
    import os
    
    print("\n **Advanced Analysis Agent (Standalone Mode)**")
    print("Type 'exit' to quit.")
    
    try:
        agent = AnalysisAgent()
    except Exception as e:
        print(f" Error initializing agent: {e}")
        sys.exit(1)
    
    while True:
        file_path_input = input("\n[File] Enter path to sales data file (e.g., data/Agents.xlsx): ").strip().strip('"').strip("'")
        if not file_path_input:
            continue
            
        if os.path.exists(file_path_input):
            if agent.load_data(file_path_input):
                while True:
                    query = input("\n Query: ").strip()
                    if query.lower() in ['exit', 'quit']:
                        break
                    
                    if not query:
                        continue
                        
                    result = agent.execute_analysis(query)
                    print(f"\n{result['message']}")
                break
        else:
            print(f" [Error] File not found: {file_path_input}")
