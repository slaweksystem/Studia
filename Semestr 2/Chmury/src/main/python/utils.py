from pyspark.sql import SparkSession

def create_spark_session(app_name: str,
                         storage_account_name: str,
                         storage_account_key: str
                         ) -> SparkSession:
    # Create Spark session
    spark: SparkSession = SparkSession.builder \
        .appName(app_name) \
        .config('spark.jars.packages', 'org.apache.hadoop:hadoop-azure:3.3.4') \
        .config('fs.azure', 'org.apache.hadoop.fs.azure.NativeAzureFileSystem') \
        .getOrCreate()
    
    spark.conf.set(
            f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net",
            storage_account_key
    )
    
    return spark