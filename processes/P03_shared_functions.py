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