import pandas as pd
from omop2poll.load_data import load_survey_data


def map_responses(input_data):
    survey_data = load_survey_data()

    mapping_numeric = survey_data.groupby('question_concept_id').apply(
        lambda x: dict(zip(x['answer_concept_id'], x['answer_numeric']))).to_dict()

    mapping_text = survey_data.groupby('question_concept_id').apply(
        lambda x: dict(zip(x['answer_concept_id'], x['answer_text'].str.strip()))).to_dict()

    input_data['answer_numeric'] = None
    input_data['answer_text'] = None

    for idx, row in input_data.iterrows():
        question_id = row['question_concept_id']
        answer_id = row['answer_concept_id']

        input_data.at[idx, 'answer_numeric'] = mapping_numeric.get(question_id, {}).get(answer_id, None)
        input_data.at[idx, 'answer_text'] = mapping_text.get(question_id, {}).get(answer_id, None)

        if isinstance(input_data.at[idx, 'answer_text'], (int, float)):
            input_data.at[idx, 'answer_text'] = str(input_data.at[idx, 'answer_text'])
        elif isinstance(input_data.at[idx, 'answer_text'], str) and input_data.at[idx, 'answer_text'].isdigit():
            pass

    return input_data
