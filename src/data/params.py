params_tles = {
    "format_text": {
        "format": "text"
    },

    "invalid_format": {
        "format": 'html'
    },

    "empty_format": {
        "format": ''
    }
}


params_positions = {
    "valid_timestamp": {
        "timestamps": "1627496882"
    },

    "valid_timestamp_1": {
        "timestamps": "0.9"
    },

    "decimal_based_timestamp": {
        "timestamps": "2000.2000"
    },

    "invalid_timestamp": {
        "timestamps": "-1627496882"
    },

    "invalid_timestamp_2": {
        "timestamps": "XXXXXXXXXXXXXXX"
    },

    "invalid_timestamp_3": {
        "timestamps": "      "
    },

    "empty_timestamp": {
        "timestamps": ""
    },

    "one_timestamp": {
        "timestamps": "2027496882"
    },

    "ten_timestamps": {
        "timestamps":  "1627496882, 1637496882, 1727496882, 1677496882, 1827496882, 1697496862, 1347496882, 1627496002, 1997496882, 2027496882"
    },

    "eleven_timestamps": {
        "timestamps":  "1627496882, 1637496882, 1727496882, 1677496882, 1827496882, 1697496862, 1347496882, 1627496002, 1997496882, 2027496882, 2027496882"
    },

    "past_timestamp": {
        "timestamps": "1027802661",
    },

    "future_timestamp": {
        "timestamps": "1727802661",
    },

    "custom_unit": {
        "timestamps": "8900",
        "units": "miles"
    },

    "daylight_position": {
        "timestamps": "890011"
    },

    "eclipsed_position": {
        "timestamps": "90000000"
    }
}