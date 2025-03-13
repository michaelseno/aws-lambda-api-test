import json
import requests
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    results = []

    # Check for the 'events' key and ensure it's a list
    events = event.get("events", [])
    if not isinstance(events, list):
        logger.error("Invalid input format. Expected 'events' to be a list.")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid input format"})
        }

    logger.info(f"Received {len(events)} events.")

    for i, single_event in enumerate(events):
        url = single_event.get("url", single_event.get("url"))
        expected_status = single_event.get("expected_status", single_event.get("expected_status"))

        logger.info(f"Processing event {i + 1}/{len(events)}")
        logger.info(f"Requesting URL: {url}")

        try:
            response = requests.get(url)
            status_code = response.status_code
            body = response.json()

            logger.info(f"Response status code: {status_code}")
            logger.info(f"Response body: {json.dumps(body)}")

            result = "Success" if status_code == expected_status else "Failure"
            logger.info(f"Result for event {i + 1}: {result}")
            results.append({
                "statusCode": status_code,
                "body": {
                    "result": result,
                    "url": url,
                    "response": body
                }
            })

        except Exception as e:
            logger.error(f"Error occurred in event {i + 1}: {str(e)}")
            results.append({
                "statusCode": 500,
                "body": {"error": str(e)}
            })

    return {
        "statusCode": 200,
        "body": json.dumps({"results": results})
    }

