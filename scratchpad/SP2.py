# Import necessary libraries (should be consistent across all sheets)
import os  # Module for interacting with the operating system (e.g., file paths)
import sys  # Module for accessing system-specific parameters and functions
import subprocess
import pandas as pd  # Library for data manipulation and analysis
import numpy as np  # Library for numerical operations and array handling
import datetime as dt  # Module for working with dates and times
import inspect  # Module for inspecting live objects (e.g., function names)
from pathlib import Path  # Object-oriented interface for working with file and directory paths
from decimal import Decimal  # For precise decimal arithmetic (e.g., handling monetary values)

# Update system path to include parent directories for module access. This allows the script to import modules anywhere in the folder hierarchy.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.dont_write_bytecode = True  # Stops sys from making __pychace__ folders

# Import specific data and functions from external modules



# Main Code (Should be on line 20)
xero_data_windows_folder = Path(r"H:\\Shared drives\\EU Finance & Accounting\\Commercial Finance\\Month End Reporting\\01 Raw Data\\01 Xero Export Data")
axiom_data_windows_folder = Path(r"H:\\Shared drives\\EU Finance & Accounting\\Commercial Finance\\Month End Reporting\\01 Raw Data\\02 Axiom Mapping Data")

xero_data_wsl_folder = Path(str(xero_data_windows_folder).replace("H:", "/mnt/h").replace("\\", "/"))
axiom_data_wsl_folder = Path(str(axiom_data_windows_folder).replace("H:", "/mnt/h").replace("\\", "/"))

print("Xero WSL Path:", xero_data_wsl_folder)
print("Axiom WSL Path:", axiom_data_wsl_folder)
