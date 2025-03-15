import requests


def fetch_data(url):
    """Fetch data from a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        return {"status_code": response.status_code, "body": response.json()}
    except requests.RequestException as e:
        return {"error": str(e)}
