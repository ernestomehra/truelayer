from src.data.params import params_positions
from src.helpers.utils import *
import pytest


class TestPositions:
    """
    Test suite for sanity testing the API endpoint: satellites/[id]/positions
    - Tier 1: tag to run only the critical tests
    - Tier 2: tag to run critical and high priority tests
    """

    endpoint = "positions"

    # TC: 01
    def test_sat_positions_response(self):
        response = get_data(self.endpoint, params=params_positions["valid_timestamp"])
        json_response = get_json_data(response)
        assert response.status_code == 200
        result = []
        expected_keys = [
                            "name",
                            "id",
                            "latitude",
                            "longitude",
                            "altitude",
                            "velocity",
                            "visibility",
                            "footprint",
                            "timestamp",
                            "daynum",
                            "solar_lat",
                            "solar_lon",
                            "units"
                        ]
        for key in json_response[0]:
            result.append(key)
        assert sorted(result) == sorted(expected_keys), 'Actual API Response does not match the expected API response'

    # TC: 02
    def test_positions_response_headers(self):
        response = get_data(self.endpoint, params=params_positions["valid_timestamp"])
        assert response.status_code == 200
        expected_keys = ['Server', 'Connection', 'X-Powered-By', 'Access-Control-Allow-Origin', 'Content-Type',
                         'Content-Length', 'X-Apache-Time', 'Date', 'Keep-Alive', 'Cache-Control',
                         'X-Rate-Limit-Remaining', 'X-Rate-Limit-Interval', 'X-Rate-Limit-Limit']

        result = []
        for key in response.headers.keys():
            if key in expected_keys:
                result.append(key)
        assert sorted(result) == sorted(expected_keys), 'Returned headers do not match the expected headers.'

    # TC: 03
    def test_positions_allowed_methods(self):
        response = get_data(self.endpoint, params=params_positions["valid_timestamp"])
        assert response.status_code == 200

    # TC: 04
    def test_positions_disallowed_methods(self):
        response = post_data(self.endpoint)
        json_response = get_json_data(response)
        assert json_response["error"] == "authorization required"
        assert json_response["status"] == 401

    # TC: 05
    def test_positions_empty_timestamp(self):
        response = get_data(self.endpoint, params=params_positions["empty_timestamp"])
        assert response.status_code == 400
        json_response = get_json_data(response)
        assert json_response["error"] == "invalid timestamp in list: "

    def test_positions_no_timestamp(self):
        response = get_data(self.endpoint)
        assert response.status_code == 400
        json_response = get_json_data(response)
        assert json_response["error"] == "invalid timestamp in list: "

    def test_positions_valid_timestamp(self):
        response = get_data(self.endpoint, params=params_positions["valid_timestamp"])
        assert response.status_code == 200

    def test_positions_valid_timestamp_1(self):
        response = get_data(self.endpoint, params=params_positions["valid_timestamp_1"])
        assert response.status_code == 200

    def test_positions_valid_decimal_based_timestamp(self):
        response = get_data(self.endpoint, params=params_positions["decimal_based_timestamp"])
        assert response.status_code == 200

    # Negative epoch timestamp
    def test_positions_invalid_timestamp(self):
        response = get_data(self.endpoint, params=params_positions["invalid_timestamp"])
        assert response.status_code == 400
        json_response = get_json_data(response)
        assert json_response["error"] == f"invalid timestamp in list: {params_positions['invalid_timestamp']['timestamps']}"

    def test_positions_invalid_timestamp_2(self):
        response = get_data(self.endpoint, params=params_positions["invalid_timestamp_2"])
        assert response.status_code == 400
        json_response = get_json_data(response)
        assert json_response["error"] == f"invalid timestamp in list: {params_positions['invalid_timestamp_2']['timestamps']}"

    def test_positions_invalid_timestamp_3(self):
        response = get_data(self.endpoint, params=params_positions["invalid_timestamp_3"])
        assert response.status_code == 400
        json_response = get_json_data(response)
        assert json_response["error"] == f"invalid timestamp in list: {params_positions['invalid_timestamp_3']['timestamps']}"

    # Boundary value analysis
    def test_positions_one_timestamp(self):
        response = get_data(self.endpoint, params=params_positions["one_timestamp"])
        assert response.status_code == 200
        json_response = get_json_data(response)
        assert json_response[0]["timestamp"] == int(params_positions["one_timestamp"]["timestamps"])

    # Boundary value analysis
    @pytest.mark.tier1
    def test_positions_ten_timestamps(self):
        response = get_data(self.endpoint, params=params_positions["ten_timestamps"])
        assert response.status_code == 200
        json_response = get_json_data(response)
        assert len(json_response) == 10

    # Boundary value analysis
    def test_positions_eleven_timestamps(self):
        response = get_data(self.endpoint, params=params_positions["eleven_timestamps"])
        assert response.status_code == 200
        json_response = get_json_data(response)
        assert len(json_response[0]) == 10  # This is what I expect, since the documentation is incorrect,
        # expected result should be defined properly because currently 10 is not a limit to timestamps
        # and the documentation needs to be corrected or bug needs to be fixed (if the document is correct).

    # Reference: Current EPOCH Time = 1627802661
    def test_positions_past_timestamp(self):
        response = get_data(self.endpoint, params=params_positions["past_timestamp"])
        assert response.status_code == 200

    def test_positions_future_timestamp(self):
        response = get_data(self.endpoint, params=params_positions["future_timestamp"])
        assert response.status_code == 200

    def test_positions_invalid_iss_id(self):
        response = get_data(self.endpoint, iss="5", params=params_positions["past_timestamp"])
        assert response.status_code == 404
        json_response = get_json_data(response)
        assert json_response["error"] == "satellite not found"

    def test_positions_default_unit(self):
        response = get_data(self.endpoint, params=params_positions["valid_timestamp"])
        assert response.status_code == 200
        json_response = get_json_data(response)
        assert json_response[0]["units"] == "kilometers"

    def test_positions_custom_unit(self):
        response = get_data(self.endpoint, params=params_positions["custom_unit"])
        assert response.status_code == 200
        json_response = get_json_data(response)
        assert json_response[0]["units"] == "miles"

    def test_daylight_positions(self):
        response = get_data(self.endpoint, params=params_positions["daylight_position"])
        assert response.status_code == 200
        json_response = get_json_data(response)
        assert json_response[0]["visibility"] == "daylight"

    def test_night_positions(self):
        response = get_data(self.endpoint, params=params_positions["eclipsed_position"])
        assert response.status_code == 200
        json_response = get_json_data(response)
        assert json_response[0]["visibility"] == "eclipsed"










