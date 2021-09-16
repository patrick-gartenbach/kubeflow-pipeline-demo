#!/usr/bin/env bash
mysql --user="root" --password="Hpecp123!"  --database="taxi" --execute="DROP TABLE IF EXISTS yellow_trips"
mysql --user="root" --password="Hpecp123!"  --database="taxi" --execute="CREATE TABLE IF NOT EXISTS yellow_trips (
  		vendor_id varchar(3) NOT NULL DEFAULT '0',
 		pickup_datetime datetime NOT NULL,
 		dropoff_datetime datetime NOT NULL,
 		passenger_count tinyint(2) NOT NULL DEFAULT 0,
 		trip_distance decimal(6,2) NOT NULL DEFAULT 0,
 		rate_code tinyint NOT NULL DEFAULT 0,
  		store_and_fwd_flag varchar(1) NOT NULL DEFAULT 'N',
 		PULocationID smallint(3) NOT NULL DEFAULT 0,
  		DOLocationID smallint(3) NOT NULL DEFAULT 0,
 		payment_type tinyint NOT NULL DEFAULT 0,
 		fare_amount decimal(6,2) NOT NULL DEFAULT 0,
 		extra decimal(6,2) NOT NULL DEFAULT 0, 
  		mta_tax decimal(6,2) NOT NULL DEFAULT 0,
  		tip_amount decimal(6,2) NOT NULL DEFAULT 0,
  		tolls_amount decimal(6,2) NOT NULL DEFAULT 0,
  		improvement_surcharge decimal(6,2) NOT NULL DEFAULT 0, 
  		total_amount decimal(7,2) NOT NULL DEFAULT 0
		);"
for f in *.csv
do
       mysql --local-infile --user="root" --password="Hpecp123!"  --database="taxi" --execute="LOAD DATA LOCAL INFILE '$f' INTO TABLE yellow_trips FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 2 ROWS;"
done