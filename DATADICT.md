# Data dictionary

## About
This file contains an overview of the attributes (columns), types and descriptions for all tables used in the project.

## Tables

### Taxi_zones
| Column | Type | Description |
| --- | --- | --- |
| locationid | VARCHAR | ID of the taxi zones    |
| borough | VARCHAR |  Borough name. I.e. EWR, Queens, Bronx   |
| zone | VARCHAR |  Zone name. I.e. Newark Airport, Astoria Park   |
| service_zone | VARCHAR |  Zone Group name. I.e. Boro Zone, Yellow Zone   |

---

### Precipitation
| Column | Type | Description |
| --- | --- | --- |
| station | VARCHAR | Weather station code ID |
| name | VARCHAR | Station Name. I.e. NY CITY CENTRAL PARK, NY US |
| date | DATE | Date of the record |
| awnd | DECIMAL | Average wind speedc|
| prcp | DECIMAL | Precipitation |
| snow | DECIMAL | Snowfall |
| snwd | DECIMAL | Snow depth |
| tavg | DECIMAL | Average Temperature |
| tmax | DECIMAL | Maximum temperature |
| tmin | DECIMAL | Minimum temperature |
| datekey | INT | Date key for Time dimension |

---

### Stage_green
| Column | Type | Description |
| --- | --- | --- |
| VendorID | VARCHAR | Vendor ID | 
| lpep_pickup_datetime | VARCHAR | Pickup date time | 
| lpep_dropoff_datetime | VARCHAR | Dropoff date time | 
| store_and_fwd_flag | CHAR | Store and forward flag | 
| RatecodeID | VARCHAR | Rate Code ID | 
| PULocationID | VARCHAR | Pickup Location ID | 
| DOLocationID | VARCHAR | Dropoff Location ID | 
| passenger_count | INT | Number of passengers present | 
| trip_distance | DECIMAL | Distance of the trip | 
| fare_amount | DECIMAL | Fare amount  | 
| extra | DECIMAL | Extra amount | 
| mta_tax | DECIMAL | Tax amount | 
| tip_amount | DECIMAL | Trip amount | 
| tolls_amount | DECIMAL | Tolls amount | 
| ehail_fee | DECIMAL | Ehail fee | 
| improvement_surcharge | DECIMAL | Improvement surcharge amount | 
| total_amount | DECIMAL | Total amount | 
| payment_type | VARCHAR | Payment Type | 
| trip_type| VARCHAR | Trip type | 
| congestion_surcharge|  DECIMAL | Congestion surcharge amount | 

---

### Stage_yellow
| Column | Type | Description |
| --- | --- | --- |
| VendorID | VARCHAR | Vendor ID | 
| tpep_pickup_datetime | VARCHAR | Pickup date time | 
| tpep_dropoff_datetime | VARCHAR | Dropoff date time | 
| passenger_count | INT | Number of passengers present | 
| trip_distance | DECIMAL | Distance of the trip | 
| RatecodeID | VARCHAR | Rate Code ID | 
| store_and_fwd_flag | CHAR | Store and forward flag | 
| PULocationID | VARCHAR | Pickup Location ID | 
| DOLocationID | VARCHAR | Dropoff Location ID | 
| payment_type | VARCHAR | Payment Type | 
| fare_amount | DECIMAL | Fare amount | 
| extra | DECIMAL | Extra amount | 
| mta_tax | DECIMAL | Tax amount | 
| tip_amount | DECIMAL | Trip amount | 
| tolls_amount | DECIMAL | Tolls amount | 
| improvement_surcharge | DECIMAL | Improvement surcharge amount | 
| total_amount | DECIMAL | Total amount | 
| congestion_surcharge | DECIMAL | Congestion surcharge amount | 

---

### Stage_fhv
| Column | Type | Description |
| --- | --- | --- |
| dispatching_base_num | VARCHAR | Dispatching Base Number | 
| pickup_datetime | VARCHAR | Pickup date time | 
| dropoff_datetime | VARCHAR | Dropoff date time | 
| puLocationID | VARCHAR | Pickup Location ID | 
| doLocationID | VARCHAR | Dropoff Location ID | 
| SR_Flag | VARCHAR | SR Flag |  

---

### Stage_fhvhv
| Column | Type | Description |
| --- | --- | --- |
| hvfhs_license_num | VARCHAR | High Volume For-Hire Services Vehicle ID Number | 
| dispatching_base_num | VARCHAR | Dispatching Base Number | 
| pickup_datetime | VARCHAR | Pickup date time | 
| dropoff_datetime | VARCHAR | Dropoff date time | 
| puLocationID | VARCHAR | Pickup Location ID | 
| doLocationID | VARCHAR | Dropoff Location ID | 
| SR_Flag | VARCHAR | SR Flag | 

---

### Time
| Column | Type | Description |
| --- | --- | --- |
| trip_timestamp | timestamp |  [not null] Trip Timestamp | 
| hour | INT | # of the Hour | 
| day | INT | # of the Day | 
| week | INT | # of the Week | 
| month | INT | # of the Month | 
| year | INT | # of the Year | 
| weekday | INT | # of the Weekday (Sunday=1, Monday=2,...) | 
| datekey | INT | Key ID for the Time Dimension (YYYYMMDD) | 

---

### Taxi_rides
| Column | Type | Description |
| --- | --- | --- |
| VendorID | VARCHAR | Vendor ID | 
| pickup_datetime | VARCHAR | Pickup date time | 
| dropoff_datetime | VARCHAR | Dropoff date time | 
| store_and_fwd_flag | CHAR | Store and forward flag | 
| RatecodeID | VARCHAR | Rate Code ID | 
| PULocationID | VARCHAR | Pickup Location ID | 
| DOLocationID | VARCHAR | Dropoff Location ID | 
| passenger_count | INT | Passenger count | 
| trip_distance | DECIMAL | Trip Distance | 
| fare_amount | DECIMAL | Fare Amount | 
| extra | DECIMAL | Extra Amount | 
| mta_tax | DECIMAL | Tax MTA Amount | 
| tip_amount | DECIMAL | Tip Amount | 
| tolls_amount | DECIMAL | Tolls Amount | 
| improvement_surcharge | DECIMAL | Improvement Surcharge Amount | 
| total_amount | DECIMAL | Total Amount | 
| payment_type | VARCHAR | Payment Type | 
| congestion_surcharge | DECIMAL | Congestion Surcharge | 
| datekey | INT | Key ID for the Time Dimension (YYYYMMDD) | 

---