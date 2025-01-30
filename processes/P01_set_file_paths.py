# Import necessary libraries (should be consistent across all sheets)
import os  # Module for interacting with the operating system (e.g., file paths)
import sys  # Module for accessing system-specific parameters and functions
import pandas as pd  # Library for data manipulation and analysis
import numpy as np  # Library for numerical operations and array handling
import datetime as dt  # Module for working with dates and times
import inspect  # Module for inspecting live objects (e.g., function names)
from pathlib import Path  # Object-oriented interface for working with file and directory paths
from decimal import Decimal  # For precise decimal arithmetic (e.g., handling monetary values)

# Update system path to include parent directories for module access. This allows the script to import modules anywhere in the folder hierarchy.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import specific data and functions from external modules





# Main Code (Should be on line 20)
# Define required folder paths
xero_data_folder = Path("/home/gerrypidgeongopuff/CodingRepository/Python/GoPuff/XeroData/source_data/xero_data")
system_data_folder = Path("/home/gerrypidgeongopuff/CodingRepository/Python/GoPuff/XeroData/source_data/system_data")
download_folder = Path("/mnt/c/Users/GerryPidgeon/Downloads")