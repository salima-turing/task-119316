import json
import unittest
from unittest.mock import patch, Mock

import pandas as pd

def process_data_stream(event, context):
    data = json.loads(event['body'])
    df = pd.DataFrame(data)
    average = df['value'].mean()
    result = {
        "average": average
    }
    return json.dumps(result)


class TestDataStreamProcessor(unittest.TestCase):

    def test_in_memory_processing(self):
        test_data = [{"value": 1}, {"value": 2}, {"value": 3}]
        df = pd.DataFrame(test_data)
        expected_average = 2.0

        result = json.loads(process_data_stream({'body': df.to_json(orient='records')}, None))
        self.assertEqual(result['average'], expected_average)

    @patch('your_module.external_service_call')
    def test_mocked_external_service(self, mock_service_call):
        mock_service_call.return_value = [{"value": 4}, {"value": 5}]
        test_event = {
            "body": json.dumps({"some": "input"})
        }
        result = json.loads(process_data_stream(test_event, None))
        self.assertEqual(result['average'], 4.5)


if __name__ == '__main__':
    unittest.main()
