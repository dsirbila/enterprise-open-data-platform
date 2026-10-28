from pyspark.sql.window import Window
from pyspark.sql import functions as F

def transform_currency_data(df):
    window_spec = Window.partitionBy("currency").orderBy("date")
    
    transformed_df = df.withColumn(
        "prev_rate", F.lag("rate", 1).over(window_spec)
    ).withColumn(
        "daily_change", F.col("rate") - F.col("prev_rate")
    )
    
    return transformed_df
