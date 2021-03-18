# Airflow Tutorial
This tutorial demonstrates how to use Apache Airflow for workflow orchestration.

## Problem Statement
Perform ETL job from PGCB website. Extract daily reports from the first page, clean the data and store it in database. The script will only extract the new reports from the first page; meaning if ETL job already download data from previous days, it will only download report of the current day.

## Project Structure
```
etl_airflow
|--etl
|  |--Dockerfile
|  |--etl.py
|  |--requirements.txt
|--.gitignore
|--docker-compose.yml
|--README.md
```