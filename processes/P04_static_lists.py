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
XERO_COLUMNS_TO_KEEP = ['Date', 'Source', 'Contact', 'Description', 'Contact Group', 'Reference', 'Currency', 'Invoice Number', 
                        'Debit (Source)', 'Credit (Source)', 'Gross (Source)', 'Net (Source)', 'VAT (Source)', 'Debit (GBP)', 
                        'Credit (GBP)', 'Gross (GBP)', 'Net (GBP)', 'VAT (GBP)', 'Revalued FX Rate', 'Revalued (GBP)', 'VAT Rate', 
                        'VAT Rate Name', 'Account Code', 'Account', 'Account Type', 'Location', 'Cost Centre', 'Related account']

XERO_COLUMNS_TO_RENAME = {'Date': 'TxDate',
                          'Source': 'Source',
                          'Contact': ' Contact',
                          'Description': 'Description',
                          'Contact Group': 'ContactGroup',
                          'Reference': 'Reference', 
                          'Currency': 'TxCurrency',
                          'Invoice Number': 'InvoiceNumber',
                          'Debit (Source)': 'DebitLocalCurrency',
                          'Credit (Source)': 'CreditLocalCurrency',
                          'Gross (Source)': 'GrossLocalCurrency',
                          'Net (Source)': 'NetLocalCurrency',
                          'VAT (Source)': 'VatLocalCurrency',
                          'Debit (GBP)': 'DebitGBP',
                          'Credit (GBP)': 'CreditGBP',
                          'Gross (GBP)': 'GrossGBP',
                          'Net (GBP)': 'NetGBP',
                          'VAT (GBP)': 'VatGBP',
                          'Revalued FX Rate': 'RevaluedFxRate', 
                          'Revalued (GBP)': 'RevaluedGBP',
                          'VAT Rate': 'VatRate', 
                          'VAT Rate Name': 'VatRateName', 
                          'Account Code': 'GLNumber', 
                          'Account': 'GLName', 
                          'Account Type': 'GLType', 
                          'Location': 'Location', 
                          'Cost Centre': 'CostCentre', 
                          'Related account': 'RelatedAccount'}

XERO_COLUMNS_SORT_ORDER = ['TxDate', 'TxMonth', 'GLCode', 'GLNumber', 'GLName', 'GLType', 'Location', 'CostCentre', 'TxCurrency', 
                           'VatRate', 'NetGBP', 'GrossGBP', 'NetLocalCurrency', 'GrossLocalCurrency', 'NetFxRate', 'GrossFxRate', 
                           'Source', 'ContactGroup', 'Description', 'RelatedAccount']