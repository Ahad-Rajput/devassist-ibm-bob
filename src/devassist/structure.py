"""`devassist structure <path>` — print a visual file tree of the project."""

import os

from .tree import tree_lines


def cmd_structure(path):
    """Print a visual file tree of the project."""
    if not os.path.isdir(path):
        print(f"Error: '{path}' is not a directory.")
        return

    print(f"\n📁 Project structure: {os.path.abspath(path)}\n")
    for line in tree_lines(path):
        print(f"  {line}")
    print()
