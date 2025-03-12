import json
import requests


def lambda_handler(event, context):
    url = event.get("url", "https://jsonplaceholder.typicode.com/posts/1")
    expected_status = event.get("expected_status", 200)

    try:
        response = requests.get(url)
        status_code = response.status_code
        body = response.json()

        if status_code == expected_status:
            result = "Success"
        else:
            result = "Failure"

        return {
            "statusCode": status_code,
            "body": json.dumps({
                "result": result,
                "url": url,
                "response": body
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
