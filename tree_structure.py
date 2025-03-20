# You can run this in the terminal from CyberGator project root
# using the command: 
#           python tree_structure.py
# This script will generate a tree structure of the project

import os

def tree_structure(directory, indent=""):
    # Recursively prints the directory structure.
    items = sorted(os.listdir(directory))
    for index, item in enumerate(items):
        path = os.path.join(directory, item)
        is_last = index == len(items) - 1
        connector = "└── " if is_last else "├── "
        print(indent + connector + item)
        if os.path.isdir(path):
            new_indent = indent + ("    " if is_last else "│   ")
            tree_structure(path, new_indent)

# Run this in the root of the project
root_directory = "."  # Change this if needed
print(root_directory)
tree_structure(root_directory)