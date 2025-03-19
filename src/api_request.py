import time
import uuid

import requests


def fetch_data(url):
    try:
        start = time.time()
        response = requests.get(url)
        end = time.time()
        response_time = int((end - start) * 1000)
        return {
            "status_code": response.status_code,
            "response_time": response_time
        }
    except Exception as e:
        return {
            "status_code": 500,
            "response_time": 0,
            "error_message": str(e)
        }


def run_tests(test_cases):
    results = []
    err = ""
    for test_case in test_cases:
        response = fetch_data(test_case["url"])
        test_result = "Passed" if response["status_code"] == test_case["expected_status"] else "Failed"
        if "Passed" in test_result:
            err = "N/A"
        else:
            err = response["error_message"]
        result = {
            "test_id": str(uuid.uuid4()),
            "test_case": test_case["use_case"],
            "url": test_case["url"],
            "expected_status": test_case["expected_status"],
            "actual_status": response["status_code"],
            "test_result": test_result,
            "response_time": response["response_time"],
            "error": err
        }
        results.append(result)
    return results
