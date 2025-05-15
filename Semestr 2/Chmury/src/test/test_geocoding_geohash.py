import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, FloatType, Row
from ..main.python.geocoding import add_geohash

@pytest.fixture(scope="module")
def spark_session():
    return SparkSession.builder \
        .master("local[1]") \
        .appName("GeocodingTest") \
        .getOrCreate()

def test_add_geohash(spark_session):
    # Define schema for the test DataFrame
    schema = StructType([
        StructField("Id", StringType(), True),
        StructField("Latitude", FloatType(), True),
        StructField("Longitude", FloatType(), True)
    ])
    
    # Create test data
    data = [
        Row(Id="1", Latitude=40.6892, Longitude=-74.0445),
        Row(Id="2", Latitude=37.8199, Longitude=-122.4783),
    ]
    
    # Create DataFrame
    test_df = spark_session.createDataFrame(data, schema=schema)
    
    # Apply Function
    modified_df = add_geohash(test_df)
    
    # Show results for visual confirmation in real-world use
    modified_df.show()
    
    # Collect the results for testing
    results = modified_df.collect()
    
    # Expected geohash for the given latitudes and longitudes
    expected_hashes = ['dr5r', '9q8z']
    
    # Asserting the results
    for row, expected_hash in zip(results, expected_hashes):
        assert row['geohash'] == expected_hash