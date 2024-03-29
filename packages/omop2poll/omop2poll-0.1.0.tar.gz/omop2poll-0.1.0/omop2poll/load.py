import pandas as pd
import os


def load_survey_data(filename='healthcare_survey.csv'):
    """
    Reads survey data from a CSV file.

    :param filename: The path to the CSV file containing the survey data.
    :return: A pandas DataFrame containing the loaded survey data.
    """
    current_dir = os.path.dirname(os.path.realpath(__file__))

    file_path = os.path.join(current_dir,  filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File path {file_path} does not exist.")
    return pd.read_csv(file_path)

