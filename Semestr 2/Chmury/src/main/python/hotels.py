from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StringType, StructField, StructType, DoubleType, LongType
from pyspark.sql.functions import udf, lit, col

from .geocoding import get_lat_long

def load_hotel_data(spark: SparkSession, file_path: str) -> DataFrame:
    """
    Loads hotel data from a gzipped CSV file into a Spark DataFrame with a predefined schema.

    Parameters:
    - spark (SparkSession): The Spark session object used to manage interactions with the Spark engine.
    - file_path (str): The file path to the gzipped CSV file containing hotel data.
    
    Returns:
    - DataFrame: A Spark DataFrame containing the hotel data structured according to the predefined schema.
    """
    # Define Schema
    schema = StructType([
        StructField("Id", LongType(), True),
        StructField("Name", StringType(), True),
        StructField("Country", StringType(), True),
        StructField("City", StringType(), True),
        StructField("Address", StringType(), True),
        StructField("Latitude", DoubleType(), True),
        StructField("Longitude", DoubleType(), True)
    ])

    # Read the partitioned and gzipped CSV files into a DataFrame
    return spark.read.option("header", "true") \
        .option("inferSchema", "true") \
        .option("compression", "gzip") \
        .csv(file_path, schema = schema)

def fill_missing_hotel_coords(df: DataFrame, geo_api_key: str) -> DataFrame:
    """
    Fills missing latitude and longitude values in a DataFrame using an external geocoding API.
    
    This function identifies rows in the DataFrame where latitude or longitude are missing. It uses a geocoding
    service, accessed via a user-provided API key, to retrieve the missing coordinates based on the hotel's
    address, city, and country. The new coordinates are then merged into the original DataFrame.

    Parameters:
    - df (DataFrame): The DataFrame containing hotel data with potential missing coordinates.
    - geo_api_key (str): The API key for accessing the geocoding service.

    Returns:
    - DataFrame: The input DataFrame with missing latitude and longitude values filled in.

    Example Usage:
    ```
    # Assuming `df` is a Spark DataFrame containing hotel data with some missing 'Latitude' or 'Longitude' values.
    geo_api_key = "your_geographic_api_key_here"
    filled_df = fill_missing_hotel_coords(df, geo_api_key)
    # `filled_df` will have no missing values in the 'Latitude' and 'Longitude' columns.
    ```
    """
    df_missing_lat_long = df.filter(df['Latitude'].isNull() | df['Longitude'].isNull())
    udf_get_lat_long = udf(get_lat_long,
                           StructType([StructField("lat", DoubleType(), True),
                                       StructField("long", DoubleType(), True)]))
    df_missing_lat_long = df_missing_lat_long.withColumn("latlong_temp", udf_get_lat_long(df.Country, df.City, df.Address, lit(geo_api_key)))\
                   .withColumn("Latitude", col("latlong_temp.lat")) \
                   .withColumn("Longitude", col("latlong_temp.long")) \
                   .drop("latlong_temp")

    df = df.filter(df['Latitude'].isNotNull() & df['Longitude'].isNotNull()).union(df_missing_lat_long)
    return df
