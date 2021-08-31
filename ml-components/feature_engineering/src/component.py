import kfp.components as comp
def feature_engineering(LIVY_URL,dataset_name,train_data_path: comp.OutputPath("CSV"),test_data_path: comp.OutputPath("CSV")):
    from livy import LivySession
    import pandas as pd
    with LivySession.create(url=LIVY_URL,executor_memory='3g',executor_cores=1,num_executors=2,driver_memory='4g') as session: #spark_conf={'spark.sql.catalogImplementation': 'hive'}) as session:
        # Workaround to change spark config
        session.run("from pyspark.sql.functions import year, month, dayofmonth, dayofweek, hour")
        session.run("from pyspark.conf import SparkConf;from pyspark.sql import SparkSession; spark.sparkContext._conf.getAll(); conf = spark.sparkContext._conf.setAll([('spark.sql.catalogImplementation', 'hive'),('spark.network.timeout','300s')]); spark.sparkContext.stop(); spark = SparkSession.builder.config(conf=conf).getOrCreate(); spark.sparkContext._conf.getAll()")
        # Load Dataset
        session.run("yellow_taxi_clean = spark.sql(\"SELECT * FROM default."+dataset_name+"\")")
        session.run("print(\"Features selected\")")
        session.run("yellow_taxi_selected_features = spark.sql(\"SELECT PULocationID, EXTRACT(year from `tpep_pickup_datetime`) as pickup_year, EXTRACT(month from `tpep_pickup_datetime`) as pickup_month, EXTRACT(day from `tpep_pickup_datetime`) as pickup_day, EXTRACT(hour from `tpep_pickup_datetime`) as pickup_hour, EXTRACT(dayofweek from `tpep_pickup_datetime`) as pickup_weekday  FROM default.yellow_taxi_clean\")")
        session.run("yellow_taxi_grouped = yellow_taxi_selected_features.groupBy(\"PULocationID\",\"pickup_year\",\"pickup_month\",\"pickup_day\",\"pickup_weekday\",\"pickup_hour\").count()")
        session.run("yellow_2018_1 = yellow_taxi_grouped.filter(((yellow_taxi_grouped.pickup_year==2018) & (yellow_taxi_grouped.pickup_month < 5)))")
       # session.run("yellow_2018_2 = yellow_taxi_grouped.filter(((yellow_taxi_grouped.pickup_year==2018) & (yellow_taxi_grouped.pickup_month > 4) & (yellow_taxi_grouped.pickup_month < 9)))")
       # session.run("yellow_2018_3 = yellow_taxi_grouped.filter(((yellow_taxi_grouped.pickup_year==2018) & (yellow_taxi_grouped.pickup_month > 9)))")
       # session.run("yellow_2019_1 = yellow_taxi_grouped.filter(((yellow_taxi_grouped.pickup_year==2019) & (yellow_taxi_grouped.pickup_month < 5)))")
       # session.run("yellow_2019_2 = yellow_taxi_grouped.filter(((yellow_taxi_grouped.pickup_year==2019) & (yellow_taxi_grouped.pickup_month > 4) & (yellow_taxi_grouped.pickup_month < 9)))")
       # session.run("yellow_2019_3 = yellow_taxi_grouped.filter(((yellow_taxi_grouped.pickup_year==2019) & (yellow_taxi_grouped.pickup_month  > 9)))")   
       # session.run("print(\"Features grouped\")") 
        yellow_2018_1 = session.download("yellow_2018_1")  
        session.run("yellow_2018_1.unpersist()")
        print("Data download part 1 done")
       # yellow_2018_2 = session.download("yellow_2018_2") 
       # session.run("yellow_2018_2.unpersist()")
       # print("Data download part 2 done")
       # yellow_2018_3 = session.download("yellow_2018_3")
       # session.run("yellow_2018_3.unpersist()")
       # print("Data download part 3 done")
       # yellow_2019_1 = session.download("yellow_2019_1") 
       # session.run("yellow_2019_1.unpersist()")
       # print("Data download part 4 done")
       # yellow_2019_2 = session.download("yellow_2019_2")  
       # session.run("yellow_2019_2.unpersist()")
       # print("Data download part 5 done")
       # yellow_2019_3 = session.download("yellow_2019_3") 
       # print("Data download part 6 done")
       # taxi_data = pd.concat([yellow_2018_1, yellow_2018_2,yellow_2018_3, yellow_2019_1, yellow_2019_2,yellow_2019_3], ignore_index=True, sort=False)
        taxi_data = yellow_2018_1
        print(taxi_data.head())
        taxi_data = taxi_data.sample(frac=0.1)
        train_size = int(0.7 * len(taxi_data))
        train_set = taxi_data[:train_size]
        test_set = taxi_data[train_size:]
        train_set.to_csv(path_or_buf=train_data_path,index=False)
        test_set.to_csv(path_or_buf=test_data_path,index=False)