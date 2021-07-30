from src.data.params import params_positions
from src.helpers.utils import *
from src.helpers.environment import TestEnvironment as env
import pytest


class TestPositions:
    """
    Test suite for sanity testing the API endpoint: satellites/[id]/positions
    - Tier 1: tag to run only the critical tests
    - Tier 2: tag to run critical and high priority tests
    """

    endpoint = "positions"

    @pytest.mark.tier1
    @pytest.mark.tier2
    def test_sat_positions_response(self):
        response = get_data(env.URL, params=params_positions["valid_timestamp"])
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
        for key in json_response:
            result.append(key)
        assert sorted(result) == sorted(expected_keys), 'Actual API Response does not match the expected API response'

    @pytest.mark.tier1
    def test_positions_response_headers(self):
        response = get_data(env.URL, params=params_positions["valid_timestamp"])
        assert response.status_code == 200

        

    @pytest.mark.tier2
    def test_positions_allowed_methods(self):
        pass

    def test_positions_disallowed_methods(self):
        pass

    def test_positions_empty_timestamp(self):
        pass

    def test_positions_valid_timestamp(self):
        pass

    # Negative epoch timestamp
    def test_positions_invalid_timestamp(self):
        pass

    # Boundary value analysis
    def test_positions_one_timestamp(self):
        pass

    # Boundary value analysis
    def test_positions_ten_timestamps(self):
        pass

    # Boundary value analysis
    def test_positions_eleven_timestamps(self):
        pass

    def test_positions_timestamp_custom_timezone(self):
        pass

    def test_positions_past_timestamp(self):
        pass

    def test_positions_future_timestamp(self):
        pass

    def test_positions_invalid_iss_id(self):
        pass

    def test_positions_default_unit(self):
        pass

    def test_positions_custom_unit(self):
        pass










