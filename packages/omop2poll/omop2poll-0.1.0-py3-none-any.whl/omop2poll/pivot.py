import pandas as pd
import os


def pivot_data_numeric(filename):
    if not os.path.exists(filename):
        print(f"The specified file {filename} does not exist.")
        return
    """
    Loads a dataset, pivots it to have questions as columns with 'q' prefixed to question IDs and numeric answers as values,
    and saves the pivoted dataset to a new CSV file.

    Parameters:
    - filename: The name (and path, if not in the current directory) of the dataset file to load.

    The function will save the pivoted dataset with a prefixed name 'pivoted_' in the same directory.
    """
    data = pd.read_csv(filename)
    pivot_df = data.pivot_table(index='respondent_id',
                                columns='question_concept_id',
                                values='answer_numeric',
                                aggfunc='first')

    pivot_df.columns = ['q' + str(col) for col in pivot_df.columns]
    new_filename = 'pivot_n_' + filename.split('/')[-1]
    pivot_df.to_csv(new_filename)

    print(f"Pivoted dataset with numeric values saved as: {new_filename}")


def pivot_data_text(filename):
    if not os.path.exists(filename):
        print(f"The specified file {filename} does not exist.")
        return
    """
    Loads a dataset, pivots it to have questions as columns with 'q' prefixed to question IDs and numeric answers as values,
    and saves the pivoted dataset to a new CSV file.

    Parameters:
    - filename: The name (and path, if not in the current directory) of the dataset file to load.

    The function will save the pivoted dataset with a prefixed name 'pivoted_' in the same directory.
    """
    data = pd.read_csv(filename)
    pivot_df = data.pivot_table(index='respondent_id',
                                columns='question_concept_id',
                                values='answer_text',
                                aggfunc='first')

    pivot_df.columns = ['q' + str(col) for col in pivot_df.columns]
    new_filename = 'pivot_t_' + filename.split('/')[-1]
    pivot_df.to_csv(new_filename)

    print(f"Pivoted dataset with text values saved as: {new_filename}")
