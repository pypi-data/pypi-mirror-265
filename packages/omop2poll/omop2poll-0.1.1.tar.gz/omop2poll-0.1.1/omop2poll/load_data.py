import pandas as pd
import os


def load_survey_data(filename='survey.csv'):
    current_dir = os.path.dirname(os.path.realpath(__file__))

    file_path = os.path.join(current_dir,  filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File path {file_path} does not exist.")
    return pd.read_csv(file_path)