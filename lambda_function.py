import json
import requests
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    results = []

    # Check if the event is a list of multiple events
    if isinstance(event, list):
        logger.info(f"Received multiple events: {len(event)}")
        events = event
    else:
        logger.info("Received single event")
        events = [event]

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

            if status_code == expected_status:
                result = "Success"
                logger.info(f"Status check successful for event {i + 1}")
            else:
                result = "Failure"
                logger.warning(f"Status check failed for event {i + 1} - url: {url}. Expected {expected_status}, got {status_code}")

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

