"""
Multi-Agent Sales Analysis System
==================================

A conversational multi-agent system for intelligent sales data analysis.

Features:
- 🤖 Hybrid LLM (Gemini) + function-based analysis
- 📊 Quarter sales calculation & insights
- 📈 Advanced visualizations
- 💾 Excel read/write with new columns
- 🔄 Google Drive & local file support

Usage:
    from sales_agent.agents.orchestrator import OrchestratorAgent
    
    orchestrator = OrchestratorAgent()
    response = orchestrator.start_conversation("Show me quarter sales")
    
Or use the CLI:
    $ sales-agent
    # or
    $ python -m sales_agent.main
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from sales_agent.agents.orchestrator import OrchestratorAgent
from sales_agent.agents.data_retrieval_agent import DataRetrievalAgent
from sales_agent.agents.analysis_agent import AnalysisAgent

__all__ = [
    "OrchestratorAgent",
    "DataRetrievalAgent",
    "AnalysisAgent",
]
