"""
DAG #3: This DAG is a compilation and arrangement of tasks to insert data from staging table into 
the Redshift fact and dimension tables.
"""
from datetime import datetime, timedelta
import logging
import os
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.amazon.aws.operators.s3_copy_object import S3CopyObjectOperator
from helpers import SqlQueries, DataValidationQueries
from operators import DataQualityOperator, DataAnalysisOperator

LOCAL_DIR='/Users/leandroarruda/Codes/UdacityCapstoneDEng/data/'

default_args = {
    'owner': 'Leo Arruda',
    'start_date': datetime(2021, 1, 1),
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('NYC_TLC_RUN_MODELING_DAG',
          default_args=default_args,
          description='Load monthly data from Redshift staging to analytical model table',
          schedule_interval='@monthly',
          catchup=False,
          tags=['Load', 'Dataset', 'Redshift', 'Model'],
          )

start_modeling = DummyOperator(task_id='Start_modeling_Redshift',  dag=dag)


prepare_stage_tables = PostgresOperator(
    dag=dag,
    task_id='prepare_stage_tables',
    postgres_conn_id='redshift',
    sql=SqlQueries.edit_stage_tables,
    autocommit=True
)

setup_and_create_data_tables = PostgresOperator(
    dag=dag,
    task_id='setup_and_create_data_tables',
    postgres_conn_id='redshift',
    sql=SqlQueries.create_data_tables,
    autocommit=True
)

modeling = DummyOperator(
    task_id='Join_Modeling',
    dag=dag
)

populate_time_table = PostgresOperator(
    dag=dag,
    task_id='populate_time_table',
    postgres_conn_id='redshift',
    sql=SqlQueries.move_time_data,
    autocommit=True
)

populate_ride_tables = PostgresOperator(
    dag=dag,
    task_id='populate_ride_tables',
    postgres_conn_id='redshift',
    sql=SqlQueries.move_ride_data,
    autocommit=True
)

start_quality_ckecks = DummyOperator(task_id='Start_Quality_Checks',  dag=dag)
end_quality_ckecks = DummyOperator(task_id='End_Quality_Checks',  dag=dag)

data_quality_integrity_checks = DataQualityOperator(
    task_id='Data_Quality_Integrity_Check',
    dag=dag,
    conn_id="redshift",
    checks=[
        (DataValidationQueries.data_in_taxi_rides_unique_integrity, 1),
        (DataValidationQueries.data_in_precipitation_unique_integrity, 1),
        (DataValidationQueries.data_in_taxi_zones_unique_integrity, 1),
    ],
)

data_quality_unit_checks = DataQualityOperator(
    task_id='Data_Quality_Unit_Check',
    dag=dag,
    conn_id="redshift",
    checks=[
        (DataValidationQueries.unit_test_in_time_table, True),
        (DataValidationQueries.unit_test_in_taxi_rides_and_time_tables, True),
    ],
)

data_quality_source_count_checks = DataQualityOperator(
    task_id='Data_Quality_Source_Count_Check',
    dag=dag,
    conn_id="redshift",
    checks=[
        (DataValidationQueries.data_in_taxi_rides_table_count, True),
        (DataValidationQueries.data_in_taxi_zones_table_count, True),
        (DataValidationQueries.data_in_time_table_count, True),
        (DataValidationQueries.data_in_precipitation_table_count, True),
    ],
)

# data_modeling_quality_checks = DataQualityOperator(
#     task_id='Model_data_quality_checks',
#     dag=dag,
#     conn_id="redshift",
#     target_tables=[
#         'time',
#         'taxi_rides'
#     ]
# )

data_analytics_queries = DataAnalysisOperator(
    task_id='Data_Analytics',
    dag=dag,
    redshift_conn_id="redshift",
    queries=SqlQueries.analysisQueries
)

end_modeling = DummyOperator(task_id='Finish_modeling_Redshift',  dag=dag)

start_modeling >> [prepare_stage_tables, setup_and_create_data_tables] >> modeling

modeling >> [populate_time_table, populate_ride_tables] >> start_quality_ckecks

start_quality_ckecks >> [data_quality_integrity_checks, data_quality_unit_checks, data_quality_source_count_checks] >> end_quality_ckecks

end_quality_ckecks >> data_analytics_queries >> end_modeling