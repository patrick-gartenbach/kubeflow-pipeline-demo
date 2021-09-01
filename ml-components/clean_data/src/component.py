def clean_data(LIVY_URL,dataset_name) -> str:
    from livy import LivySession
    with LivySession.create(url=LIVY_URL,executor_memory='3g',executor_cores=1,num_executors=2) as session: #spark_conf={'spark.sql.catalogImplementation': 'hive'}) as session:
        # Workaround to change spark config
        session.run("from pyspark.sql.functions import year, month, dayofmonth")
        session.run("from pyspark.conf import SparkConf;from pyspark.sql import SparkSession; spark.sparkContext._conf.getAll(); conf = spark.sparkContext._conf.setAll([('spark.sql.catalogImplementation', 'hive'),('spark.driver.memory', '2000M')]); spark.sparkContext.stop(); spark = SparkSession.builder.config(conf=conf).getOrCreate(); spark.sparkContext._conf.getAll()")
        # Load Dataset
        session.run("yellow_taxi = spark.sql(\"SELECT * FROM default.yellow_taxi\")")
        session.run("yellow_taxi_clean = yellow_taxi.filter(((yellow_taxi.passenger_count <= 9) &\
                                       (yellow_taxi.passenger_count > 0) &\
                                       (yellow_taxi.total_amount < 250) &\
                                       (yellow_taxi.trip_distance > 0) &\
                                       (yellow_taxi.trip_distance < 100) &\
                                       (yellow_taxi.VendorID <= 2) &\
                                       (yellow_taxi.VendorID >= 1) &\
                                       (year(\"tpep_pickup_datetime\") <= 2020) &\
                                       (year(\"tpep_pickup_datetime\") >= 2018) &\
                                       (year(\"tpep_dropoff_datetime\") >= 2018) &\
                                       (year(\"tpep_dropoff_datetime\") <= 2020) &\
                                       (yellow_taxi.DOLocationID > 0) &\
                                       (yellow_taxi.DOLocationID <= 265) &\
                                       (yellow_taxi.PULocationID > 0) &\
                                       (yellow_taxi.PULocationID <= 265))).filter(\"VendorID is not NULL\")")
        session.run("print(\"Data cleaned\")")
        session.run("yellow_taxi_clean.write.mode(\"overwrite\").saveAsTable(\"yellow_taxi_clean\")")
        session.run("print(\"Cleaned Data saved\")")
        return "yellow_taxi_clean"