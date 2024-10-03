import sys
from pathlib import Path

# Add the root directory to the Python path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(root_dir))
