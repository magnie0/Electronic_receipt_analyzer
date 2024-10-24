import os
import pandas as pd
import openpyxl
import re

#concatenaties all excel files (in format year-month-day.xlsx) in current directory to one file

#name for result file
result = "result.xlsx"

#get list of files in current directory to concatenate
def get_files():
    #list all files and directories in the current directory
    files = os.listdir('.')

    #sort the list of files alphabetically
    sorted_files = sorted(files)

    #filter only files with date
    date_pattern = f"\d\d\d\d-\d\d-\d\d.xlsx"
    date_files = [file for file in sorted_files if re.match(date_pattern, file)]
    return date_files


def concatenate():
    input_files = get_files()
    

    # Create a list to hold DataFrames
    dataframes = []

    # Read each Excel file and append to the list
    for file_path in input_files:
        # Read the data from the first sheet of the current file
        df = pd.read_excel(file_path)
        dataframes.append(df)
    concatenate_df = pd.concat(dataframes)

    concatenate_df.to_excel(result, index=False)
   


concatenate()