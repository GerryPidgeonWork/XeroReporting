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
from processes.P01_set_file_paths import consolidated_xero_data_wsl_folder, clean_xero_data_wsl_folder
from processes.P03_shared_functions import clean_numeric_column, calculate_x_rate
from processes.P04_static_lists import XERO_COLUMNS_TO_KEEP, XERO_COLUMNS_TO_RENAME, XERO_COLUMNS_SORT_ORDER

# Main Code
def process_xero_data():
    # Capture start time
    start_time = dt.datetime.now()

    # Show Started Message in Terminal
    func_name = inspect.currentframe().f_code.co_name
    print(f'{func_name} started')

    # Create Dataframe with imported data
    df = pd.read_csv(consolidated_xero_data_wsl_folder / 'Consolidated Xero Data.csv', encoding='utf-8')

    # Adjust Dataframe by retaining and renaming columns
    df = df[XERO_COLUMNS_TO_KEEP]
    df = df.rename(columns=XERO_COLUMNS_TO_RENAME)
        
    # Clean and create Date column(s)
    df['TxDate'] = pd.to_datetime(df['TxDate']).dt.date
    df['TxMonth'] = df['TxDate'].apply(lambda x: pd.Timestamp(year=x.year, month=x.month, day=1))

    # Clean Numerical column(s)
    df = clean_numeric_column(df, 'DebitLocalCurrency')
    df = clean_numeric_column(df, 'CreditLocalCurrency')
    df = clean_numeric_column(df, 'GrossLocalCurrency')
    df = clean_numeric_column(df, 'NetLocalCurrency')
    df = clean_numeric_column(df, 'VatLocalCurrency')
    df = clean_numeric_column(df, 'DebitGBP')
    df = clean_numeric_column(df, 'CreditGBP')
    df = clean_numeric_column(df, 'GrossGBP')
    df = clean_numeric_column(df, 'NetGBP')
    df = clean_numeric_column(df, 'VatGBP')
    df['VatRate'] = df['VatRate'] / 100

    # Create Columns
    df['GLNumber'] = df['GLNumber'].astype(int).astype(str)
    df['GLCode'] = df['GLNumber'] + ' ' + df['GLName']
    df = calculate_x_rate(df, transaction_type="Debit")
    df = calculate_x_rate(df, transaction_type="Credit")
    df = calculate_x_rate(df, transaction_type="Net")
    df = calculate_x_rate(df, transaction_type="Gross")

    # Reorder Dataframe
    df = df[XERO_COLUMNS_SORT_ORDER]
    df = df.sort_values(by=['TxDate', 'GLNumber'], ascending=True)

    # Temp Save
    os.chdir(clean_xero_data_wsl_folder)
    df.to_csv('Cleaned Xero Data.csv', index=False, encoding="utf-8")
    print(f"Saving file to: {os.getcwd()}")

    # Capture end time and calculate duration
    end_time = dt.datetime.now()
    duration = end_time - start_time

    # Show Complete Message in Terminal
    print(f'{func_name} complete in {duration}')

    return df

cleaned_xero_data = process_xero_data()