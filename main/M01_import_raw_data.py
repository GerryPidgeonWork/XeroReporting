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
sys.dont_write_bytecode = True  # Stops sys from making __pychace__ folders

# Import specific data and functions from external modules
from processes.P01_set_file_paths import xero_data_folder



# Main Code (Should be on line 20)
def load_xero_data():
    """
    Loads and consolidates multiple Excel files containing Xero data from a specified folder.

    The function performs the following steps:
    1. Lists all `.xlsx` files in the `xero_data_folder`, excluding temporary files (e.g., `~$` prefixed files).
    2. Reads each file to locate the header row containing the keyword "Date".
    3. Re-reads the file with the correct header and removes unwanted rows and columns.
    4. Combines all cleaned DataFrames into a single DataFrame.
    5. Prints summary details, including the number of rows combined.
    6. Captures execution time and prints completion status.

    Returns:
        pd.DataFrame: A consolidated DataFrame containing Xero data from all processed files.
    """

    # Capture start time
    start_time = dt.datetime.now()

    # Show Started Message in Terminal
    func_name = inspect.currentframe().f_code.co_name
    print(f'{func_name} started')

    # List all Excel files in the folder
    xlsx_files = [f for f in Path(xero_data_folder).glob("*.xlsx") if not f.name.startswith("~$")]

    # Initialize an empty list to store DataFrames
    dataframes = []

    # Process each file
    for file in xlsx_files:
        print(f"Processing: {file.name}")

        # Read the raw file (to find the header row)
        df = pd.read_excel(file, engine="openpyxl")
        
        # Find the header row containing "Date"
        header_row_index = df[df.iloc[:, 0].astype(str).str.contains("Date", na=False)].index[0]

        # Re-read the file using the correct header row
        df = pd.read_excel(file, engine="openpyxl", skiprows=header_row_index + 1, header=0)

        # Drop empty "Unnamed" columns
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # Remove "Total" rows
        df = df[df['Date'] != 'Total']

        # Append to list
        dataframes.append(df)

    # Combine all DataFrames
    combined_xero_data = pd.concat(dataframes, ignore_index=True)

    # Capture end time and calculate duration
    end_time = dt.datetime.now()
    duration = end_time - start_time

    # Show Complete Message in Terminal
    print(f'{func_name} complete in {duration}')

    return combined_xero_data

imported_xero_data = load_xero_data()