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
from processes.P01_set_file_paths import download_folder, system_data_folder, mapping_data_folder
from main.M02a_clean_raw_xero_data import cleaned_xero_data

# Create Dataframe with imported data
df = cleaned_xero_data.copy()

# Import Required Mapping Data Files
gl_mapping_df = pd.read_csv(mapping_data_folder / "gl_mapping.csv")
location_mapping_df = pd.read_csv(mapping_data_folder / "location_mapping.csv")

# Print shape of each data frame
print(f"Xero Data Shape: Rows {df.shape[0]}, Columns {df.shape[1]}")
print(f"GL Mapping File Shape: Rows {gl_mapping_df.shape[0]}, Columns {gl_mapping_df.shape[1]}")
print(f"Location Mapping File Shape: Rows {location_mapping_df.shape[0]}, Columns {location_mapping_df.shape[1]}")

# Set Data Types for Mapping Files
gl_mapping_df['GLNumber'] = gl_mapping_df['GLNumber'].astype(int).astype(str)

# Replace blank enties with "Missing"
df[['GLNumber', 'GLName', 'Location', 'CostCentre']] = df[['GLNumber', 'GLName', 'Location', 'CostCentre']].apply(lambda col: col.astype(str).str.strip().replace({"": "Missing", "nan": "Missing"})).fillna("Missing")

# Make a copy of Xero Data Dataframe for mapping files
gl_checking_df = df.copy()
location_checking_df = df.copy()

# Merge DataFrames Together
df = pd.merge(df, gl_mapping_df, on=['GLName', 'GLNumber'], how='left')
df = pd.merge(df, location_mapping_df, on=['Location'], how='left')

# Populate "Missing" Locations onto "location_mapping.csv"
location_missing_df = df.copy()
location_missing_df = location_missing_df.loc[location_missing_df['LocationGroup'].isna()]
location_missing_df = location_missing_df.loc[:, ['Location', 'LocationGroup']].drop_duplicates()
location_combined_df = pd.concat([location_mapping_df, location_missing_df], ignore_index=True)
location_combined_df = location_combined_df.drop_duplicates(keep='first')
location_combined_df.to_csv(Path(mapping_data_folder) / 'location_mapping.csv', index=False, encoding='utf-8')

# Populate "Missing" Locations onto "gl_mapping.csv"
gl_missing_df = df.copy()
gl_missing_df = gl_missing_df.loc[gl_missing_df[['GLGroup', 'Signage']].isna().any(axis=1)]
gl_missing_df = gl_missing_df.loc[:, ['GLNumber', 'GLName', 'GLGroup', 'Signage']].drop_duplicates()
print(gl_missing_df)
gl_combined_df = pd.concat([gl_mapping_df, gl_missing_df], ignore_index=True)
gl_combined_df = gl_combined_df.drop_duplicates(keep='first')
gl_combined_df.to_csv(Path(mapping_data_folder) / 'gl_mapping.csv', index=False, encoding='utf-8')

# Check if there are any blank records in mapping files
print(f"Blank GLGroup Mapping Records: {gl_combined_df['GLGroup'].isna().sum()}")
print(f"Blank Signage Mapping Records: {gl_combined_df['Signage'].isna().sum()}")
print(f"Blank LocationGroup Mapping Records: {location_combined_df['LocationGroup'].isna().sum()}")

# Apply Signage to values
df['NetGBP'] = df['NetGBP'] * df['Signage'].fillna(1)
df['GrossGBP'] = df['GrossGBP'] * df['Signage'].fillna(1)
df['NetLocalCurrency'] = df['NetLocalCurrency'] * df['Signage'].fillna(1)
df['GrossLocalCurrency'] = df['GrossLocalCurrency'] * df['Signage'].fillna(1)

# Create AxiomCode
df['AxiomGLCode'] = df['GLNumber'].astype(str).str[:5]
df['AxiomLocationCode'] = 'LO_' + df['Location'].str.split(' ', n=1).str[0]
df['AxiomCostCentreCode'] = df['CostCentre'].str.split(' ', n=1).str[0]

# Populate Axiom Data




# Overwrite Specific GLGroups
df['GLGroup'] = np.where((df['GLGroup'] == 'Operations Wages') & (df['CostCentre'] == '10026 Shift Leads'), 'GM and SL Costs', df['GLGroup'])
df['GLGroup'] = np.where((df['GLGroup'] == 'Corp S&W') & (df['CostCentre'] == '10026 Shift Leads'), 'GM and SL Costs', df['GLGroup'])
df['GLGroup'] = np.where((df['GLGroup'] == 'Corp S&W') & (df['CostCentre'] == '10027 Site Leadership'), 'GM and SL Costs', df['GLGroup'])
df['GLGroup'] = np.where((df['GLGroup'] == 'Operations Wages') & (df['CostCentre'] == '10063 Drivers (W2)'), 'Driver Earnings', df['GLGroup'])
df['GLGroup'] = np.where((df['GLGroup'] == 'Corp S&W') & (df['CostCentre'] == '10063 Drivers (W2)'), 'Driver Earnings', df['GLGroup'])
df['GLGroup'] = np.where((df['GLGroup'] == 'Corp S&W') & (df['CostCentre'] == '10025 Ops Associates') & (df['LocationGroup'] == 'MFC'), 'Operations Wages', df['GLGroup'])
df['GLGroup'] = np.where((df['GLGroup'] == 'Other Corp SG&A') & (df['GLName'] == 'Prof Services: Recruitment Expenses'), 'Driver Acquisition Costs', df['GLGroup'])
df['GLGroup'] = np.where((df['GLGroup'] == 'MFC Rent') & (df['LocationGroup'] == 'HQ'), 'Other Corp SG&A', df['GLGroup'])
df['GLGroup'] = np.where((df['GLGroup'] == 'Insurance') & (df['LocationGroup'] == 'HQ'), 'Other Corp SG&A', df['GLGroup'])
df['GLGroup'] = np.where((df['GLGroup'] == 'Other MFC Costs') & (df['LocationGroup'] == 'HQ'), 'Other Corp SG&A', df['GLGroup'])
df['GLGroup'] = np.where((df['GLGroup'] == 'Other MFC Costs') & (df['LocationGroup'] == 'MFC'), 'Other MFC Opex', df['GLGroup'])

# Sort DataFrame for Output
df = df[['TxDate', 'TxMonth', 'GLCode', 'GLNumber', 'GLName', 'GLType', 'GLGroup', 'Location', 'LocationGroup', 'CostCentre', 'TxCurrency', 'VatRate', 'NetGBP', 'GrossGBP', 'NetLocalCurrency', 'GrossLocalCurrency', 'NetFxRate', 'GrossFxRate']]


# Save Final Output
os.chdir(download_folder)
df.to_csv('Xero Final Output.csv', index=False, encoding='utf-8')