import os
import sys

# Go two levels up from the current file (test2.py)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
print("Adding to sys.path:", project_root)

# Add project root to sys.path so you can import from src
sys.path.append(project_root)

# Now this import should work
from src.commons.utils import load_envs
