from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
import os


with DAG(
    dag_id='backup_starrocks_be',
    start_date=datetime(2025, 8, 11),
    schedule_interval='@daily',  
    catchup=False,
) as dag:
    
    backup_task = BashOperator(
        task_id='backup_minio_be',
        bash_command='''
            mc alias set myminio ${MINIO_URL} ${MINIO_ACCESS} ${MINIO_SECRET}
            mc alias set aws_s3 ${AWS_URL} ${AWS_ACCESS} ${AWS_SECRET}
            mc mirror myminio/starrocks aws_s3/starrockk/be --overwrite
            ''',
    )

    backup_task