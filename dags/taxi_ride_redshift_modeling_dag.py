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
from helpers import SqlQueries
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

data_modeling_quality_checks = DataQualityOperator(
    task_id='Model_data_quality_checks',
    dag=dag,
    conn_id="redshift",
    target_tables=[
        'time',
        'taxi_rides'
    ]
)

data_analytics_queries = DataAnalysisOperator(
    task_id='Data_Analytics',
    dag=dag,
    redshift_conn_id="redshift",
    queries=SqlQueries.analysisQueries
)

end_modeling = DummyOperator(task_id='Finish_modeling_Redshift',  dag=dag)


start_modeling >> [prepare_stage_tables, setup_and_create_data_tables] >> modeling

modeling >> [populate_time_table, populate_ride_tables] >> data_modeling_quality_checks

data_modeling_quality_checks >> data_analytics_queries >> end_modeling