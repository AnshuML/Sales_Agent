"""
Multi-Agent Sales Analysis System
==================================

A conversational multi-agent system for sales data analysis.

Features:
- Retrieves data from Google Drive or local files
- Calculates insights like quarter sales
- Creates visualizations
- Writes results back to Excel files

Usage:
    python main.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sales_agent.agents.orchestrator import OrchestratorAgent
from sales_agent.utils.config import validate_config


def print_welcome():
    """Print welcome message."""
    print("\n" + "="*70)
    print("  📊 MULTI-AGENT SALES ANALYSIS SYSTEM")
    print("="*70)
    print("\n🤖 Powered by hybrid LLM + function-based intelligence")
    print("💡 I can help you analyze sales data, calculate metrics,")
    print("   and create visualizations!\n")


def print_help():
    """Print help information."""
    print("\n📖 **Example Queries:**")
    print("  • 'Show me this quarter's sales (Nov, Dec, Jan)'")
    print("  • 'Calculate total revenue'")
    print("  • 'Create a bar chart of top products'")
    print("  • 'Add a profit margin column'")
    print("\n💡 **Commands:**")
    print("  • 'help' - Show this help message")
    print("  • 'new' - Start a new conversation")
    print("  • 'exit' or 'quit' - Exit the program\n")


def main():
    """Main CLI interface."""
    try:
        # Validate configuration
        validate_config()
    except ValueError as e:
        print(f"\n❌ Configuration Error:\n{e}\n")
        print("Please create a .env file based on .env.example")
        print("and add your GOOGLE_API_KEY")
        return
    
    print_welcome()
    print_help()
    
    orchestrator = None
    
    while True:
        try:
            # Get user input
            if orchestrator is None:
                print("\n" + "-"*70)
                user_input = input("\n🎯 What would you like to analyze? ").strip()
            else:
                user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye! Thanks for using the Multi-Agent Sales Analysis System!\n")
                break
            
            elif user_input.lower() == 'help':
                print_help()
                continue
            
            elif user_input.lower() == 'new':
                orchestrator = None
                print("\n✨ Starting new conversation...")
                continue
            
            # Process with orchestrator
            if orchestrator is None:
                # Start new conversation
                orchestrator = OrchestratorAgent()
                response = orchestrator.start_conversation(user_input)
            else:
                # Continue existing conversation
                response = orchestrator.process_user_response(user_input)
            
            # Display response
            print(f"\n🤖 Assistant:\n{response}")
            
            # Check if conversation is complete
            if orchestrator and orchestrator.is_complete():
                print("\n" + "="*70)
                print("✅ **Analysis Complete!**")
                print("="*70)
                
                summary = orchestrator.get_conversation_summary()
                if summary.get('output_file'):
                    print(f"\n📄 Output file: {summary['output_file']}")
                    print("\nYou can now:")
                    print("  1. Download the file")
                    print("  2. Open it to see the results")
                    print("  3. Start a 'new' conversation for more analysis")
                
                # Reset for new conversation
                orchestrator = None
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Type 'exit' to quit or continue chatting.")
            continue
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Type 'new' to start over or 'help' for assistance.")


if __name__ == "__main__":
    main()
