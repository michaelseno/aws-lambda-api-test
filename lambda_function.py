import json
import logging
from src.utils import read_file
from src.api_request import run_tests
from src.notification_service import NotificationService

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
sns = NotificationService()


def lambda_handler(event, context):
    try:
        if "test_cases" in event:
            test_cases = event["test_cases"]
        else:
            test_cases = read_file()

        results = run_tests(test_cases=test_cases)
        logger.info("Test results: %s", json.dumps(results, indent=2))

        success_count = sum(1 for r in results if r["test_result"] == "Passed")
        failure_count = sum(1 for r in results if r["test_result"] == "Failed")
        summary = (f"API Test Completed: "
                   f"{success_count} Passed, {failure_count} Failed")
        sns.publish(subject="API Test Results", message=summary)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "API Test Completed",
                "results": results,
            })
        }

    except Exception as e:
        logger.error("Error during Lambda execution: %s", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
