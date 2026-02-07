"""Conversation state management for multi-agent orchestration."""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ConversationState:
    """Tracks the state of the conversation across agents."""
    
    # User query
    original_query: str = ""
    parsed_intent: str = ""
    
    # Data source information
    data_source: Optional[str] = None  # 'google_drive', 's3', 'local'
    data_path: Optional[str] = None    # URL, path, or file ID
    downloaded_file_path: Optional[str] = None
    
    # Data processing
    dataframe_loaded: bool = False
    analysis_complete: bool = False
    
    # Results
    results: Dict[str, Any] = field(default_factory=dict)
    output_file_path: Optional[str] = None
    
    # Conversation history
    messages: List[Dict[str, str]] = field(default_factory=list)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def add_message(self, role: str, content: str):
        """Add a message to conversation history."""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self.updated_at = datetime.now()
    
    def set_data_source(self, source: str, path: str):
        """Set data source information."""
        self.data_source = source
        self.data_path = path
        self.updated_at = datetime.now()
    
    def set_downloaded_file(self, file_path: str):
        """Record downloaded file path."""
        self.downloaded_file_path = file_path
        self.dataframe_loaded = True
        self.updated_at = datetime.now()
    
    def set_results(self, results: Dict[str, Any]):
        """Store analysis results."""
        self.results = results
        self.analysis_complete = True
        self.updated_at = datetime.now()
    
    def set_output_file(self, file_path: str):
        """Record output file path."""
        self.output_file_path = file_path
        self.updated_at = datetime.now()
    
    def is_complete(self) -> bool:
        """Check if conversation is complete."""
        return (
            self.dataframe_loaded and
            self.analysis_complete and
            self.output_file_path is not None
        )
    
    def get_summary(self) -> Dict[str, Any]:
        """Get conversation summary."""
        return {
            "query": self.original_query,
            "data_source": self.data_source,
            "data_loaded": self.dataframe_loaded,
            "analysis_complete": self.analysis_complete,
            "output_file": self.output_file_path,
            "messages_count": len(self.messages),
        }
