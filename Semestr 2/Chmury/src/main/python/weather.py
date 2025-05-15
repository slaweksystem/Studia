from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import avg, first, round

def load_weather_data(spark: SparkSession, path: str) -> DataFrame:
    """
    Reads weather data from Parquet files.
    
    Parameters:
    - spark (SparkSession): The Spark session object.
    - path: File path pattern for loading data.
    
    Returns:
    - DataFrame: Spark DataFrame containing the weather data.
    """
    return spark.read.parquet(path)

def aggregate_weather_data_by_geohash(df: DataFrame) -> DataFrame:
    """
    Aggregates weather data by geohash and date on temperature data.
    
    Parameters:
    - df (DataFrame): DataFrame containing the weather data with 'geohash' columns.
    
    Returns:
    - DataFrame: Aggregated DataFrame by geohash.
    """
    return df.groupBy("geohash", "wthr_date").agg(
        round(avg("avg_tmpr_f"), 1).alias("avg_tmpr_f"), 
        round(avg("avg_tmpr_c"), 1).alias("avg_tmpr_c")
    )

def join_hotel_and_weather_data(df_hotels: DataFrame, df_weather: DataFrame) -> DataFrame:
    """
    Joins hotel data with weather data on geohash.
    
    Parameters:
    - df_hotels (DataFrame): DataFrame containing hotel data.
    - df_weather (DataFrame): DataFrame containing weather data aggregated by geohash.
    
    Returns:
    - DataFrame: Resultant DataFrame after left joining on 'geohash'.
    """
    return df_hotels.join(df_weather, "geohash", "left")

def write_data_to_parquet(df: DataFrame, output_path: str) -> None:
    """
    Writes DataFrame to a specified parquet output directory.
    
    Parameters:
    - df (DataFrame): DataFrame to write.
    - output_path (str): Path to write the DataFrame.
    """
    df.write.parquet(output_path)
