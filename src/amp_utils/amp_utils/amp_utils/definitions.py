#!/usr/bin/env python3
from pathlib import Path

def get_project_root():
    """
    Gets the project root directory, assuming this function is called
    from a file within the project, and that there's a 'pyproject.toml'
    file at the project root.
    """
    current_file = Path(__file__).resolve() # Using resolve to get an absolute path.
    for parent in current_file.parents: # Iterate over every parent.
        if (parent / "pyproject.toml").exists(): # Checks if file exists
            return parent
    raise FileNotFoundError("Project root (with pyproject.toml) not found.")

def get_file_path_from_root(relative_path) -> Path:
    """Gets the absolute path to the project root directory."""
    root = str(get_project_root())
    relative_path = str(relative_path)
    return Path(root + relative_path)