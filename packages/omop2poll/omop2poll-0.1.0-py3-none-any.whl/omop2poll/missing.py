import pandas as pd


def replace_missing_values(input_data):
    """
    Load a dataset (CSV or Excel) into a pandas DataFrame, treating predefined values as missing.
    :param input_data: str, name of the file to load. The function will infer the file type (CSV or Excel) from the extension.
    :return: a pandas DataFrame with the predefined missing values replaced by NaN.
    """
    missing_values = [-99, -98, -97]
    if input_data.endswith('.csv'):
        return pd.read_csv(input_data, na_values=missing_values)
    elif input_data.endswith(('.xlsx', '.xls')):
        return pd.read_excel(input_data, na_values=missing_values)
    else:
        raise ValueError("Unsupported file type. Please provide a .csv or .xlsx file.")
