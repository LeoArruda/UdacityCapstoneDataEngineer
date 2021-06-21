class DataValidationQueries:
    """
    DataQualityOperator runs data check SQL queries against the redshift database
    and evaluates the results to confirm that the data did in fact load into the queried table.
    """

    ############
    # Integrity checks to ensure the model is being followed
    ############
    data_in_taxi_rides_unique_integrity ="""
        SELECT count(*) from taxi_rides
        WHERE pickup_datetime = '2020-12-01 00:29:37'
    """
    data_in_precipitation_unique_integrity ="""
        SELECT count(*) from precipitation
        WHERE date = '2015-01-01'
    """

    data_in_taxi_zones_unique_integrity ="""
        SELECT count(*) from taxi_zones
        WHERE locationid = 1
    """

    ############
    # Source/Count checks to ensure completeness
    ############
    data_in_taxi_rides_table_count = """
        SELECT count(*) != 0
        FROM taxi_rides
    """

    data_in_taxi_zones_table_count = """
        SELECT count(*) != 0
        FROM taxi_zones
    """

    data_in_time_table_count = """
        SELECT count(*) != 0
        FROM time
    """

    data_in_precipitation_table_count = """
        SELECT count(*) != 0
        FROM precipitation
    """

    ############
    # Unit Tests to the scripts are doing the right thing
    ############
    unit_test_in_time_table = """
        SELECT COUNT(*) != 0 FROM public.time
        WHERE WEEK=50
    """

    unit_test_in_taxi_rides_and_time_tables = """
        SELECT COUNT(*) != 0 FROM public.taxi_rides as tr
        JOIN time as t
        ON t.trip_timestamp = tr.pickup_datetime
        WHERE t.WEEK=50
    """
