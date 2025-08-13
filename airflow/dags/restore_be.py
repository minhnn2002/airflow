from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime


with DAG(
    dag_id='restore_starrocks-be',
    start_date=datetime(2025, 8, 11),
    schedule_interval=None,  
    catchup=False,
) as dag:
    
    restore_task = BashOperator(
        task_id='restore_be',
        bash_command='''
            mc alias set myminio ${MINIO_URL} ${MINIO_ACCESS} ${MINIO_SECRET}
            mc alias set aws_s3 ${AWS_URL} ${AWS_ACCESS} ${AWS_SECRET}
            mc mirror aws_s3/starrockk/be myminio/starrocks --overwrite
            mc anonymous set public myminio/starrocks
            ''',
    )

    restore_task