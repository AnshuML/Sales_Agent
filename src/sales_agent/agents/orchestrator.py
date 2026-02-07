"""Orchestrator Agent - Main coordinator for multi-agent system."""

from typing import Optional
from sales_agent.utils.conversation_state import ConversationState
from sales_agent.agents.data_retrieval_agent import DataRetrievalAgent
from sales_agent.agents.analysis_agent import AnalysisAgent


class OrchestratorAgent:
    """Main orchestrator that coordinates between agents."""
    
    def __init__(self):
        """Initialize the orchestrator with all sub-agents."""
        self.state = None
        self.data_agent = DataRetrievalAgent()
        self.analysis_agent = AnalysisAgent()
        self.current_step = "initial"
    
    def start_conversation(self, user_query: str) -> str:
        """
        Start a new conversation with user query.
        
        Args:
            user_query: User's initial query
            
        Returns:
            Response message
        """
        self.state = ConversationState()
        self.state.original_query = user_query
        self.state.add_message("user", user_query)
        
        print(f"\n{'='*60}")
        print(f"🎯 User Query: {user_query}")
        print(f"{'='*60}\n")
        
        # Check if data is needed
        if self._query_needs_data(user_query):
            self.current_step = "need_data_source"
            response = self.data_agent.ask_for_data_location()
        else:
            response = "I can help with that, but I need more information..."
        
        self.state.add_message("assistant", response)
        return response
    
    def process_user_response(self, user_input: str) -> str:
        """
        Process user's response based on current conversation step.
        
        Args:
            user_input: User's response
            
        Returns:
            Response message
        """
        self.state.add_message("user", user_input)
        
        if self.current_step == "need_data_source":
            return self._handle_data_source_response(user_input)
        
        elif self.current_step == "need_data_path":
            return self._handle_data_path_response(user_input)
        
        elif self.current_step == "ready_for_analysis":
            return self._handle_analysis_query(user_input)
        
        else:
            response = "I'm not sure what to do next. Let's start over."
            self.state.add_message("assistant", response)
            return response
    
    def _query_needs_data(self, query: str) -> bool:
        """Determine if query needs data."""
        # Most sales analysis queries need data
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in [
            'sales', 'revenue', 'data', 'quarter', 'month', 'analyze', 'show', 'calculate'
        ])
    
    def _handle_data_source_response(self, user_input: str) -> str:
        """Handle user's response about data source."""
        data_source = self.data_agent.detect_data_source(user_input)
        
        if data_source:
            self.state.set_data_source(data_source, "")
            self.current_step = "need_data_path"
            
            # If user already provided the path/URL in the same message
            if data_source == 'google_drive' and ('drive.google.com' in user_input or 'docs.google.com' in user_input):
                # Extract URL and skip to path handling
                return self._handle_data_path_response(user_input)
            
            response = self.data_agent.ask_for_path(data_source)
        else:
            response = (
                "❌ I couldn't detect the data source. Please specify:\n"
                "  • Google Drive\n"
                "  • Local file\n"
                "  • S3 bucket"
            )
        
        self.state.add_message("assistant", response)
        return response
    
    def _handle_data_path_response(self, user_input: str) -> str:
        """Handle user's response with file path/URL."""
        data_source = self.state.data_source
        
        if not data_source:
            # Try to detect from input
            data_source = self.data_agent.detect_data_source(user_input)
            if data_source:
                self.state.set_data_source(data_source, user_input)
            else:
                return "❌ Could not detect data source. Please start over."
        
        # Retrieve the data
        success, message, file_path = self.data_agent.retrieve_data(
            data_source,
            user_input,
            self.state
        )
        
        if success:
            # Load data into analysis agent
            if self.analysis_agent.load_data(file_path):
                self.current_step = "ready_for_analysis"
                
                # Automatically analyze based on original query
                analysis_response = self._handle_analysis_query(self.state.original_query)
                
                response = f"{message}\n\n{analysis_response}"
            else:
                response = f"{message}\n\n❌ Failed to load data for analysis."
        else:
            response = message
        
        self.state.add_message("assistant", response)
        return response
    
    def _handle_analysis_query(self, query: str) -> str:
        """Handle analysis query."""
        print(f"\n🔬 Analyzing: {query}")
        
        results = self.analysis_agent.execute_analysis(query)
        
        response = results.get("message", "Analysis complete!")
        
        if results.get("success"):
            self.state.set_results(results.get("data", {}))
            if results.get("data", {}).get("output_file"):
                self.state.set_output_file(results["data"]["output_file"])
        
        return response
    
    def get_conversation_summary(self) -> dict:
        """Get summary of the conversation."""
        return self.state.get_summary() if self.state else {}
    
    def is_complete(self) -> bool:
        """Check if conversation is complete."""
        return self.state.is_complete() if self.state else False


if __name__ == "__main__":
    # Test orchestrator
    orchestrator = OrchestratorAgent()
    print("🤖 Orchestrator Agent initialized")
    
    # Simulate conversation
    response = orchestrator.start_conversation("Show me this quarter's sales")
    print(f"\nAgent: {response}")
