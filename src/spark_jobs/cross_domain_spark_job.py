"""lecture 22: PySpark job — 3 წყაროს join, query optimization."""

from pyspark.sql import SparkSession, functions as F
from pyspark.sql.functions import broadcast, lit

def main() -> None:
    spark = (
        SparkSession.builder
        .appName("CrossDomainJoin")
        .master("spark://spark-master:7077")
        .getOrCreate()
    )
    
    spark.sparkContext.setLogLevel("ERROR")
    
    weather_df = spark.read.parquet("/data/format_comparison/weather.parquet")
    currency_df = spark.read.parquet("/data/spark_input/currency_rates.parquet")
    seismic_df = spark.read.parquet("/opt/spark/examples/src/main/resources/users.parquet")
    
    weather_df = weather_df.withColumn("date_key", F.to_date("forecast_time"))
    currency_df = (
        currency_df
        .withColumnRenamed("currency", "currency_code")
        .withColumnRenamed("date", "date_key")
    )
    seismic_df = seismic_df.withColumn("date_key", lit("2023-01-01"))
    
    weather_daily = weather_df.groupBy("date_key").agg(
        F.round(F.avg("temperature_c"), 1).alias("avg_temp")
    )
    usd_daily = (
        currency_df.filter(F.col("currency_code") == "USD")
        .select("date_key", F.col("rate").alias("usd_rate"))
    )
    seismic_daily = seismic_df.groupBy("date_key").agg(
        F.count("*").alias("earthquake_count")
    )
    
    result = (
        weather_daily
        .join(usd_daily, "date_key", "outer")
        .join(seismic_daily, "date_key", "outer")
        .fillna({"earthquake_count": 0})
        .orderBy("date_key")
    )
    
    print("=== Execution Plan (join-ის ოპტიმიზაციამდე) ===")
    result.explain(mode="formatted")
    result.show()
    
    optimized = weather_daily.join(broadcast(usd_daily), "date_key", "left")
    print("=== Execution Plan (broadcast join-ით) ===")
    optimized.explain(mode="formatted")
    
    result.write.mode("overwrite").parquet("/data/cross_domain_daily_summary.parquet")
    spark.stop()

if __name__ == "__main__":
    main()
