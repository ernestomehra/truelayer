from src.helpers.utils import *
from src.data.params import params_tles


class TestTLE:
    """
    Test suite for sanity testing the TLE data returned for the endpoint: satellites/[id]/tles
    """
    endpoint = "tles"

    # TC: 01 - Check happy response returned for all valid params.
    def test_tle_response(self):
        response = get_data(self.endpoint)
        assert response.status_code == 200, 'Status code returned is not 200 OK'
        json_response = get_json_data(response)
        expected_keys = [
            "requested_timestamp",
            "tle_timestamp",
            "id",
            "name",
            "header",
            "line1",
            "line2"
        ]
        result = []
        for key in json_response.keys():
            result.append(key)

        assert result == expected_keys, 'Keys do not match the expected list in the response returned'

    # TC: 02 - Check headers returned for all valid params.
    def test_tle_headers(self):
        response = get_data(self.endpoint)
        expected_keys = ['Server', 'Connection', 'X-Powered-By', 'Access-Control-Allow-Origin', 'Content-Type',
                         'Content-Length', 'X-Apache-Time', 'Date', 'Keep-Alive', 'Cache-Control',
                         'X-Rate-Limit-Remaining', 'X-Rate-Limit-Interval', 'X-Rate-Limit-Limit']
        result = []
        for key in response.headers.keys():
            if key in expected_keys:
                result.append(key)
        assert sorted(result) == sorted(expected_keys), 'Returned headers do not match the expected headers.'

    # TC: 03 - Check default format returned is JSON
    def test_tle_default_format(self):
        response = get_data(self.endpoint)
        json_response = response.headers
        assert json_response["Content-Type"] == "application/json", 'Json format not returned'

    # TC: 04 - Check custom format is text/plain can be returned from the API
    def test_tle_custom_format(self):
        response = get_data(self.endpoint, params=params_tles["format_text"])
        json_response = response.headers
        assert json_response["Content-Type"] == "text/plain", 'Text format of the response not returned'

    # TC: 05 - Check invalid format param is handled well. Defaulted to JSON
    def test_tle_invalid_format(self):
        response = get_data(self.endpoint, params=params_tles["invalid_format"])
        json_response = response.headers
        assert json_response["Content-Type"] == "application/json", 'Default format - json not returned'

    # TC 06 - Check empty format param is handled, JSON should be returned
    def test_tle_empty_format(self):
        response = get_data(self.endpoint, params=params_tles["empty_format"])
        json_response = response.headers
        assert json_response["Content-Type"] == "application/json", 'Default format - json not returned'

    # TC 07 - Check response received for invalid iss id
    def test_tle_invalid_iss_id(self):
        response = get_data(self.endpoint, '0000', params=params_tles["empty_format"])
        json_response = response.json()
        assert response.status_code == 404
        assert json_response["error"] == "satellite not found", 'Error message not returned correctly'

    # TC 08 - Negative test to check returned error for methods not allowed.
    def test_disallowed_methods(self):
        response = post_data(self.endpoint)
        json_response = get_json_data(response)
        assert json_response["error"] == "authorization required"


