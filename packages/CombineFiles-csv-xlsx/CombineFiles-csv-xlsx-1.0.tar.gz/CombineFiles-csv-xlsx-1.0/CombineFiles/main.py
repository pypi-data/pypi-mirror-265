import os
import pandas as pd

def combine_excel_files(folder_path):
    """
    Combine all Excel files (.xlsx) present in a folder into a single DataFrame.

    Parameters:
        folder_path (str): Path to the folder containing Excel files.

    Returns:
        Combined DataFrame
    """
    # Initialize an empty list to store DataFrames
    dfs = []
    
    # Iterate through each file in the folder
    for file in os.listdir(folder_path):
        if file.endswith('.xlsx'):
            # Read the Excel file into a DataFrame
            file_path = os.path.join(folder_path, file)
            data = pd.read_excel(file_path)
            
            # Append DataFrame to the list
            dfs.append(data)
    
    # Concatenate all DataFrames in the list
    combined_data = pd.concat(dfs, ignore_index=True)
    
    # Write the combined DataFrame
    return combined_data


def combine_csv_files(folder_path):
    """
    Combine all CSV files (.csv) present in a folder into a single DataFrame.

    Parameters:
        folder_path (str): Path to the folder containing CSV files.
        
    Returns:
        Combined DataFrame
    """
    # Initialize an empty list to store DataFrames
    dfs = []
    
    # Iterate through each file in the folder
    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            # Read the Excel file into a DataFrame
            file_path = os.path.join(folder_path, file)
            data = pd.read_csv(file_path)
            
            # Append DataFrame to the list
            dfs.append(data)
    
    # Concatenate all DataFrames in the list
    combined_data = pd.concat(dfs, ignore_index=True)
    # Write the combined DataFrame to a CSV file
    return combined_data

# Example usage:
# combine_excel_files("path_to_excel_folder", "output_combined_excel.csv")
# combine_csv_files("path_to_csv_folder", "output_combined_csv.csv")
