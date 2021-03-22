import datetime as dt
import etl

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

# # Libraries to extract files
# import requests
# # from bs4 import BeautifulSoup
# from bs4 import BeautifulSoup
# from pathlib import Path
# from datetime import datetime
# import json
# import wget

# # Libraries to transform data
# import numpy as np
# import pandas as pd
# import openpyxl

# # Libraries to load data
# # import sqlite3
# # from sqlite3 import Error
# import psycopg2
# from sqlalchemy import create_engine
# from sqlalchemy.types import Integer, Text, Float, Date

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    "owner": "abdullah reza",
    "depends_on_past": False,
    "email": ["air.reza@hotmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": dt.timedelta(minutes=5),
    "start_date": dt.datetime(2021, 3, 21)
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

# schedule_interval=timedelta(days=1) 
# with DAG("pgcb_etl", default_args=default_args, schedule_interval="@hourly") as dag:
dag = DAG(
    "pgcb_etl",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False
)

# etl_task = PythonOperator(
#     task_id = "PGCB_ETL",
#     python_callable=etl.extract_files,
#     dag=dag
# )

extract_url = BashOperator(
    task_id = "extract_urls",
    bash_command="python /opt/airflow/dags/extract_urls.py",
    dag=dag
)