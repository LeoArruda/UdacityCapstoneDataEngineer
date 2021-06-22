class SqlQueries:
    """
    This function hosts the various SQL queries used to perform tasks in Amazon Redshift.
    These queries create tables, copy data from S3 to Redshift, modify the data model and run data analysis tasks.
    """
    drop_cab_types ='''DROP TABLE IF EXISTS cab_types'''
    drop_fhv_bases ='''DROP TABLE IF EXISTS fhv_bases'''
    drop_fhv_trips ='''DROP TABLE IF EXISTS fhv_trips'''
    drop_fhv_trips_staging ='''DROP TABLE IF EXISTS fhv_trips_staging'''
    drop_green_tripdata_staging ='''DROP TABLE IF EXISTS green_tripdata_staging'''
    drop_hvfhs_license ='''DROP TABLE IF EXISTS hvfhs_licenses'''
    drop_precipitation ='''DROP TABLE IF EXISTS precipitation'''
    drop_stage_fhv ='''DROP TABLE IF EXISTS stage_fhv'''
    drop_stage_fhvhv ='''DROP TABLE IF EXISTS stage_fhvhv'''
    drop_stage_green ='''DROP TABLE IF EXISTS stage_green'''
    drop_stage_yellow ='''DROP TABLE IF EXISTS stage_yellow'''
    drop_taxi_rides ='''DROP TABLE IF EXISTS taxi_rides'''
    drop_taxi_zones ='''DROP TABLE IF EXISTS taxi_zones'''
    drop_time ='''DROP TABLE IF EXISTS time'''
    drop_trips ='''DROP TABLE IF EXISTS trips'''
    drop_uber_trips_2014 ='''DROP TABLE IF EXISTS uber_trips_2014'''
    drop_yellow_tripdata_staging ='''DROP TABLE IF EXISTS yellow_tripdata_staging'''

    drop_all_tables = [
        drop_cab_types,
        drop_fhv_bases,
        drop_fhv_trips,
        drop_fhv_trips_staging,
        drop_green_tripdata_staging,
        drop_hvfhs_license,
        drop_precipitation,
        drop_stage_fhv,
        drop_stage_fhvhv,
        drop_stage_green,
        drop_stage_yellow,
        drop_taxi_rides,
        drop_taxi_zones,
        drop_time,
        drop_trips,
        drop_uber_trips_2014,
        drop_yellow_tripdata_staging
    ]

    create_taxi_zones='''
        CREATE TABLE IF NOT EXISTS public.taxi_zones (
            locationid VARCHAR(255),
            borough VARCHAR(255),
            zone VARCHAR(255),
            service_zone VARCHAR(255)
        )
    '''

    create_precipitation='''
        CREATE TABLE IF NOT EXISTS public.precipitation (
            station VARCHAR(255),
            name VARCHAR(255),
            date DATE,
            awnd DECIMAL,
            prcp DECIMAL,
            snow DECIMAL,
            snwd DECIMAL,
            tavg DECIMAL,
            tmax DECIMAL,
            tmin DECIMAL
        )
    '''

    create_stage_green = '''
        CREATE TABLE IF NOT EXISTS public.stage_green (
            VendorID                VARCHAR,
            lpep_pickup_datetime    VARCHAR,
            lpep_dropoff_datetime   VARCHAR,
            store_and_fwd_flag      CHAR,
            RatecodeID              VARCHAR,
            PULocationID            VARCHAR,
            DOLocationID            VARCHAR,
            passenger_count         INT,
            trip_distance           DECIMAL,
            fare_amount             DECIMAL,
            extra                   DECIMAL,
            mta_tax                 DECIMAL,
            tip_amount              DECIMAL,    
            tolls_amount            DECIMAL,
            ehail_fee               DECIMAL,
            improvement_surcharge   DECIMAL,
            total_amount            DECIMAL,
            payment_type            VARCHAR,
            trip_type               VARCHAR,
            congestion_surcharge    DECIMAL
        )
    '''

    create_stage_yellow = '''
        CREATE TABLE IF NOT EXISTS public.stage_yellow (
            VendorID                VARCHAR,
            tpep_pickup_datetime    VARCHAR,
            tpep_dropoff_datetime   VARCHAR,
            passenger_count         INT,
            trip_distance           DECIMAL,
            RatecodeID              VARCHAR,
            store_and_fwd_flag      CHAR,
            PULocationID            VARCHAR,
            DOLocationID            VARCHAR,
            payment_type            VARCHAR,
            fare_amount             DECIMAL,
            extra                   DECIMAL,
            mta_tax                 DECIMAL,
            tip_amount              DECIMAL,
            tolls_amount            DECIMAL,
            improvement_surcharge   DECIMAL,
            total_amount            DECIMAL,
            congestion_surcharge    DECIMAL
        )
    '''

    create_stage_fhv = '''
        CREATE TABLE IF NOT EXISTS public.stage_fhv (
            dispatching_base_num    VARCHAR,
            pickup_datetime         VARCHAR,
            dropoff_datetime        VARCHAR,
            puLocationID            VARCHAR,
            doLocationID            VARCHAR,
            SR_Flag                 VARCHAR
        )
    '''

    create_stage_fhvhv = '''
            CREATE TABLE IF NOT EXISTS public.stage_fhvhv (
                hvfhs_license_num       VARCHAR,
                dispatching_base_num    VARCHAR,
                pickup_datetime         VARCHAR,
                dropoff_datetime        VARCHAR,
                puLocationID            VARCHAR,
                doLocationID            VARCHAR,
                SR_Flag                 VARCHAR
            )
        '''

    create_stage_tables = [
        create_precipitation,
        create_taxi_zones,
        create_stage_green,
        create_stage_yellow,
        create_stage_fhv,
        create_stage_fhvhv
    ]

    edit_staging = """
        ALTER TABLE {table} rename column {columnA} to {columnB};
    """

    edit_stage_tables = [
        edit_staging.format(table='stage_green', columnA='lpep_pickup_datetime', columnB='pickup_datetime'),
        edit_staging.format(table='stage_green', columnA='lpep_dropoff_datetime', columnB='dropoff_datetime'),
        edit_staging.format(table='stage_yellow', columnA='tpep_pickup_datetime', columnB='pickup_datetime'),
        edit_staging.format(table='stage_yellow', columnA='tpep_dropoff_datetime', columnB='dropoff_datetime')
    ]

    create_time_table = """
        CREATE TABLE IF NOT EXISTS time(
            trip_timestamp  TIMESTAMP NOT NULL sortkey,
            hour            INT, 
            day             INT, 
            week            INT, 
            month           INT, 
            year            INT, 
            weekday         INT,
            datekey         INT
        );
    """

    create_taxi_table = """
        CREATE TABLE IF NOT EXISTS taxi_rides(
            VendorID                VARCHAR,
            pickup_datetime         VARCHAR,
            dropoff_datetime        VARCHAR,
            store_and_fwd_flag      CHAR,
            RatecodeID              VARCHAR,
            PULocationID            VARCHAR,
            DOLocationID            VARCHAR,
            passenger_count         INT,
            trip_distance           DECIMAL,
            fare_amount             DECIMAL,
            extra                   DECIMAL,
            mta_tax                 DECIMAL,
            tip_amount              DECIMAL,    
            tolls_amount            DECIMAL,
            improvement_surcharge   DECIMAL,
            total_amount            DECIMAL,
            payment_type            VARCHAR,
            congestion_surcharge    DECIMAL,
            pickup_datekey          INT,
            dropoff_datekey         INT
        );
    """

    create_data_tables = [create_time_table, create_taxi_table]

    alter_stage_add_pickup_datekey = ''' 
        ALTER TABLE public.{table}
        ADD COLUMN pickup_datekey INT DEFAULT NULL
    '''

    alter_stage_add_dropoff_datekey = ''' 
        ALTER TABLE public.{table}
        ADD COLUMN dropoff_datekey INT DEFAULT NULL
    '''

    alter_tables_datekey = [
        alter_stage_add_pickup_datekey.format(table='stage_green'),
        alter_stage_add_dropoff_datekey.format(table='stage_green'),
        alter_stage_add_pickup_datekey.format(table='stage_yellow'),
        alter_stage_add_dropoff_datekey.format(table='stage_yellow')
    ]

    alter_stage_insert_pickup_datekey = ''' 
        UPDATE public.{table}
        SET pickup_datekey = CAST(to_char(to_date(pickup_datetime, 'YYYY-MM-DD'), 'YYYYMMDD') as int);
    '''

    alter_stage_insert_dropoff_datekey = ''' 
        UPDATE public.{table}
        SET dropoff_datekey = CAST(to_char(to_date(dropoff_datetime, 'YYYY-MM-DD'), 'YYYYMMDD') as int);
    '''

    insert_into_tables_datekey = [
        alter_stage_insert_pickup_datekey.format(table='stage_green'),
        alter_stage_insert_dropoff_datekey.format(table='stage_green'),
        alter_stage_insert_pickup_datekey.format(table='stage_yellow'),
        alter_stage_insert_dropoff_datekey.format(table='stage_yellow')
    ]
    
    move_staging_time = '''
        INSERT INTO public.time (trip_timestamp, hour, day, week, month, year, weekday, datekey)
        SELECT  DISTINCT to_timestamp ({column}, 'YYYY-MM-DD HH24:MI:SS') as DT, 
                extract(hour from DT), 
                extract(day from DT), 
                extract(week from DT), 
                extract(month from DT), 
                extract(year from DT), 
                extract(dayofweek from DT),
                cast(to_char(DT, 'YYYYMMDD') as int)
        FROM public.{table}
    '''

    move_time_data = [
        move_staging_time.format(table='taxi_rides', column='pickup_datetime')
    ]

    alter_precipitation_add_datekey = ''' 
        ALTER TABLE public.{table}
        ADD COLUMN datekey INT DEFAULT NULL
    '''

    alter_precipitation_insert_datekey = '''
        UPDATE public.{table}
        SET datekey = CAST(to_char(date, 'YYYYMMDD') as int);
    '''

    alter_precipitation_table_datekey = [
        alter_precipitation_add_datekey.format(table='precipitation'),
        alter_precipitation_insert_datekey.format(table='precipitation'),
    ]

    move_staging__taxi = '''
        ALTER TABLE taxi_rides APPEND FROM {table} 
        IGNOREEXTRA
    '''

    move_ride_data = [
        move_staging__taxi.format(table='stage_green'),
        move_staging__taxi.format(table='stage_yellow')
    ]


    analyse_location = '''
        SELECT 
            zones.borough,
            sum(rides.total_amount) as total
        FROM 
            public.taxi_rides as rides
        JOIN
            public.taxi_zones as zones
            ON
                rides.{locationColumn} = zones.locationid
        GROUP BY
            zones.borough
        ORDER BY
            total DESC
        LIMIT 
            10
        ;
    '''

    analysisQueries = [
        analyse_location.format(locationColumn='PULocationID'),
        analyse_location.format(locationColumn='DOLocationID')
    ]