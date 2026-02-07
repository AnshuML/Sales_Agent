"""Data Retrieval Agent - Handles conversational data source detection and file retrieval."""

from typing import Optional, Tuple
from sales_agent.utils.conversation_state import ConversationState
from sales_agent.data_sources.google_drive import GoogleDriveClient
from sales_agent.data_sources.local_storage import get_local_file
from pathlib import Path


class DataRetrievalAgent:
    """Agent responsible for retrieving data from various sources."""
    
    def __init__(self):
        """Initialize the data retrieval agent."""
        self.google_drive_client = None
    
    def detect_data_source(self, user_input: str) -> Optional[str]:
        """
        Detect data source from user input.
        
        Args:
            user_input: User's response about data location
            
        Returns:
            Data source type: 'google_drive', 's3', 'local', or None
        """
        user_input_lower = user_input.lower()
        
        if any(keyword in user_input_lower for keyword in ['drive', 'google', 'gdrive']):
            return 'google_drive'
        elif any(keyword in user_input_lower for keyword in ['s3', 'aws', 'bucket']):
            return 's3'
        elif any(keyword in user_input_lower for keyword in ['local', 'file', 'computer', 'disk']):
            return 'local'
        
        # Check if it's a URL
        if 'drive.google.com' in user_input_lower or 'docs.google.com' in user_input_lower:
            return 'google_drive'
        elif user_input_lower.startswith('s3://'):
            return 's3'
        elif Path(user_input).exists():
            return 'local'
        
        return None
    
    def ask_for_data_location(self) -> str:
        """Get message asking for data location."""
        return (
            "📁 Where is your data stored?\n\n"
            "Options:\n"
            "  1️⃣ Google Drive (share the link)\n"
            "  2️⃣ Local file (provide file path)\n"
            "  3️⃣ S3 bucket (coming soon)\n\n"
            "Please specify:"
        )
    
    def ask_for_path(self, data_source: str) -> str:
        """Get message asking for file path/link."""
        if data_source == 'google_drive':
            return (
                "🔗 Please share your Google Drive file link or ID\n\n"
                "Example: https://docs.google.com/spreadsheets/d/1xABC.../edit"
            )
        elif data_source == 'local':
            return (
                "📂 Please provide the full path to your file\n\n"
                "Example: C:\\Users\\Documents\\sales_data.xlsx"
            )
        elif data_source == 's3':
            return (
                "☁️ Please provide the S3 bucket and key\n\n"
                "Example: s3://my-bucket/sales_data.xlsx"
            )
        else:
            return "Please provide the file path or link"
    
    def retrieve_data(
        self,
        data_source: str,
        path: str,
        state: ConversationState
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Retrieve data from the specified source.
        
        Args:
            data_source: Type of data source
            path: Path, URL, or file ID
            state: Conversation state to update
            
        Returns:
            Tuple of (success: bool, message: str, file_path: Optional[str])
        """
        try:
            if data_source == 'google_drive':
                return self._retrieve_from_google_drive(path, state)
            elif data_source == 'local':
                return self._retrieve_from_local(path, state)
            elif data_source == 's3':
                return False, "❌ S3 integration coming soon!", None
            else:
                return False, f"❌ Unknown data source: {data_source}", None
                
        except Exception as e:
            return False, f"❌ Error retrieving data: {str(e)}", None
    
    def _retrieve_from_google_drive(
        self,
        url_or_id: str,
        state: ConversationState
    ) -> Tuple[bool, str, Optional[str]]:
        """Retrieve file from Google Drive."""
        try:
            print("\n🔐 Initializing Google Drive client...")
            
            if self.google_drive_client is None:
                self.google_drive_client = GoogleDriveClient()
            
            print("⬇️  Downloading file from Google Drive...")
            file_path = self.google_drive_client.download_file(url_or_id)
            
            state.set_downloaded_file(file_path)
            
            return (
                True,
                f"✅ Successfully downloaded file from Google Drive!\n📄 File: {Path(file_path).name}",
                file_path
            )
            
        except FileNotFoundError as e:
            return False, str(e), None
        except Exception as e:
            return False, f"❌ Google Drive error: {str(e)}", None
    
    def _retrieve_from_local(
        self,
        file_path: str,
        state: ConversationState
    ) -> Tuple[bool, str, Optional[str]]:
        """Retrieve local file."""
        try:
            validated_path = get_local_file(file_path)
            state.set_downloaded_file(validated_path)
            
            return (
                True,
                f"✅ Found local file!\n📄 File: {Path(validated_path).name}",
                validated_path
            )
            
        except FileNotFoundError:
            return False, f"❌ File not found: {file_path}", None
        except Exception as e:
            return False, f"❌ Error accessing local file: {str(e)}", None


if __name__ == "__main__":
    # Test the data retrieval agent
    agent = DataRetrievalAgent()
    
    print("🤖 Data Retrieval Agent initialized")
    print(agent.ask_for_data_location())
    
    # Test detection
    test_inputs = [
        "Google Drive",
        "https://drive.google.com/file/d/123/edit",
        "C:\\Users\\data.xlsx",
        "local file"
    ]
    
    for inp in test_inputs:
        source = agent.detect_data_source(inp)
        print(f"\nInput: {inp}")
        print(f"Detected source: {source}")
