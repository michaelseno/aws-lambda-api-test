import unittest
from unittest.mock import patch, MagicMock
from lambda_function import lambda_handler
from src.utils import read_file


class TestLambdaFunction(unittest.TestCase):
    @patch('requests.get')
    def test_lambda_handler_success(self, mock_get):
        """Test successful API request."""
        # Arrange: Mock the `requests.get` response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Success"}
        mock_get.return_value = mock_response

        events = {"events": []}

        for data in read_file():
            if 'success' in data['use_case']:
                events['events'].append(data)
                context = {}

                result = lambda_handler(events, context)

                # Assert: Check the status code and response body
                self.assertEqual(result['statusCode'], 200)
                self.assertIn("Success", result['body'])

    @patch('requests.get')
    def test_lambda_handler_failure(self, mock_get):
        """Test failed API request (404 error)."""
        # Arrange: Mock the `requests.get` response for failure
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": "Not Found"}
        mock_get.return_value = mock_response

        events = {"events": []}

        for data in read_file():
            if 'failure' in data['use_case']:
                events['events'].append(data)

                context = {}

                result = lambda_handler(events, context)

                # Assert: Check the status code and error message
                self.assertEqual(result['statusCode'], 404)
                self.assertIn("Not Found", result['body'])

    @patch('requests.get')
    def test_lambda_handler_exception(self, mock_get):
        """Test when an exception occurs during the request."""
        # Arrange: Mock `requests.get` to raise an exception
        mock_get.side_effect = Exception("Request failed")

        events = {"events": []}
        for data in read_file():
            if 'success' in data['use_case']:
                events['events'].append(data)
                break

        context = {}

        # Act: Call the Lambda function
        result = lambda_handler(events, context)

        # Assert: Check if error is handled properly
        self.assertEqual(result['statusCode'], 500)
        self.assertIn("Request failed", result['body'])


if __name__ == "__main__":
    # You can set verbosity to 2 for more detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
