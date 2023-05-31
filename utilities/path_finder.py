import os
from pathlib import Path

def get_path_to_file(*args: tuple) -> str:
    """Get the path of the file in the project root directory"""

    if len(args) < 1:
        raise ValueError("At least one argument is required")
    
    if not all([isinstance(item, str) for item in args]):
        raise TypeError("Arguments should be of type `string` only")
    
    parent_directory = Path(__file__).parent.parent
    values = ' '.join(map(str, args))

    return os.path.join(parent_directory, *values.split())
