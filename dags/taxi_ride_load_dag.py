"""
DAG is a compilation and arrangement of tasks to be run on a monthly basis.
"""
from datetime import datetime, timedelta
import logging
import os
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.amazon.aws.operators.s3_copy_object import S3CopyObjectOperator
from helpers import SqlQueries
from operators import S3ToRedshiftOperator, DataQualityOperator, DataAnalysisOperator, RenderToS3Operator

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

dag = DAG('NYC_TLC_LOAD_DAG',
          default_args=default_args,
          description='Prepare tables and load monthly data from S3 to Redshift for processing',
          schedule_interval='@monthly',
          catchup=False,
          tags=['Load', 'Dataset', 'Redshift'],
          )

start_tables = DummyOperator(
    task_id='prepare_S3_Redshift_Start',  dag=dag)

clean_all_tables = PostgresOperator(
    dag=dag,
    task_id='truncate_all_tables',
    postgres_conn_id='redshift',
    sql=SqlQueries.drop_all_tables,
    autocommit=True
)

setup_tables = PostgresOperator(
    dag=dag,
    task_id='create_stage_tables',
    postgres_conn_id='redshift',
    sql=SqlQueries.create_stage_tables,
    autocommit=True
)

finish_tables = DummyOperator(
    task_id='prepare_S3_Redshift_End',  dag=dag)


start_load = DummyOperator(
    task_id='Load_from_S3_to_Redshift_Start',  dag=dag)


task_taxi_zones_s3_to_redshift = S3ToRedshiftOperator(
    dag=dag,
    s3_bucket='udacity-data-lake',
    s3_key='data/taxi_zones.json',
    schema="PUBLIC",
    table='taxi_zones',
    copy_options=[ 'json \'s3://udacity-data-lake/data/taxi_paths.json\'', 'region \'us-east-2\''],
    task_id='transfer_taxi_zones_s3_to_redshift',
)

task_precipitation_s3_to_redshift = S3ToRedshiftOperator(
    dag=dag,
    s3_bucket='udacity-data-lake',
    s3_key='data/precipitation.json',
    schema="PUBLIC",
    table='precipitation',
    copy_options=[ 'json \'s3://udacity-data-lake/data/precipitation_paths.json\'', 'region \'us-east-2\''],
    task_id='transfer_precipitation_s3_to_redshift',
)

task_green_s3_to_redshift = S3ToRedshiftOperator(
    dag=dag,
    s3_bucket='nyc-tlc',
    s3_key='trip data/green_tripdata_2020-12.csv',
    schema="PUBLIC",
    table='stage_green',
    copy_options=[ 'IGNOREHEADER 1', 'DELIMITER \',\'', 'IGNOREBLANKLINES', 'REMOVEQUOTES', 'EMPTYASNULL', 'region \'us-east-1\''],
    task_id='transfer_green_s3_to_redshift',
)

task_yellow_s3_to_redshift = S3ToRedshiftOperator(
    dag=dag,
    s3_bucket='nyc-tlc',
    s3_key='trip data/yellow_tripdata_2020-12.csv',
    schema="PUBLIC",
    table='stage_yellow',
    copy_options=[ 'IGNOREHEADER 1', 'DELIMITER \',\'', 'IGNOREBLANKLINES', 'REMOVEQUOTES', 'EMPTYASNULL', 'region \'us-east-1\''],
    task_id='transfer_yellow_s3_to_redshift',
)

task_fhv_s3_to_redshift = S3ToRedshiftOperator(
    dag=dag,
    s3_bucket='nyc-tlc',
    s3_key='trip data/fhv_tripdata_2020-12.csv',
    schema="PUBLIC",
    table='stage_fhv',
    copy_options=[ 'IGNOREHEADER 1', 'DELIMITER \',\'', 'IGNOREBLANKLINES', 'REMOVEQUOTES', 'EMPTYASNULL', 'region \'us-east-1\''],
    task_id='transfer_fhv_s3_to_redshift',
)

task_fhvhv_s3_to_redshift = S3ToRedshiftOperator(
    dag=dag,
    s3_bucket='nyc-tlc',
    s3_key='trip data/fhvhv_tripdata_2020-12.csv',
    schema="PUBLIC",
    table='stage_fhvhv',
    copy_options=[ 'IGNOREHEADER 1', 'DELIMITER \',\'', 'IGNOREBLANKLINES', 'REMOVEQUOTES', 'EMPTYASNULL', 'region \'us-east-1\''],
    task_id='transfer_fhvhv_s3_to_redshift',
)

task_redshift_initial_data_quality = DataQualityOperator(
    task_id='task_redshift_staging_data_quality',
    dag=dag,
    conn_id='redshift',
    target_tables=[
        'taxi_zones',
        'stage_green',
        'stage_yellow',
        'stage_fhv',
        'stage_fhvhv'
    ]
)

end_load = DummyOperator(
    task_id='Load_from_S3_to_Redshift_End',  dag=dag)

# [END howto_operator_s3_to_redshift_task_1]


start_tables >> clean_all_tables >> setup_tables >> finish_tables

finish_tables >> start_load 

start_load >> [task_taxi_zones_s3_to_redshift, task_precipitation_s3_to_redshift, task_green_s3_to_redshift, task_yellow_s3_to_redshift, task_fhv_s3_to_redshift, task_fhvhv_s3_to_redshift ] 

[task_taxi_zones_s3_to_redshift, task_precipitation_s3_to_redshift, task_green_s3_to_redshift, task_yellow_s3_to_redshift, task_fhv_s3_to_redshift, task_fhvhv_s3_to_redshift ]  >> task_redshift_initial_data_quality

task_redshift_initial_data_quality >> end_load