from src.data.params import params_positions
from src.helpers.utils import *


class TestPositions:
    """
    Test suite for sanity testing the API endpoint: satellites/[id]/positions
    - Tier 1: tag to run only the critical tests
    - Tier 2: tag to run critical and high priority tests
    """

    endpoint = "positions"

    # TC: 01 - Check that the satellite position API response returned is as expected.
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

    # TC: 02 - Check the headers returned are as expected.
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

    # TC: 03 - Test HTTP methods on the API that are allowed
    def test_positions_allowed_methods(self):
        response = get_data(self.endpoint, params=params_positions["valid_timestamp"])
        assert response.status_code == 200

    # TC: 04 - Check HTTP methods on the API that are not allowed.
    def test_positions_disallowed_methods(self):
        response = post_data(self.endpoint)
        json_response = get_json_data(response)
        assert json_response["error"] == "authorization required"
        assert json_response["status"] == 401

    # TC: 05 - Check sending an empty timestamp, blank timestamp param.
    def test_positions_empty_timestamp(self):
        response = get_data(self.endpoint, params=params_positions["empty_timestamp"])
        assert response.status_code == 400
        json_response = get_json_data(response)
        assert json_response["error"] == "invalid timestamp in list: "

    # TC: 06 - Check sending param timestamp but '' an empty test string.
    def test_positions_no_timestamp(self):
        response = get_data(self.endpoint)
        assert response.status_code == 400
        json_response = get_json_data(response)
        assert json_response["error"] == "invalid timestamp in list: "

    # TC: 07 - Check happy path, find response for valid epoch timestamp
    def test_positions_valid_timestamp(self):
        response = get_data(self.endpoint, params=params_positions["valid_timestamp"])
        assert response.status_code == 200

    # TC: 08 - Check variation of another valid timestamp, 0.9 in this case.
    def test_positions_valid_timestamp_1(self):
        response = get_data(self.endpoint, params=params_positions["valid_timestamp_1"])
        assert response.status_code == 200

    # TC: 09 - Check floating point timestamp param
    def test_positions_valid_decimal_based_timestamp(self):
        response = get_data(self.endpoint, params=params_positions["decimal_based_timestamp"])
        assert response.status_code == 200

    # Negative epoch timestamp Scenarios
    # TC: 10 - Check response received for timestamp param as a negative value
    def test_positions_invalid_timestamp(self):
        response = get_data(self.endpoint, params=params_positions["invalid_timestamp"])
        assert response.status_code == 400
        json_response = get_json_data(response)
        assert json_response["error"] == f"invalid timestamp in list: {params_positions['invalid_timestamp']['timestamps']}"

    # TC: 11 - Check response received for invalid timestamp <XXXXXXX>
    def test_positions_invalid_timestamp_2(self):
        response = get_data(self.endpoint, params=params_positions["invalid_timestamp_2"])
        assert response.status_code == 400
        json_response = get_json_data(response)
        assert json_response["error"] == f"invalid timestamp in list: {params_positions['invalid_timestamp_2']['timestamps']}"

    # TC: 12 - Check response received for invalid timestamp <    >, spaces.
    def test_positions_invalid_timestamp_3(self):
        response = get_data(self.endpoint, params=params_positions["invalid_timestamp_3"])
        assert response.status_code == 400
        json_response = get_json_data(response)
        assert json_response["error"] == f"invalid timestamp in list: {params_positions['invalid_timestamp_3']['timestamps']}"

    # Boundary value analysis
    # TC: 13 - Check response received for one timestamp param
    def test_positions_one_timestamp(self):
        response = get_data(self.endpoint, params=params_positions["one_timestamp"])
        assert response.status_code == 200
        json_response = get_json_data(response)
        assert json_response[0]["timestamp"] == int(params_positions["one_timestamp"]["timestamps"])

    # TC: 14 - Check response received for ten timestamps, which is a limit as per documentation
    def test_positions_ten_timestamps(self):
        response = get_data(self.endpoint, params=params_positions["ten_timestamps"])
        assert response.status_code == 200
        json_response = get_json_data(response)
        assert len(json_response) == 10

    # TC: 15 - Check response received for eleven timestamps, which is a limit as per documentation
    def test_positions_eleven_timestamps(self):
        response = get_data(self.endpoint, params=params_positions["eleven_timestamps"])
        assert response.status_code == 200
        json_response = get_json_data(response)
        assert len(json_response[0]) == 10  # This is what I expect, since the documentation is incorrect,
        # expected result should be defined properly because currently 10 is not a limit to timestamps
        # and the documentation needs to be corrected or bug needs to be fixed (if the document is correct).

    # Timestamp Reference for following cases: Current EPOCH Time = 1627802661
    # TC: 16 - Check iss response for past timestamp
    def test_positions_past_timestamp(self):
        response = get_data(self.endpoint, params=params_positions["past_timestamp"])
        assert response.status_code == 200

    # TC: 17 - Check iss response for future timestamp
    def test_positions_future_timestamp(self):
        response = get_data(self.endpoint, params=params_positions["future_timestamp"])
        assert response.status_code == 200

    # TC: 18 - Check iss response for an invalid iss id
    def test_positions_invalid_iss_id(self):
        response = get_data(self.endpoint, iss="5", params=params_positions["past_timestamp"])
        assert response.status_code == 404
        json_response = get_json_data(response)
        assert json_response["error"] == "satellite not found"

    # TC: 19 - Check default unit for response received is kilometers.
    def test_positions_default_unit(self):
        response = get_data(self.endpoint, params=params_positions["valid_timestamp"])
        assert response.status_code == 200
        json_response = get_json_data(response)
        assert json_response[0]["units"] == "kilometers"

    # TC: 20 - Check custom unit miles is returned when explicitly defined in the payload.
    def test_positions_custom_unit(self):
        response = get_data(self.endpoint, params=params_positions["custom_unit"])
        assert response.status_code == 200
        json_response = get_json_data(response)
        assert json_response[0]["units"] == "miles"

    # TC: 21 - Check position daylight is returned for the relevant timestamp
    def test_daylight_positions(self):
        response = get_data(self.endpoint, params=params_positions["daylight_position"])
        assert response.status_code == 200
        json_response = get_json_data(response)
        assert json_response[0]["visibility"] == "daylight"

    # TC: 22 - Check position eclipsed is returned for the relevant timestamp
    def test_night_positions(self):
        response = get_data(self.endpoint, params=params_positions["eclipsed_position"])
        assert response.status_code == 200
        json_response = get_json_data(response)
        assert json_response[0]["visibility"] == "eclipsed"
