import os
import unittest
import pandas as pd
from random import randint
from whatsapp_parser.parser import parse_line, chat_to_dataframe, group_conversations_by_time


class TestParser(unittest.TestCase):

    def test_parse_line_with_new_message(self):
        line = "6/13/22, 7:07 AM - John Doe: Merry Christmas!"
        expected_result = {
            'datetime': '6/13/22, 7:07 AM',
            'author': 'John Doe',
            'message': 'Merry Christmas!',
            'new_message': True
        }
        self.assertEqual(parse_line(line), expected_result)

    def test_parse_line_with_continuation(self):
        line = "This message continues the previous one."
        expected_result = {
            'message': line,
            'new_message': False
        }
        self.assertEqual(parse_line(line), expected_result)

    def test_chat_to_dataframe(self):
        text = [
            "1/16/23, 10:02 PM - John Doe: Merry Christmas!",
            "This message continues the previous one.",
            "1/16/23, 10:48 PM - Jane Doe: Happy Boxing Day!"
        ]
        df = chat_to_dataframe(text)
        self.assertEqual(len(df), 2)
        self.assertIn('This message continues the previous one.',
                      df.loc[0, 'message'])

    def test_group_conversations_by_time(self):
        data = {
            'datetime': pd.to_datetime(['2020-12-25 20:30', '2020-12-25 20:35', '2020-12-25 20:50']),
            'message': ['Message 1', 'Message 2', 'Message 3']
        }
        df = pd.DataFrame(data)
        group_conversations_by_time(df)
        self.assertEqual(df.loc[0, 'conversation_id'], 1)
        self.assertEqual(df.loc[1, 'conversation_id'], 1)
        self.assertEqual(df.loc[2, 'conversation_id'], 2)

    def test_full_pipeline_input(self):
        directory_path = './tests/data'

        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            self.assertTrue(os.path.isfile(file_path))
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.readlines()
            df = chat_to_dataframe(text)
            time_threshold_s = randint(5, 10) * 60
            group_conversations_by_time(df, time_threshold_s)
            conversation_count = df['conversation_id'].nunique()
            for i in range(1, conversation_count):
                group_1 = df[df['conversation_id'] == i]
                group_2 = df[df['conversation_id'] == i + 1]
                self.assertTrue(len(group_1) > 0, i)
                self.assertTrue(len(group_2) > 0, i)
                time_diff = group_2.iloc[0]['datetime'] - group_1.iloc[-1]['datetime']
                self.assertTrue(time_diff.total_seconds() > time_threshold_s, f'\nGroup_1\n{group_1}\nGroup_2\n{group_2}\nTime\t{time_diff}\t{time_diff.total_seconds()}')


if __name__ == '__main__':
    unittest.main()
