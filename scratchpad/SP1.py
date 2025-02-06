import os

xero_data_folder = "H:/Shared drives/EU Finance & Accounting/Commercial Finance/Month End Reporting/01 Raw Data/01 Xero Export Data"

# Manually convert to a WSL-compatible path
wsl_path = xero_data_folder.replace("H:", "/mnt/h").replace("\\", "/")
print("WSL Path:", wsl_path)

# Check if the directory exists
if os.path.exists(wsl_path):
    print("Directory found! Listing files:")
    files = os.listdir(wsl_path)
    for file in files:
        print(file)
else:
    print("Directory not found. Check if H: is mounted in /mnt/h/")
