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

# Import specific data and functions from external modules





# Main Code (Should be on line 20)
def clean_numeric_column(df, column_name):
    """
    Cleans a specified column in a DataFrame by removing non-numeric characters
    and converting the column to float.

    Args:
        df (pd.DataFrame): The DataFrame containing the column to clean.
        column_name (str): The name of the column to clean.

    Returns:
        pd.DataFrame: The DataFrame with the cleaned column.
    """
    df[column_name] = df[column_name].replace(r"[^\d\.\-]", "", regex=True).astype(float)
    return df

def calculate_x_rate(df, transaction_type="Debit"):
    """
    Calculates the exchange rate (X Rate) for a given transaction type by dividing 
    the source currency amount by the GBP amount. If the denominator is NaN or zero, 
    the exchange rate defaults to 1.

    Args:
        df (pd.DataFrame): The DataFrame containing financial transaction data.
        transaction_type (str, optional): The type of transaction to calculate 
                                          exchange rate for. 
                                          Options: "Debit", "Credit", "Net", "Gross".
                                          Defaults to "Debit".

    Returns:
        pd.DataFrame: The DataFrame with a new column for the calculated exchange rate.
    
    Example Usage:
        df = calculate_x_rate(df, transaction_type="Credit")
    """

    # Validate transaction type
    valid_types = {"Debit", "Credit", "Net", "Gross"}
    if transaction_type not in valid_types:
        raise ValueError(f"Invalid transaction type: {transaction_type}. Choose from {valid_types}.")

    # Dynamically construct column names
    source_col = f"{transaction_type}LocalCurrency"
    gbp_col = f"{transaction_type}GBP"
    xrate_col = f"{transaction_type}FxRate"

    # Check if necessary columns exist
    if source_col not in df.columns or gbp_col not in df.columns:
        raise KeyError(f"Missing required columns: '{source_col}' or '{gbp_col}' in DataFrame.")

    # Calculate X Rate, handling division by zero or NaN
    df[xrate_col] = df[source_col] / df[gbp_col]
    df[xrate_col] = df[xrate_col].fillna(1)  # Replace NaN with 1
    df[xrate_col] = df[xrate_col].replace([float('inf'), -float('inf')], 1)  # Handle division by zero

    return df

def convert_sql_to_pandas_filter(sql_condition):
    """
    Convert SQL-like conditions into Pandas filtering expressions.
    """

    # Standardize spacing and case
    sql_condition = sql_condition.strip()

    # Convert standalone ACCT, CC, and LOC to explicit field names
    sql_condition = re.sub(r'\bACCT\b', 'ACCT.ACCT', sql_condition)
    sql_condition = re.sub(r'\bCC\b', 'CC.CC', sql_condition)
    sql_condition = re.sub(r'\bLOC\b', 'LOC.LOC', sql_condition)

    # Replace SQL logical operators with Pandas equivalents
    sql_condition = sql_condition.replace(" and ", " & ").replace(" AND ", " & ")
    sql_condition = sql_condition.replace(" or ", " | ").replace(" OR ", " | ")
    sql_condition = sql_condition.replace("<>", "!=")

    # # Handle string equality conditions (e.g., column = 'value')
    # sql_condition = re.sub(r"(\b\w+\.\w+\b)\s*=\s*'([^']*)'", r"(df['\1'] == '\2')", sql_condition)

    # # Handle string inequality conditions (e.g., column <> 'value')
    # sql_condition = re.sub(r"(\b\w+\.\w+\b)\s*!=\s*'([^']*)'", r"(df['\1'] != '\2')", sql_condition)

    # # Handle NOT IN clauses (e.g., column NOT IN ('val1', 'val2'))
    # sql_condition = re.sub(r"(\b\w+\.\w+\b)\s*not in\s*\(([^)]+)\)", r"(~df['\1'].isin([\2]))", sql_condition)

    # # Handle IN clauses (e.g., column IN ('val1', 'val2'))
    # sql_condition = re.sub(r"(\b\w+\.\w+\b)\s*in\s*\(([^)]+)\)", r"(df['\1'].isin([\2]))", sql_condition)

    # # Handle numeric conditions (e.g., column = 123, column <> 456)
    # sql_condition = re.sub(r"(\b\w+\.\w+\b)\s*=\s*(\d+)", r"(df['\1'] == \2)", sql_condition)
    # sql_condition = re.sub(r"(\b\w+\.\w+\b)\s*!=\s*(\d+)", r"(df['\1'] != \2)", sql_condition)

    # # Ensure all column references are wrapped in df[]
    # sql_condition = re.sub(r'\b([A-Z]+\.[A-Z0-9_]+)\b', r"df['\1']", sql_condition)

    # # Ensure proper handling of multiple conditions
    # sql_condition = re.sub(r'(\(df\[\'[A-Z0-9_.]+\'\] == .+?)\s*([&|])\s*(df\[\'[A-Z0-9_.]+\'\] == .+?\))', r"(\1 \2 \3)", sql_condition)

    # # Fix accidental duplicate df['df[' issues
    # sql_condition = sql_condition.replace("df['df[", "df[")

    # # ✅ Debugging Output
    # print(f"🔵 Converted Pandas filter: {sql_condition}")

    # # ❌ Syntax Error Checking: Detect incorrect `=` usage
    # if re.search(r"(?<![=!<>])=(?![=!<>])", sql_condition):  
    #     raise ValueError(f"❌ Syntax Error: Detected a misplaced '=' in filter: {sql_condition}")

    return sql_condition