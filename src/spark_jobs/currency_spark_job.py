from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder \
        .appName("Lab21-Currency-Transform-SQL") \
        .master("local[*]") \
        .getOrCreate()

    input_path = "data/spark_input/currency_rates.parquet"
    print(f"Reading Parquet data from {input_path}...")
    df = spark.read.parquet(input_path)

    # 1. პარკეტის temp view-დ დარეგისტრირება SQL-ით query-ისთვის
    # (შევამოწმოთ სვეტების სახელები: ჩვენს parquet-ში არის date, currency, rate)
    df.createOrReplaceTempView("currency_rates")

    print("\n=== Step 5.1: Spark SQL Daily Stats ===")
    daily_stats_sql = spark.sql("""
        SELECT
            currency AS currency_code,
            ROUND(AVG(rate), 4) AS avg_rate,
            MIN(rate) AS min_rate,
            MAX(rate) AS max_rate,
            COUNT(*) AS days_count
        FROM currency_rates
        GROUP BY currency
        ORDER BY currency;
    """)
    daily_stats_sql.show()

    print("\n=== Step 5.2: Spark SQL Window Function (Daily Changes) ===")
    daily_changes_sql = spark.sql("""
        SELECT
            currency AS currency_code,
            date AS rate_date,
            rate,
            LAG(rate, 1) OVER (
                PARTITION BY currency 
                ORDER BY date
            ) AS prev_rate,
            ROUND(rate - LAG(rate, 1) OVER (
                PARTITION BY currency 
                ORDER BY date
            ), 4) AS daily_change
        FROM currency_rates
        ORDER BY currency, date;
    """)
    daily_changes_sql.show(10)

    # შედეგების შენახვა პარკეტ ფორმატში როგორც ლექციაშია მოთხოვნილი
    output_path = "data/spark_output/currency_transformed_sql"
    daily_changes_sql.write.mode("overwrite").parquet(output_path)
    print(f"SQL-transformed data successfully written to {output_path}")

    spark.stop()

if __name__ == "__main__":
    main()
