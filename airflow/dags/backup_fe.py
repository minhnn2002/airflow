from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime

def upload_to_s3(filename, key, bucket_name):
    hook = S3Hook('aws_s3')
    hook.load_file(filename=filename, key=key, bucket_name=bucket_name)

with DAG(
    dag_id="backup_starrocks_fe",
    start_date=datetime(2025, 8, 11),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    backup_and_copy = BashOperator(
        task_id="backup_and_copy",
        bash_command=(
            'sshpass -p "password" ssh -o StrictHostKeyChecking=no '
            '-p 2222 root@starrocks-fe '
            '"tar -czvf /tmp/fe.tar.gz -C /opt/starrocks/fe ."'
        )
    )

    copy_zip = BashOperator(
        task_id="copy_zip",
        bash_command=(
            'sshpass -p "password" scp -P 2222 root@starrocks-fe:/tmp/fe.tar.gz /tmp/fe.tar.gz'
        )
    )

    upload = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_to_s3,
        op_kwargs={
            'filename': "/tmp/fe.tar.gz",
            'key': 'fe/fe.tar.gz',
            'bucket_name': 'starrockk'
        }
    )

    backup_and_copy >> copy_zip >> upload
