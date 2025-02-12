# Import necessary libraries (should be consistent across all sheets)
import os  # Module for interacting with the operating system (e.g., file paths)
import sys  # Module for accessing system-specific parameters and functions
import re
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
from processes.P01_set_file_paths import converted_axiom_data_wsl_folder, clean_axiom_data_wsl_folder

# Load Axiom Allocation Rules
os.chdir(converted_axiom_data_wsl_folder)
allocation_logic_axiom_df = pd.read_csv('Axiom Allocation Rules.csv', encoding='utf-8')

# Copy Column to convert from SQL to Pandas
allocation_logic_axiom_df['PandasConversion'] = allocation_logic_axiom_df['AllocationRule']

# Replace with Upper Case
allocation_logic_axiom_df['PandasConversion'] = (allocation_logic_axiom_df['PandasConversion']
                                                 .str.replace('=', ' = ')
                                                 .str.replace('Acct', 'ACCT', case=True)
                                                 .str.replace('Loc', 'LOC', case=True)
                                                 .str.replace('cc', 'CC', case=True))

# Regular expression pattern to match "XX.XX" format
pattern = r'\b([A-Z]+)\.([A-Za-z0-9]+)\b(?=\s)'

# Apply regex transformation directly to the PandasConversion column
allocation_logic_axiom_df['PandasConversion'] = allocation_logic_axiom_df['PandasConversion'].apply(lambda x: re.sub(pattern, r"df['\1.\2']", x) if pd.notna(x) else x)

# Replace SQL logical operators with Pandas equivalents
allocation_logic_axiom_df['PandasConversion'] = (allocation_logic_axiom_df['PandasConversion']
                                                 .str.replace(r"\bAND\b", "&", case=True, regex=True)
                                                 .str.replace(r"\bOR\b", "|", case=True, regex=True)
                                                 .str.replace(r"\bAND\b", "&", case=True, regex=True)
                                                 .str.replace(r"\bOR\b", "|", case=True, regex=True)
                                                 .str.replace(r"(?<![<>])=", "==", regex=True)
                                                 .str.replace(r"<>", "!=", regex=True))


    # allocation_logic_axiom_df['AllocationRule'] = (allocation_logic_axiom_df['AllocationRule']
    #                                                .str.replace('Acct', 'ACCT')
    #                                                .str.replace('ACCT ', 'ACCT.ACCT ')
    #                                                .str.replace('ACCT.ACCT.ACCT', 'ACCT.ACCT')
    #                                                .str.replace('cc', 'CC')
    #                                                .str.replace('Cc', 'CC')
    #                                                .str.replace('CC ', 'CC.CC ')
    #                                                .str.replace('CC.CC.CC', 'CC.CC')
    #                                                .str.replace('loc', 'LOC')
    #                                                .str.replace('Loc', 'LOC')
    #                                                .str.replace('LOC ', 'LOC.LOC '))




# Save Final Allocation Rule
os.chdir(clean_axiom_data_wsl_folder)
allocation_logic_axiom_df.to_csv('Converted Axiom Allocation Rules.csv', index=False, encoding='utf-8')