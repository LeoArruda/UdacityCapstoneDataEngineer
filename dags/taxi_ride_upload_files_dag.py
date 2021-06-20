"""
DAG #2: This DAG is a compilation and arrangement of tasks to copy data from files stored into an S3 bucket and
insert it into the Redshift staging tables.
"""
import os
import logging
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from operators import (RenderToS3Operator)

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

dag = DAG('NYC_TLC_UPLOAD_FILES_DAG',
          default_args=default_args,
          description='Load Precipitation and Taxi Zones data to S3 for processing',
          schedule_interval='@monthly',
          catchup=False,
          tags=['Load', 'Dataset', 'S3'],
          )

content_list = os.listdir(LOCAL_DIR)
dir_list = filter(
    lambda x: os.path.isdir(
        os.path.join(LOCAL_DIR, x)), content_list)

logging.info('Uploading : {}'.format(dir_list))

print('Uploading : {}'.format(dir_list))

start_upload = DummyOperator(
    task_id='Upload_To_S3_Start',  dag=dag)

end_upload = DummyOperator(
    task_id='Upload_To_S3_Finalized',  dag=dag)

render_to_s3 = RenderToS3Operator(
        task_id='Render_To_S3',
        dag=dag,
        local_output=False,
        migrate_output=True,
        local_output_data_path=LOCAL_DIR,
        s3_bucket_name_prefix='udacity-data-lake',
        data_folders=dir_list,
        input_data_path=LOCAL_DIR,
        aws_connection_id='aws_credentials',
        aws_default_region='us-east-2',
)

start_upload >> render_to_s3 >> end_upload