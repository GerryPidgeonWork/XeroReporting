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
from processes.P01_set_file_paths import download_folder, system_data_folder
from main.M02_clean_raw_data import cleaned_xero_data


# Create Dataframe with imported data
df = cleaned_xero_data.copy()

# Import Required Sstem Data Files
mapping_df = pd.read_csv(system_data_folder / "GLCode To GLGroup Mapping.csv")
mapping_df['GLNumber'] = mapping_df['GLNumber'].astype(int).astype(str)

missing_df = df[['GLNumber', 'GLName']]
missing_df = missing_df.drop_duplicates()


print(f"Shape of Mapping DF: {mapping_df.shape}")
print(f"Shape of De-duplicated DF: {missing_df.shape}")


df = pd.merge(df, mapping_df, on=['GLNumber', 'GLName'], how='left')

# Update Comments

mapping_df = pd.concat([mapping_df, missing_df], ignore_index=True)
mapping_df = mapping_df.drop_duplicates(subset=['GLNumber', 'GLName'], keep='first')



# Import Required Sstem Data Files


# Add Missing Records to CSV
# try:
#     os.remove('GLCode To GLGroup Mapping (Old).csv')
# except FileNotFoundError:
#     pass
# os.rename('GLCode To GLGroup Mapping.csv', 'Full Rx List, with Cleaned Names (Old).csv')
# df.to_csv('Full Rx List, with Cleaned Names.csv', index=False)