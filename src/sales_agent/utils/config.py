"""Configuration management for the multi-agent sales analysis system."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).parent.parent
CREDENTIALS_DIR = BASE_DIR / "credentials"
TEMP_DIR = BASE_DIR / "temp_downloads"

# Ensure directories exist
CREDENTIALS_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GOOGLE_API_KEY and not GROQ_API_KEY:
    print("⚠️  Warning: Neither GOOGLE_API_KEY nor GROQ_API_KEY found in .env file")

# Google Drive settings
GOOGLE_DRIVE_CREDENTIALS_PATH = os.getenv(
    "GOOGLE_DRIVE_CREDENTIALS_PATH",
    str(CREDENTIALS_DIR / "credentials.json")
)

# AWS S3 settings (optional)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

# Application settings
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
TEMP_DOWNLOAD_DIR = os.getenv("TEMP_DOWNLOAD_DIR", str(TEMP_DIR))

# LLM settings
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")  # 'groq' or 'gemini'
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile" if LLM_PROVIDER == "groq" else "gemini-pro")
LLM_TEMPERATURE = 0.1
LLM_MAX_TOKENS = 2048

# Supported file formats
SUPPORTED_FORMATS = [".csv", ".xlsx", ".xls", ".json"]


def validate_config():
    """Validate that required configuration is present."""
    errors = []
    
    if LLM_PROVIDER == "gemini" and not GOOGLE_API_KEY:
        errors.append("GOOGLE_API_KEY is required for Gemini provider")
    elif LLM_PROVIDER == "groq" and not GROQ_API_KEY:
        errors.append("GROQ_API_KEY is required for Groq provider")
    
    if errors:
        raise ValueError(f"Configuration errors:\n" + "\n".join(f"- {e}" for e in errors))
    
    return True


if __name__ == "__main__":
    # Test configuration
    try:
        validate_config()
        print("✅ Configuration is valid!")
        print(f"📁 Base directory: {BASE_DIR}")
        print(f"🤖 LLM Provider: {LLM_PROVIDER}")
        print(f"🔑 Google API Key: {'Set' if GOOGLE_API_KEY else 'Not set'}")
        print(f"🔑 Groq API Key: {'Set' if GROQ_API_KEY else 'Not set'}")
        print(f"🔑 AWS credentials: {'Set' if AWS_ACCESS_KEY_ID else 'Not set'}")
    except ValueError as e:
        print(f"❌ {e}")
