import unittest
import os
import pandas as pd
from omop2poll.pivot import pivot_data_text, pivot_data_numeric

test_data_numeric = {
    'respondent_id': [1, 2, 1, 2],
    'question_concept_id': [101, 101, 102, 102],
    'answer_numeric': [1, 2, 1, 2]
}

test_data_text = {
    'respondent_id': [1, 2, 1, 2],
    'question_concept_id': [101, 101, 102, 102],
    'answer_text': ['Yes', 'No', 'Maybe', 'Yes']
}


class TestPivot(unittest.TestCase):
    test_filename_numeric = 'test_numeric.csv'
    test_filename_text = 'test_text.csv'

    @classmethod
    def setUpClass(cls):
        pd.DataFrame(test_data_numeric).to_csv(cls.test_filename_numeric, index=False)
        pd.DataFrame(test_data_text).to_csv(cls.test_filename_text, index=False)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.test_filename_numeric)
        os.remove(cls.test_filename_text)
        os.remove('pivot_n_' + cls.test_filename_numeric)
        os.remove('pivot_t_' + cls.test_filename_text)

    def test_pivot_data_numeric(self):
        pivot_data_numeric(self.test_filename_numeric)
        self.assertTrue(os.path.exists('pivot_n_' + self.test_filename_numeric))

    def test_pivot_data_text(self):
        pivot_data_text(self.test_filename_text)
        self.assertTrue(os.path.exists('pivot_t_' + self.test_filename_text))

        # Add more tests here to check for the content and correctness of the pivoted files


if __name__ == '__main__':
    unittest.main()
