import requests
from src.helpers.environment import TestEnvironment as env


def get_data(relative_path, iss='25544', params=None):
    """

    :param relative_path: pass the endpoint url only
    :param iss: by default set to iss, but user can pass other values to check negative tests
    :param params: only one parameter is accepted, format=text or json(default), check params.py for examples used
    :return: return API response object as is received from the API
    """
    data = requests.get(env.URL + iss + '/' + relative_path, params=params)
    return data


def get_json_data(response):
    """

    :param response: consumes API response object
    :return: return json format response object
    """
    return response.json()


def post_data(relative_path, iss='25544'):
    """

    :param relative_path: endpoint of the url to be tested
    :param iss: by default set to iss, but user can pass other values to check negative tests
    :return: return response received from hitting a POST request
    """
    data = requests.post(env.URL + iss + '/' + relative_path)
    return data
