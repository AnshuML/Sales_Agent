"""Google Drive integration for downloading sales data files."""

import io
import os
import re
from pathlib import Path
from typing import Optional
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import pickle


# If modifying these scopes, delete the file token.pickle
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


class GoogleDriveClient:
    """Client for interacting with Google Drive API."""
    
    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize Google Drive client.
        
        Args:
            credentials_path: Path to credentials.json file
        """
        self.credentials_path = credentials_path or 'credentials/credentials.json'
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Drive API."""
        creds = None
        token_path = 'credentials/token.pickle'
        
        # Load saved credentials if they exist
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, let user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"❌ Credentials file not found: {self.credentials_path}\n"
                        "Please download credentials.json from Google Cloud Console"
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            Path(token_path).parent.mkdir(exist_ok=True)
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('drive', 'v3', credentials=creds)
        print("✅ Authenticated with Google Drive")
    
    def extract_file_id(self, url_or_id: str) -> str:
        """
        Extract file ID from Google Drive URL or return ID if already provided.
        
        Args:
            url_or_id: Google Drive URL or file ID
            
        Returns:
            File ID
            
        Example URLs:
            - https://drive.google.com/file/d/1xABC.../edit
            - https://docs.google.com/spreadsheets/d/1xABC.../edit
        """
        # If it's already just an ID (no slashes), return it
        if '/' not in url_or_id:
            return url_or_id
        
        # Extract ID from URL
        patterns = [
            r'/d/([a-zA-Z0-9-_]+)',  # /d/FILE_ID
            r'id=([a-zA-Z0-9-_]+)',  # id=FILE_ID
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url_or_id)
            if match:
                return match.group(1)
        
        raise ValueError(f"Could not extract file ID from: {url_or_id}")
    
    def download_file(
        self,
        file_id_or_url: str,
        output_dir: str = 'temp_downloads',
        filename: Optional[str] = None
    ) -> str:
        """
        Download file from Google Drive.
        
        Args:
            file_id_or_url: Google Drive file ID or URL
            output_dir: Directory to save the file
            filename: Optional custom filename (otherwise uses Drive filename)
            
        Returns:
            Path to downloaded file
        """
        file_id = self.extract_file_id(file_id_or_url)
        
        # Get file metadata
        file_metadata = self.service.files().get(
            fileId=file_id,
            fields='name, mimeType'
        ).execute()
        
        file_name = filename or file_metadata['name']
        mime_type = file_metadata['mimeType']
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Handle Google Sheets (export as Excel)
        if 'spreadsheet' in mime_type:
            file_name = file_name if file_name.endswith('.xlsx') else f"{file_name}.xlsx"
            request = self.service.files().export_media(
                fileId=file_id,
                mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        else:
            # Regular file download
            request = self.service.files().get_media(fileId=file_id)
        
        # Download file
        output_file = output_path / file_name
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                print(f"⬇️  Download {int(status.progress() * 100)}%")
        
        # Write to file
        with open(output_file, 'wb') as f:
            f.write(fh.getvalue())
        
        print(f"✅ Downloaded: {file_name} ({len(fh.getvalue()) / 1024:.1f} KB)")
        
        return str(output_file)
    
    def list_files(self, query: Optional[str] = None, max_results: int = 10) -> list:
        """
        List files in Google Drive.
        
        Args:
            query: Search query (e.g., "name contains 'sales'")
            max_results: Maximum number of results
            
        Returns:
            List of file dictionaries with 'id', 'name', 'mimeType'
        """
        results = self.service.files().list(
            q=query,
            pageSize=max_results,
            fields="files(id, name, mimeType, modifiedTime)"
        ).execute()
        
        files = results.get('files', [])
        
        if files:
            print(f"📂 Found {len(files)} files:")
            for f in files:
                print(f"  - {f['name']} ({f['id']})")
        else:
            print("📂 No files found")
        
        return files


def download_from_drive(
    url_or_id: str,
    credentials_path: Optional[str] = None,
    output_dir: str = 'temp_downloads'
) -> str:
    """
    Convenience function to download a file from Google Drive.
    
    Args:
        url_or_id: Google Drive URL or file ID
        credentials_path: Path to credentials.json
        output_dir: Output directory
        
    Returns:
        Path to downloaded file
    """
    client = GoogleDriveClient(credentials_path)
    return client.download_file(url_or_id, output_dir)


if __name__ == "__main__":
    # Test the client
    print("🧪 Testing Google Drive Client")
    print("\nNote: You need credentials.json in the credentials/ folder")
    print("Get it from: https://console.cloud.google.com/apis/credentials")
