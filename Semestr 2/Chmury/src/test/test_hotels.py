import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, Row
from pyspark.sql.functions import col
from unittest.mock import patch
from ..main.python.hotels import fill_missing_hotel_coords

@pytest.fixture(scope="module")
def spark_session():
    return SparkSession.builder \
        .master("local[1]") \
        .appName("GeocodingTest") \
        .getOrCreate()

def create_test_dataframe(spark_session):
    schema = StructType([
        StructField("Id", StringType(), True),
        StructField("Country", StringType(), True),
        StructField("City", StringType(), True),
        StructField("Address", StringType(), True),
        StructField("Latitude", DoubleType(), True),
        StructField("Longitude", DoubleType(), True)
    ])
    
    data = [
        Row("1", "France", "Paris", "Eiffel Tower", 48.8584, 2.2945),
        Row("2", "USA", "San Francisco", "Golden Gate Bridge", None, None)
    ]
    
    return spark_session.createDataFrame(data, schema)

@patch("src.main.python.hotels.get_lat_long")
def test_fill_missing_hotel_coords(mock_get_lat_long, spark_session):
    # Create the test DataFrame
    test_df = create_test_dataframe(spark_session)
    
    # Set up the mock response for the geocoding UDF
    mock_get_lat_long.return_value = (37.8199, -122.4783)

    # Define the expected DataFrame
    expected_data = [
        Row("1", "France", "Paris", "Eiffel Tower", 48.8584, 2.2945),
        Row("2", "USA", "San Francisco", "Golden Gate Bridge", 37.8199, -122.4783)
    ]
    expected_df = spark_session.createDataFrame(expected_data, test_df.schema)

    # Invoke the function under test
    result_df = fill_missing_hotel_coords(test_df, "fake_api_key")

    # Sort both DataFrames by ID for consistent ordering
    result_df = result_df.orderBy("Id")
    expected_df = expected_df.orderBy("Id")

    # Assert that the result DataFrame matches the expected DataFrame
    assert result_df.collect() == expected_df.collect()