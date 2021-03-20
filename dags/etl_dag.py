import datetime as dt
import etl

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    "owner": "abdullah reza",
    "depends_on_past": False,
    "email": ["air.reza@hotmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    'retry_delay': dt.timedelta(minutes=5),
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
    schedule_interval="@hourly"
)

etl_task = PythonOperator(
    task_id = "PGCB_ETL",
    python_callable=etl.main,
    dag=dag
)