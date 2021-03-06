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
etl_airflow.
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

## How to Run Workflows in Airflow
### DAG
A DAGfile is nothing but a python script. In general, we specify DAGs in a single `.py` file which is stored in `dags` directory. However, for advance and complex workflows, [**Packaged DAGs**](https://airflow.apache.org/docs/apache-airflow/stable/concepts.html#packaged-dags) can be used. For example, in our current project we have two DAGs: `dummy_dag.py` and `etl_dag.py`. Referring to `etl_dag.py`, the steps for define and declaring a DAG is written below:
1. First, we import python packages such as `datetime`, `airflow` etc.
```python
import datetime as dt

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
```
2. Next, we define default arguments for DAGs.
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
}
```
3. Subsequently, we declare a DAG.
```python
dag = DAG(
    "pgcb_etl",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False
)
```
4. Once a DAG is declared, we define tasks for the DAG. For example, task `extract` is defined and declared in the following code snippet. In this example, we used ***`BashOperator`***.
```python
extract = BashOperator(
    task_id = "extract_urls",
    bash_command="python /opt/airflow/dags/extract_urls.py",
    dag=dag
)
```
5. Lastly, we define dependencies.
```python
extract >> transform_load
```

** Details how-to guide can be found in [How-To Guides](https://airflow.apache.org/docs/apache-airflow/stable/howto/index.html)

** For more details on Airflow, refer to the project [wiki](https://github.com/rezaabdullah/etl_airflow/wiki).