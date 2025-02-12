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
from processes.P01_set_file_paths import converted_axiom_data_wsl_folder, clean_xero_data_wsl_folder, converted_axiom_data_wsl_folder, processed_axiom_data_wsl_folder
from processes.P03_shared_functions import convert_sql_to_pandas_filter
from main.M02a_clean_raw_xero_data import cleaned_xero_data

# Create Dataframe with imported data
df = cleaned_xero_data.copy()

# Load Axiom Data
os.chdir(converted_axiom_data_wsl_folder)
location_axiom_df = pd.read_csv('Axiom Location Mapping Data.csv', encoding='utf-8')
cost_centre_axiom_df = pd.read_csv('Axiom Cost Centre Mapping Data.csv', encoding='utf-8')
gl_account_axiom_df = pd.read_csv('Axiom GL Account Mapping Data.csv', encoding='utf-8')

# Create AxiomCode from Xero Data
df['AxiomGLCode'] = df['GLNumber'].astype(str).str[:5].astype(str)
df['AxiomLocationCode'] = df['Location'].str.split(' ', n=1).str[0]
df['AxiomLocationCode'] = np.where(df['AxiomLocationCode'].str.isdigit(), 'LO_' + df['AxiomLocationCode'], '')
df['AxiomCostCentreCode'] = df['CostCentre'].str.split(' ', n=1).str[0].astype(str)

# Change Numbers to Strings for Merging
cost_centre_axiom_df['CC.CC'] = cost_centre_axiom_df['CC.CC'].astype(str)
gl_account_axiom_df['ACCT.ACCT'] = gl_account_axiom_df['ACCT.ACCT'].astype(str)

# Merge Files and rename relevant columns
df = pd.merge(df, location_axiom_df, left_on='AxiomLocationCode', right_on='LOC.LOC', how='left')
df = pd.merge(df, cost_centre_axiom_df, left_on='AxiomCostCentreCode', right_on='CC.CC', how='left')
df = pd.merge(df, gl_account_axiom_df, left_on='AxiomGLCode', right_on='ACCT.ACCT', how='left')

# Populate Blank Entries
default_location_axiom_entry = location_axiom_df.iloc[-1]  # Last row of location data
default_cost_centre_axiom_entry = cost_centre_axiom_df.iloc[-1]  # Last row of cost centre data

# Fix Blank Entries with Defualt Locations and Cost Centres
for col in location_axiom_df.columns:
    df[col] = df[col].fillna(default_location_axiom_entry[col])
for col in cost_centre_axiom_df.columns:
    df[col] = df[col].fillna(default_cost_centre_axiom_entry[col])

# Save Final Output
os.chdir(clean_xero_data_wsl_folder)
df.to_csv('Xero Cleaned Output.csv', index=False, encoding='utf-8')

# Load Axiom Allocation Rules
os.chdir(clean_xero_data_wsl_folder)
df = pd.read_csv('Xero Cleaned Output.csv', encoding='utf-8')

# Individual Checks
df['GLGroup'] = ''

# Define a dictionary mapping ACCT.Level1 to GLGroup
gl_group_mapping = {
    'Depreciation & Amortization': 'Depreciation & Amortization',
    'Income Taxes': 'Income Taxes'}

# Apply the mapping only where LOC.Entity is 'International'
df.loc[df['LOC.Entity'] == 'International', 'GLGroup'] = df['ACCT.Level1'].map(gl_group_mapping).fillna(df['GLGroup'])

# Define a dictionary mapping ACCT.Level2 to GLGroup
gl_group_mapping = {
    'Gross Product Sales': 'Gross Product Sales',
    'Delivery Revenue': 'Delivery Revenue',
    'Subscription': 'Subscription',
    'Data Licensing Revenue': 'Data Licensing Revenue',
    'Other Revenue': 'Other Revenue',
    'Product Sale Discounts': 'Product Sale Discounts',
    'Chargebacks/Refunds': 'Chargebacks/Refunds',
    'Puff Points Deferral': 'Puff Points Deferral',
    'Direct Product Costs': 'Direct Product Costs',
    'Merch Incentives': 'Merch Incentives',
    'Purchase Price Variance': 'Purchase Price Variance',
    'Credit Card Processing Fees': 'Credit Card Processing Fees',
    'Damaged and Expired': 'Damaged and Expired',
    'Non Transactional Shrink': 'Non Transactional Shrink',
    'Inventory Reserves': 'Inventory Reserves',
    'Global Ads Contra COGS': 'Global Ads Contra COGS',
    'Order Packaging (Bags)': 'Order Packaging (Bags)',
    'Partnership Fees': 'Partnership Fees',
    'Interest Expense': 'Interest Expense'}

# Apply the mapping only where LOC.Entity is 'International'
df.loc[df['LOC.Entity'] == 'International', 'GLGroup'] = df['ACCT.Level2'].map(gl_group_mapping).fillna(df['GLGroup'])

gl_group_mapping = {
    'Severance Expense': 'Severance Expense',
    'Stock Based Compensation Expense': 'Stock Based Compensation Expense',
    'Process Improvement': 'Process Improvement',
    'Acquisition and Transactions Expense': 'Acquisition and Transactions Expense',
    'COGS: Other - EBITDA Adjustments': 'COGS: Other - EBITDA Adjustments',
    'Legal Contingency Expenses': 'Legal Contingency Expenses'}

# Apply the mapping only where LOC.Entity is 'International'
df.loc[df['LOC.Entity'] == 'International', 'GLGroup'] = df['ACCT.Description'].map(gl_group_mapping).fillna(df['GLGroup'])

