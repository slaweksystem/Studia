import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType
from pyspark.sql.functions import col
from pyspark.sql import DataFrame

from ..main.python.weather import aggregate_weather_data_by_geohash

def create_hotels_df(spark: SparkSession) -> DataFrame:
    schema = StructType([
        StructField("Id", LongType(), True),
        StructField("Name", StringType(), True),
        StructField("Country", StringType(), True),
        StructField("City", StringType(), True),
        StructField("Address", StringType(), True),
        StructField("Latitude", DoubleType(), True),
        StructField("Longitude", DoubleType(), True),
        StructField("geohash", StringType(), True)
    ])
    data = [
        (1, "Hotel Paris", "France", "Paris", "1 Rue de Paris", 48.8584, 2.2945, "u09t"),
        (2, "Hotel SF", "USA", "San Francisco", "1 SF St", 37.7749, -122.4194, "9q8y")
    ]
    return spark.createDataFrame(data, schema)

def create_weather_df(spark: SparkSession) -> DataFrame:
    schema = StructType([
        StructField("lng", DoubleType(), True),
        StructField("lat", DoubleType(), True),
        StructField("avg_tmpr_f", DoubleType(), True),
        StructField("avg_tmpr_c", DoubleType(), True),
        StructField("wthr_date", StringType(), True),
        StructField("wthr_year", StringType(), True),
        StructField("wthr_month", StringType(), True),
        StructField("wthr_day", StringType(), True),
        StructField("geohash", StringType(), True)
    ])
    data = [
        (-122.4194, 37.7749, 58.0, 14.4, "2020-01-01", "2020", "01", "01", "9q8y")
    ]
    return spark.createDataFrame(data, schema)

def join_hotel_and_weather_data(df_hotels: DataFrame, df_weather: DataFrame) -> DataFrame:
    return df_hotels.join(df_weather, "geohash", "left")

@pytest.fixture(scope="module")
def spark_session():
    return SparkSession.builder \
        .master("local[1]") \
        .appName("JoinTesting") \
        .getOrCreate()

def test_join_hotel_and_weather_data(spark_session):
    df_hotels = create_hotels_df(spark_session)
    df_weather = create_weather_df(spark_session)

    result_df = join_hotel_and_weather_data(df_hotels, df_weather)

    expected_data = [
        ("u09t", 1, "Hotel Paris", "France", "Paris", "1 Rue de Paris", 48.8584, 2.2945, None, None, None, None, None, None, None, None),
        ("9q8y", 2, "Hotel SF", "USA", "San Francisco", "1 SF St", 37.7749, -122.4194, -122.4194, 37.7749, 58.0, 14.4, "2020-01-01", "2020", "01", "01")
    ]
    expected_schema =  StructType([
        StructField("geohash", StringType(), True),
        StructField("Id", LongType(), True),
        StructField("Name", StringType(), True),
        StructField("Country", StringType(), True),
        StructField("City", StringType(), True),
        StructField("Address", StringType(), True),
        StructField("Latitude", DoubleType(), True),
        StructField("Longitude", DoubleType(), True),
        StructField("lng", DoubleType(), True),
        StructField("lat", DoubleType(), True),
        StructField("avg_tmpr_f", DoubleType(), True),
        StructField("avg_tmpr_c", DoubleType(), True),
        StructField("wthr_date", StringType(), True),
        StructField("wthr_year", StringType(), True),
        StructField("wthr_month", StringType(), True),
        StructField("wthr_day", StringType(), True),
    ])
    expected_df = spark_session.createDataFrame(expected_data, expected_schema)
    
    assert result_df.collect() == expected_df.collect(), "The resulting DataFrame does not match the expected DataFrame"

def create_weather_df_2(spark: SparkSession) -> DataFrame:
    schema = StructType([
        StructField("geohash", StringType(), True),
        StructField("wthr_date", StringType(), True),
        StructField("avg_tmpr_f", DoubleType(), True),
        StructField("avg_tmpr_c", DoubleType(), True)
    ])
    data = [
        ("u09t", "2020-01-01", 50.0, 10.0),
        ("u09t", "2020-01-01", 55.0, 13.0),
        ("9q8y", "2020-01-02", 60.0, 15.5),
        ("9q8y", "2020-01-02", 65.0, 18.5),
        ("9q8y", "2020-01-03", 70.0, 13.0)
    ]
    return spark.createDataFrame(data, schema)



def test_aggregate_weather_data_by_geohash(spark_session):
    df_weather = create_weather_df_2(spark_session)

    result_df = aggregate_weather_data_by_geohash(df_weather)

    expected_data = [
        ("u09t", "2020-01-01", 52.5, 11.5),
        ("9q8y", "2020-01-02", 62.5, 17.0),
        ("9q8y", "2020-01-03", 70.0, 13.0)
    ]
    expected_schema = StructType([
        StructField("geohash", StringType(), True),
        StructField("wthr_date", StringType(), True),
        StructField("avg_tmpr_f", DoubleType(), True),
        StructField("avg_tmpr_c", DoubleType(), True)
    ])
    expected_df = spark_session.createDataFrame(expected_data, expected_schema)
    
    # Note: DataFrame comparisons in tests can be tricky due to potential differences in row order
    assert result_df.sort("geohash", "wthr_date").collect() == expected_df.sort("geohash", "wthr_date").collect(), "The resulting aggregated DataFrame does not match the expected DataFrame"