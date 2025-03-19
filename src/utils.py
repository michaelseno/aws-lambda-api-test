import json
import os


def read_file():
    filepath = os.path.join(os.getcwd(), 'events', 'event.json')
    with open(filepath) as file:
        data = json.load(file)
        return data['test_cases']
