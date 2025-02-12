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
from processes.P01_set_file_paths import raw_axiom_data_wsl_folder, converted_axiom_data_wsl_folder

# Main Code (Should be on line 20)
def load_axiom_data():
    # Capture start time
    start_time = dt.datetime.now()

    # Show Started Message in Terminal
    func_name = inspect.currentframe().f_code.co_name
    print(f'{func_name} started')

    # Load Axiom Location Data
    location_axiom_mapping = raw_axiom_data_wsl_folder / 'Axiom Mapping.xlsx'
    location_axiom_df = pd.read_excel(location_axiom_mapping, sheet_name="Axiom Mapping (LOC)")
    location_axiom_df = location_axiom_df.loc[:, ~location_axiom_df.columns.str.contains('Unnamed', case=False)] # Remove Unnamed Columns
    
    # Load Axiom Account Data
    account_axiom_mapping = raw_axiom_data_wsl_folder / 'Axiom Mapping.xlsx'
    account_axiom_df = pd.read_excel(account_axiom_mapping, sheet_name="Axiom Mapping (Acct)")

    # Load Axiom Cost Centre Data
    cost_centre_axiom_mapping = raw_axiom_data_wsl_folder / 'Axiom Mapping.xlsx'
    cost_centre_axiom_df = pd.read_excel(cost_centre_axiom_mapping, sheet_name="Axiom Mapping (CC)")

    # Rename Columns
    location_axiom_df = location_axiom_df.rename(columns={col: f'LOC.{col}' for col in location_axiom_df})
    account_axiom_df = account_axiom_df.rename(columns={col: f'ACCT.{col}' for col in account_axiom_df})
    cost_centre_axiom_df = cost_centre_axiom_df.rename(columns={col: f'CC.{col}' for col in cost_centre_axiom_df})

    # Load Axiom Cost Centre Data
    allocation_logic_axiom_mapping = raw_axiom_data_wsl_folder / 'Axiom Mapping.xlsx'
    allocation_logic_axiom_df = pd.read_excel(allocation_logic_axiom_mapping, sheet_name=0)

    # Clean Data to just show allocation rules
    allocation_logic_axiom_df = allocation_logic_axiom_df.iloc[:, 1:] # Delete first column
    allocation_logic_axiom_df = allocation_logic_axiom_df.iloc[2:, :] # Delete first two rows
    allocation_logic_axiom_df = allocation_logic_axiom_df[allocation_logic_axiom_df.iloc[:, 0].notna() & allocation_logic_axiom_df.iloc[:, 1].notna()] # Keep only populated rows

    # Rename Columns
    allocation_logic_axiom_df = allocation_logic_axiom_df.rename(columns={allocation_logic_axiom_df.columns[0]: "AllocationRule", 
                                                                          allocation_logic_axiom_df.columns[1]: "GLGroup"})
    allocation_logic_axiom_df = allocation_logic_axiom_df[['GLGroup', 'AllocationRule']]

    # Save mapping files as CSV
    os.chdir(converted_axiom_data_wsl_folder)
    location_axiom_df.to_csv('Axiom Location Mapping Data.csv', index=False, encoding='utf-8')
    account_axiom_df.to_csv('Axiom GL Account Mapping Data.csv', index=False, encoding='utf-8')
    cost_centre_axiom_df.to_csv('Axiom Cost Centre Mapping Data.csv', index=False, encoding='utf-8')
    allocation_logic_axiom_df.to_csv('Axiom Allocation Rules.csv', index=False, encoding='utf-8')
 
    # Capture end time and calculate duration
    end_time = dt.datetime.now()
    duration = end_time - start_time

    # Show Complete Message in Terminal
    print(f'{func_name} complete in {duration}')

    return location_axiom_df, account_axiom_df

imported_axiom_data = load_axiom_data()