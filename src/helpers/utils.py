import requests


def get_data(url, params):
    data = requests.get(url=url, params=params)
    return data


def get_json_data(response, key):
    return response.json()[key]