import pandas as pd


def create_codebook(df):
    codebook_df = df[['question_concept_id', 'question', 'answer_concept_id', 'answer_numeric', 'answer_text']]
    codebook_df = codebook_df.drop_duplicates().sort_values(by='question_concept_id')
    return codebook_df


def print_codebook(codebook_df):
    try:
        from tabulate import tabulate
        print(tabulate(codebook_df, headers='keys', tablefmt='psql', showindex=False))
    except ImportError:
        with pd.option_context('display.max_rows', None,
                               'display.max_columns', None,
                               'display.max_colwidth', None,
                               'display.width', 1000):
            print(codebook_df)
