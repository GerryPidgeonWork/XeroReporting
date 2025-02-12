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

# Set Download folder

# Get Windows username dynamically
windows_user = os.getenv("USERPROFILE")  # Won't work in WSL, so use another method
if not windows_user:
    windows_user = os.popen("cmd.exe /c echo %USERNAME%").read().strip()  # Runs Windows CMD in WSL
windows_download_folder = Path(f"/mnt/c/Users/{windows_user}/Downloads") # Construct the Windows Downloads path

# Set Window Directory Paths
root_windows_folder = Path(r"H:\\Shared drives\\EU Finance & Accounting\\Commercial Finance\\Month End Reporting\\")
raw_xero_data_windows_folder = root_windows_folder / "01 Raw Data" / "01 Xero Export Data"
raw_axiom_data_windows_folder = root_windows_folder / "01 Raw Data" / "02 Axiom Mapping Data"
consolidated_xero_data_windows_folder = root_windows_folder / "01 Raw Data" / "03 Xero Consolidated Data"
converted_axiom_data_windows_folder = root_windows_folder / "01 Raw Data" / "04 Axiom Convetred Data"
clean_xero_data_windows_folder = root_windows_folder / "02 Cleaned Data" / "01 Xero Data"
clean_axiom_data_windows_folder = root_windows_folder / "02 Cleaned Data" / "02 Axiom Data"
processed_xero_data_windows_folder = root_windows_folder / "03 Processed Data"

# Convert Windows Directory Paths to WSL
raw_xero_data_wsl_folder = Path(str(raw_xero_data_windows_folder).replace("H:", "/mnt/h").replace("\\", "/"))
raw_axiom_data_wsl_folder = Path(str(raw_axiom_data_windows_folder).replace("H:", "/mnt/h").replace("\\", "/"))
consolidated_xero_data_wsl_folder = Path(str(consolidated_xero_data_windows_folder).replace("H:", "/mnt/h").replace("\\", "/"))
converted_axiom_data_wsl_folder = Path(str(converted_axiom_data_windows_folder).replace("H:", "/mnt/h").replace("\\", "/"))
clean_xero_data_wsl_folder = Path(str(clean_xero_data_windows_folder).replace("H:", "/mnt/h").replace("\\", "/"))
clean_axiom_data_wsl_folder = Path(str(clean_axiom_data_windows_folder).replace("H:", "/mnt/h").replace("\\", "/"))
processed_axiom_data_wsl_folder = Path(str(processed_xero_data_windows_folder).replace("H:", "/mnt/h").replace("\\", "/"))