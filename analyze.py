
import sys
import os
from pathlib import Path

# Add src to path so we can import the sales_agent package
sys.path.insert(0, str(Path(__file__).parent / "src"))

if __name__ == "__main__":
    try:
        # Run the analysis agent module
        import runpy
        runpy.run_module("sales_agent.agents.analysis_agent", run_name="__main__", alter_sys=True)
    except ImportError as e:
        print(f"❌ Error starting agent: {e}")
        print("Please ensure you are in the project root directory.")
    except Exception as e:
        print(f"❌ Error: {e}")
