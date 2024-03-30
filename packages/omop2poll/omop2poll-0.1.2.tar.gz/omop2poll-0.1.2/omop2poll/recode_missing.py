import pandas as pd


def recode_missing_values(input_data):
    missing_values = [-99, -98, -97]
    if input_data.endswith('.csv'):
        return pd.read_csv(input_data, na_values=missing_values)
    elif input_data.endswith(('.xlsx', '.xls')):
        return pd.read_excel(input_data, na_values=missing_values)
    else:
        raise ValueError("Unsupported file type. Please provide a .csv or .xlsx file.")
