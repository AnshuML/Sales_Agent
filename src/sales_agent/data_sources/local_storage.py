"""Local file system storage handler."""

import shutil
from pathlib import Path
from typing import Union


def get_local_file(file_path: Union[str, Path]) -> str:
    """
    Validate and get local file path.
    
    Args:
        file_path: Path to local file
        
    Returns:
        Absolute path to file
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    
    print(f"✅ Found local file: {file_path.name}")
    
    return str(file_path.absolute())


def copy_to_working_dir(
    file_path: Union[str, Path],
    working_dir: str = 'temp_downloads'
) -> str:
    """
    Copy local file to working directory.
    
    Args:
        file_path: Source file path
        working_dir: Destination directory
        
    Returns:
        Path to copied file
    """
    file_path = Path(file_path)
    dest_dir = Path(working_dir)
    
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    dest_file = dest_dir / file_path.name
    shutil.copy2(file_path, dest_file)
    
    print(f"✅ Copied to working directory: {dest_file.name}")
    
    return str(dest_file)


if __name__ == "__main__":
    print("📁 Local file system handler ready")
