#!/usr/bin/env python3
import os
import shutil

def cleanup_python_cache():
    """Remove all .pyc files and __pycache__ directories"""
    for root, dirs, files in os.walk('.'):
        # Remove .pyc files
        for file in files:
            if file.endswith('.pyc'):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Removed: {file_path}")
                except OSError as e:
                    print(f"Error removing {file_path}: {e}")
        
        # Remove __pycache__ directories
        for dir_name in dirs[:]:  # Use slice to avoid modifying list while iterating
            if dir_name == '__pycache__':
                dir_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(dir_path)
                    print(f"Removed directory: {dir_path}")
                    dirs.remove(dir_name)  # Remove from dirs list to avoid walking into it
                except OSError as e:
                    print(f"Error removing directory {dir_path}: {e}")

if __name__ == "__main__":
    print("Cleaning up Python cache files...")
    cleanup_python_cache()
    print("Cleanup completed!")