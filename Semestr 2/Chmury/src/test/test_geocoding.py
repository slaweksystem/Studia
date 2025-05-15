import pytest
from unittest.mock import patch
from ..main.python.geocoding import get_lat_long

@pytest.mark.parametrize(
    "country, city, address, expected_output",
    [
        ('USA', 'New York', 'Statue of Liberty', (40.6892, -74.0445)),
        ('USA', 'San Francisco', 'Golden Gate Bridge', (37.8199, -122.4783)),
        ('InvalidCountry', 'NoCity', 'NoAddress', (None, None)),
    ]
)
@patch("requests.get")
def test_get_lat_long(mock_get, country, city, address, expected_output):
    # Setup mock response data
    if expected_output == (None, None):
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {"total_results": 0}
    else:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "total_results": 1,
            "results": [{
                "geometry": {
                    "lat": expected_output[0],
                    "lng": expected_output[1]
                }
            }]
        }

    # Call the function
    result = get_lat_long(country, city, address, "fake_api_key")

    # Asserts
    assert result == expected_output
    mock_get.assert_called_once()