# Apply individual conditions using df.loc[]
df.loc[
    (
        (df['ACCT.Level1'] == 'Salaries & Related') & 
        ((df['CC.Level2'] == 'Driver Partners') | 
        (df['ACCT.Description'] == '1099 Driver Pay Tips') | 
        (df['ACCT.Description'] == 'Partnership Delivery Fee') | 
        ((df['ACCT.Description'] == '1099 Driver Pay') & df['CC.CC'].isin([10011, 10035])) | 
        (df['ACCT.ACCT'] == 90050))
    ) & (df['LOC.Entity'] == 'International'),
    'GLGroup'
] = 'Driver Earnings'

df.loc[
    (df['ACCT.Level1'] == 'Salaries & Related') & 
    (df['ACCT.Description'] != 'Severance Expense') & 
    (df['CC.Description'].isin(['Ops Associates'])) & 
    (df['LOC.Entity'] == 'International'),
    'GLGroup'
] = 'Operation Wages'

df.loc[
    ((df['ACCT.Level2'].isin(['Inbound Freight and DC Costs'])) | 
     ((df['CC.CC'] == 10076) & (df['ACCT.Level2'] == 'Salaries & Related'))) & 
    (df['LOC.Entity'] == 'International'),
    'GLGroup'
] = 'Inbound Freight and DC Costs'

df.loc[
    (df['ACCT.PnL1'] == 'Corp S&W') & 
    (df['CC.Level3'] == 'Fixed Fulfillment') & 
    (df['LOC.Entity'] == 'International') & 
    (~df['LOC.Country'].isin(['FR', 'ES'])),
    'GLGroup'
] = "GM's and Shift Leads"

df.loc[
    (df['ACCT.ACCT'].isin([63605, 64002, 64004, 63699, 67002])) & 
    (df['LOC.Entity'] == 'International') & 
    (~df['LOC.Country'].isin(['FR', 'ES'])) & 
    (df['LOC.FieldCorp'] == 'Field'),
    'GLGroup'
] = 'Driver Acquisition Cost'

df.loc[
    (df['ACCT.PnL1'] == 'Rent') & 
    (df['LOC.Entity'] == 'International') & 
    (df['LOC.FieldCorp'] == 'Field') & 
    (~df['LOC.Country'].isin(['FR', 'ES'])),
    'GLGroup'
] = 'MFC Rent'

df.loc[
    (df['ACCT.ACCT'].isin([62211, 63402, 63403, 63404, 63310])) & 
    (df['LOC.Entity'] == 'International') & 
    (~df['LOC.Country'].isin(['FR', 'ES'])) & 
    (df['LOC.FieldCorp'] == 'Field'),
    'GLGroup'
] = 'Insurance'

df.loc[
    (df['ACCT.Level2'] == 'Utilities & Other Facility Expense') & 
    (df['LOC.Entity'] == 'International') & 
    (~df['LOC.Country'].isin(['FR', 'ES'])) & 
    (df['LOC.FieldCorp'] == 'Field'),
    'GLGroup'
] = 'Utilities and Facilities'

df.loc[
    (df['ACCT.PnL1'] != 'Rent') & 
    (~df['ACCT.ACCT'].isin([62211, 63402, 63403, 63404, 63310, 63611])) & 
    (df['ACCT.Level2'] != 'Utilities & Other Facility Expense') & 
    (df['LOC.Entity'] == 'International') & 
    (~df['LOC.Country'].isin(['FR', 'ES'])) & 
    (df['LOC.FieldCorp'] == 'Field') & 
    (df['ACCT.Level1'] == 'Operating Expenses'),
    'GLGroup'
] = 'Other MFC Opex'

df.loc[
    (df['ACCT.Level2'] == 'Advertising & Promotion') & 
    (df['LOC.Entity'] == 'International') & 
    (~df['LOC.Country'].isin(['FR', 'ES'])),
    'GLGroup'
] = 'Advertising & Promotion'

df.loc[
    (df['ACCT.PnL1'] == 'Corp S&W') & 
    (df['CC.SW'] == 'Corp') & 
    (df['LOC.Entity'] == 'International') & 
    (~df['LOC.Country'].isin(['FR', 'ES'])),
    'GLGroup'
] = 'Corp S&W'

df.loc[
    (df['LOC.Entity'] == 'International') & 
    (~df['LOC.Country'].isin(['FR', 'ES'])) & 
    (df['ACCT.Level1'] == 'Operating Expenses') & 
    (df['LOC.FieldCorp'] == 'HQ') & 
    (~df['ACCT.Description'].isin([
        'Loss on Asset Write Down', 'Unrealized Currency Gains/Losses', 
        'Realized Currency Gains/Losses', 'Proceeds of Sale Gain/Loss'
    ])),
    'GLGroup'
] = 'Other Corp SG&A'

df.loc[
    (df['ACCT.Description'].isin(['Gain/Loss on lease adjustments', 'Lease Termination Cost'])) & 
    (df['LOC.Entity'] == 'International'),
    'GLGroup'
] = 'Abandoned Leases'

df.loc[
    ((df['ACCT.Description'].isin([
        'Loss on Asset Write Down', 'Unrealized Currency Gains/Losses', 'Realized Currency Gains/Losses', 
        'Intercompany Services - Income', 'Proceeds of Sale Gain/Loss', 'Other Operating', 'Other Expense'
    ]) & (df['LOC.Entity'] == 'International')) | 
    ((df['ACCT.Description'] == 'Legal Fees') & df['LOC.Country'].isin(['ES']))),
    'GLGroup'
] = 'Other Income / Expense'

os.chdir(processed_axiom_data_wsl_folder)
df.to_csv('Processed Xero Data.csv', index=False, encoding='utf-8')