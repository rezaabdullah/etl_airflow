# Airflow Tutorial
This tutorial demonstrates how to use Apache Airflow for workflow orchestration.

## Objective
The objective of the project is to demonstrate how to use Apache Airflow to orchestrate data pipeline. In this project, ETL workflow will be orchestrated by Apache Airflow.

## Problem Statement
Extract data from [Power Grid Company of Bangladesh](http://pgcb.gov.bd/site/page/0dd38e19-7c70-4582-95ba-078fccb609a8/-). Daily reports from the power generation companies are uploaded daily on the webpage. We will extract and read the report from the webpage, transform the data and load it into local database.

### Requirements and Constriants
1. In first run, read **only** the first page
2. Extract and read reports, transform the data and load it into a database
3. In subsequent run, perform ETL **only** for the newly added reports from the first page.

## Project Structure
```
root.
│   .env
│   .gitignore
│   docker-compose.yml
│   README.md
│   requirements.txt
│
├───dags
│       dummy_dag.py
│       etl_dag.py
│       extract_urls.py
│       transform_load.py
│
├───logs
└───scripts
        entrypoint.sh
```

## How to Run the Project
The project will run in Docker container. Therefore, ***Docker*** and ***Docker Compose*** must be installed on your workstation.
1. Install [Docker](https://docs.docker.com/engine/install/) on your workstation. 
2. Install [Docker Compose](https://docs.docker.com/compose/install/) on your workstation.

If ***Docker*** and ***Docker Compose*** are installed follow the steps below:
1. Download the project from [GitHub](https://github.com/rezaabdullah/etl_airflow): `git clone https://github.com/rezaabdullah/etl_airflow.git`
2. Once downloaded, go to the project directory
3. Open terminal or command prompt and enter `docker-compose up` or `docker-compose up -d`
4. It may take few minutes for the containers to download and install the required dependencies. Once the container is up, open browser and go to `localhost:8080`
5. User: `admin` and Password: `admin1234`
5. To run it once, trigger the `pgcb_etl` by clicking the play button under the **Actions** column
6. To run it continuously, **Unpause** the workflow left of **pgcb_etl**
7. You can watch the log files
![Airflow Homescreen](/static/airflow_homepage.jpg "Airflow Homepage")

## Airflow Overview
### Introduction
Airflow is a tool for automating and scheduling tasks and workflows. At its core, Airflow is simply a queuing system built on top of a metadata database. The database stores the state of queued tasks and a scheduler uses these states to prioritize how other tasks are added to the queue.

### Airflow Architecture
The architecture of Apache Airflow has four main components:
1. Metadata Database: This database stores information regarding the state of the tasks.
2. Scheduler: The Scheduler is a process that uses DAG definitions in conjunction with the state of tasks in the metadata database to decide which tasks need to be executed, as well as their execution priority.
3. Executor: The Executor is a message queuing process that is tightly bound to the Scheduler and determines the worker processes that actually execute each scheduled task.
4. Workers: These are the processes that actually execute the logic of tasks, and are determined by the Executor being used.  
![Airflow Architecture](/static/airflow_architecture.png "Airflow Architecture")

### Basic Concepts
1. DAGs: The core of the Airflow is the concept of DAG (Directed Acyclic Graph) which is a series of tasks that are part of the workflow. The workflow can be upstream (ETL) or downstream (visualization) or whole data pipeline. A DAG is written in python and **DAG_ID** is used extensively by the tool to orchestrate the running of the DAG.
2. DAG Run: DAG run must be specified via an execution_date and in a specific schedule.
3. Operators: An operator encapsulates the operation to be performed in each task in a DAG.

## Airflow Tutorial
We will deploy Airflow in Docker. Prerequisite:
1. [Docker](https://www.docker.com/get-started)
2. Docker Compose

### ETL Script
The ETL pipeline will extract data from [PGCB](http://pgcb.gov.bd/site/page/0dd38e19-7c70-4582-95ba-078fccb609a8/-) website, transform the data and load the data in Postgres DB. The ETL script for Airflow is divided into two subtasks: `extract_urls.py` and `transform_load.py`. `extract_urls.py` extracts the URLs from the PGCB website and `transform_load.py` transforms the data and load it two Postgres DB. `transform_load.py` is dependent on `extract_urls.py`.

### Define DAG
1. After importing necessary packages, first we define default arguments for DAGs.
```python
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
```
2. Next, DAG is defined. `schedule_interval` is `@daily`, meaning everyday at midnight the code will be executed and `catchup` is set to `False` for **NOT** backfilling the data.
```python
dag = DAG(
    "pgcb_etl",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False
)
```
3. Tasks for ETL are wrapped in DAG. Airflow has multiple [operators](https://airflow.apache.org/docs/apache-airflow/stable/python-api-ref.html#pythonapi-operators). To keep things simple and familiar, `BashOperator` was used.  
```python
extract = BashOperator(
    task_id = "extract_urls",
    bash_command="python /opt/airflow/dags/extract_urls.py",
    dag=dag
)

transform_load = BashOperator(
    task_id = "transform_load",
    bash_command="python /opt/airflow/dags/transform_load.py",
    dag=dag
)
```