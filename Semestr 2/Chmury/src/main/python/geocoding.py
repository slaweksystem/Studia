import requests
import pygeohash as pgh

from pyspark.sql import DataFrame
from pyspark.sql.functions import udf, lit
from pyspark.sql.types import StringType

def get_lat_long(country: str, city: str, address: str, api_key: str):
    """
    Retrieves latitude and longitude coordinates for a given address using the OpenCage Geocoding API.

    Parameters:
    - country (str): The country where the address is located.
    - city (str): The city where the address is located.
    - address (str): The specific address to search for within the specified city and country.
    - api_key (str): The API key required to authenticate and access the OpenCage Geocoding API.

    Returns:
    - tuple: A tuple containing the latitude and longitude (lat, long) of the given address.
             Returns (None, None) if the API call fails or if the address is not found.
    """
     
    base_url = 'https://api.opencagedata.com/geocode/v1/json'
    
    query = f"{address}, {city}, {country}"
    
    params = {
        'key': api_key,
        'q': query,
        'pretty': 1
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        if data['total_results'] > 0:
            lat = data['results'][0]['geometry']['lat']
            long = data['results'][0]['geometry']['lng']
            return lat, long

    # Return None, if not found or fails
    return None, None

def add_geohash(df: DataFrame, 
                latitude_col: str = 'Latitude', 
                longitude_col: str = 'Longitude'
                ) -> DataFrame:
    """
    Adds a geohash column to a DataFrame based on latitude and longitude columns.

    Parameters:
    - df (DataFrame): The input DataFrame containing the geographical coordinates.
    - latitude_col (str, optional): The name of the column in `df` that contains latitude values. Defaults to 'Latitude'.
    - longitude_col (str, optional): The name of the column in `df` that contains longitude values. Defaults to 'Longitude'.

    Returns:
    - DataFrame: A new DataFrame with an added 'geohash' column representing the geohash code for each location.

    Example Usage:
    ```
    # Assuming `df` is a Spark DataFrame having columns 'Latitude' and 'Longitude'.
    modified_df = add_geohash(df)
    # Now `modified_df` includes a 'geohash' column.
    ```
    """
    udf_get_geohash = udf(pgh.encode, StringType())
    return df.withColumn("geohash", udf_get_geohash(df[latitude_col], df[longitude_col], lit(4)))