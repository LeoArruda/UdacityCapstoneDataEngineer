
CREATE TABLE IF NOT EXISTS staging_immigration (
    "visitor_id" NUMERIC,
    "immigration_id" NUMERIC,
    "year" NUMERIC,
    "month" NUMERIC,
    "city" VARCHAR,
    "country" NUMERIC,
    "port_of_entry" NUMERIC,
    "arrival_date" NUMERIC,
    "address_code" VARCHAR,
    "departure_date" NUMERIC,
    "age" NUMERIC,
    "visa_code" NUMERIC,
    "gender" VARCHAR,
    "airline" VARCHAR,
    "visa_type" VARCHAR);

CREATE TABLE IF NOT EXISTS staging_temperature (
    "date" DATE,
    "average_temperature" NUMERIC,
    "city" VARCHAR,
    "latitude" VARCHAR,
    "longitude" VARCHAR);

CREATE TABLE IF NOT EXISTS staging_airport (
    "airport_code" VARCHAR,
    "name" VARCHAR,
    "continent" VARCHAR,
    "country_code" VARCHAR,
    "region" VARCHAR);

CREATE TABLE IF NOT EXISTS staging_demographics (
    "city" VARCHAR,
    "state" VARCHAR,
    "male_population" NUMERIC,
    "female_population" NUMERIC,
    "total_population" NUMERIC);

CREATE TABLE IF NOT EXISTS fact_city_data (
    "city_id" varchar(32) NOT NULL,
    "city_name" varchar(32) NOT NULL,
    "country" varchar(32) NOT NULL,
    "latitude" varchar(10) NOT NULL,
    "longitude" varchar(10) NOT NULL,
    "average_temperature" numeric NOT NULL,
    "date" date NOT NULL,
    CONSTRAINT "pk_fact_city_data_city_id" PRIMARY KEY (city_id));

CREATE TABLE IF NOT EXISTS dim_airport (
    "airport_id" varchar(50) NOT NULL,
    "airport_code" varchar(50) NOT NULL,
    "name" varchar(500) NOT NULL,
    "continent" varchar(50) NOT NULL,
    "country_code" varchar(32) NOT NULL,
    "state" varchar(32) NOT NULL,
    CONSTRAINT "pk_dim_airport_table_airport_id" PRIMARY KEY (airport_id));

CREATE TABLE IF NOT EXISTS dim_demographic (
    "demographic_id" varchar(100) NOT NULL,
    "city" varchar(50) NOT NULL,
    "state" varchar(50) NOT NULL,
    "male_population" int4 NOT NULL,
    "female_population" int4 NOT NULL,
    "total_population" int4 NOT NULL,
    CONSTRAINT "pk_dim_demographic_demographic_id" PRIMARY KEY (demographic_id));

CREATE TABLE IF NOT EXISTS dim_visitor (
    "visitor_id" varchar(32) NOT NULL,
    "year" int4 NOT NULL,
    "month" int4 NOT NULL,
    "city" varchar(32) NOT NULL,
    "gender" varchar(32) NOT NULL,
    "arrival_date" date NOT NULL,
    "departure_date" date NOT NULL,
    "airline" varchar(32) NOT NULL,
    CONSTRAINT "pk_dim_visitor_visitor_id" PRIMARY KEY (visitor_id));

CREATE TABLE IF NOT EXISTS dim_date (
    "Datekey" INT4 NOT NULL,
    "Year" INT4,
    "Month" INT4,
    "Day" INT4,
    "Date" Date,
    "Quarter_num" INT4,
    "Quarter" VARCHAR(255),
    "Month_name" VARCHAR(255),
    "Week" INT4,
    "Weekday" VARCHAR(255),
    "Weekday_num" INT4,
    CONSTRAINT "pk_dim_date_datekey" PRIMARY KEY ("Datekey")
);
    
