import os

from utils import create_spark_session
from geocoding import add_geohash
from hotels import load_hotel_data, fill_missing_hotel_coords
from weather import load_weather_data
from weather import aggregate_weather_data_by_geohash
from weather import join_hotel_and_weather_data
from weather import write_data_to_parquet

def main():
    # Load env variabiels
    opencage_api_key = os.getenv('OPENCAGE_API_KEY')
    storage_account_name = os.getenv('STORAGE_ACCOUNT_NAME')
    storage_account_key = os.getenv('STORAGE_ACCOUNT_KEY')
    hotels_container = os.getenv('HOTELS_CONTAINER_URL')
    weather_container = os.getenv('WEATHER_CONTAINER_URL')
    output_container_url = os.getenv('OUTPUT_CONTAINER_URL')

    # Create Spark Session
    spark = create_spark_session('Hotel Weather Data',
                                 storage_account_name,
                                 storage_account_key)

    # Load Hotels Data
    input_csv_path = f"abfss://{hotels_container}@{storage_account_name}.dfs.core.windows.net/hotels/"
    df_hotels = load_hotel_data(spark, input_csv_path)

    # Fill missing Latitude & Longitude
    df_hotels = fill_missing_hotel_coords(df_hotels, opencage_api_key)

    # Add Geohash
    df_hotels = add_geohash(df_hotels)

    # Load Weather Data
    weather_data = f"abfss://{weather_container}@{storage_account_name}.dfs.core.windows.net/weather/"
    df_weather = load_weather_data(spark, weather_data)

    # Add Geohash
    df_weather = add_geohash(df_weather, latitude_col = 'lat', longitude_col = 'lng')

    # Group columns with the same geohash
    df_weather = aggregate_weather_data_by_geohash(df_weather)

    # Perform left join
    df_enriched_dat = join_hotel_and_weather_data(df_hotels, df_weather)
        
    # Save data
    output_path = f"abfss://{output_container_url}@{storage_account_name}.dfs.core.windows.net/output/"
    write_data_to_parquet(df_enriched_dat, output_path = output_path)

    spark.stop()

if __name__ == '__main__':
    main()