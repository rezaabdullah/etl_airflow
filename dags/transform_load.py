#!/usr/bin/python3

# Task 1a
"""
Problem Statement:
1. Download files from the webpage:
    http://pgcb.gov.bd/site/page/0dd38e19-7c70-4582-95ba-078fccb609a8/-
2. When executed for the first time, the program should download files from the first page only
3. In subsequent execution, the program should download the newly added files
3. Schedule the script to run daily i.e. every 24 hours
4. After downloading the excel (.xls/.xlsm) file, clean the data that must satisfy following criteria:
    a. Data should be extracted from the excel sheet named “Forecast”
    b. Find and remove aggregated data such as Total or Area Total
    c. Show only individual features and the observations
    d. Store the data in Database or CSV files
Author  : Abdullah Reza
Date    : 20/01/2021
"""

# Libraries to read data
import json
# import wget

# Libraries to transform data
import numpy as np
import pandas as pd
import openpyxl

# Libraries to load data
# import sqlite3
# from sqlite3 import Error
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Text, Float, Date

# List of URLs to download data
URL_LIST = "/opt/airflow/logs/url_list.json"

# Function to transform data
def transform_data(URL_LIST):
    """
    This function reads URLs from URL_LIST and download the excel files
    and transform the data.
    :param URL_LIST: path of the excel file (string)
    :type URL_LIST: string
    :return df: transformed dataframe
    :rtype df: pandas dataframe
    """

    url_list = []
    with open(URL_LIST, "r") as file:
        status = json.load(file)
        url_list = status["url_list"]
    
    # Read excel reports from the links
    for url in url_list:
        df = pd.read_excel(url, sheet_name = "Forecast", engine="openpyxl")

        # Rename columns for easier handling
        df.columns = range(df.shape[1])
        # Reset row indices
        df.reset_index(drop = True, inplace = True)

        # Extract date
        date = df.where(df == "Date (day):").dropna(how="all").dropna(axis=1)
        date_row = date.index[0]
        date_columns = date.columns[0] + 1
        date = df.iat[date_row, date_columns]
        date = date.strftime("%m/%d/%Y")
        print("Data from ")

        # Slice dataframe to exclude redundant information i.e. aggregated information
        # Find start_row: 3 row below "Name of the Power Station"
        # Find start_col: Column of "Name of the Power Station"
        # Find last_row: Exclude all information below "Total"  
        power_station = df.where(df == "Name of the Power Station").dropna(how="all").dropna(axis=1)
        start_row = power_station.index[0] + 3
        start_col = power_station.columns[0]
        # total = df.where(df == "Total").dropna(how="all").dropna(axis=1)
        # last_row = total.index[0]
        last_row = -42
        df = df.iloc[start_row:last_row, start_col:]

        # Drop column 3 & column 16 which are adjacent column for power_station_name and
        # maintenance_remark respectively
        df.drop(columns = [3, 16, 18], inplace = True)

        # Column header
        header = ["power_station_name", "fuel_type", "producer", "install_capacity", "total_capacity", "current_capacity",
                "prev_day_power_gen_peak", "prev_ev_power_gen_peak", "current_day_forecast_peak", "current_ev_forecast_peak",
                "gen_short_fuel", "gen_short_plant_issue", "maintenance_remark", "start_up_date"]
        # Rename column headers
        df.columns = header

        # Remove rows with aggregated information such as "area Total" or "Total"
        df = df[~df.power_station_name.str.contains("Total")]

        # Change data types for the numerical columns
        df = df.astype({"power_station_name" : "str",
                        "fuel_type" : "str",
                        "producer" : "str",
                        "install_capacity" : "str",
                        "total_capacity" : "float",
                        "current_capacity" : "float",
                        "prev_day_power_gen_peak" : "float",
                        "prev_ev_power_gen_peak" : "float",
                        "current_day_forecast_peak" : "float",
                        "current_ev_forecast_peak" : "float",
                        "gen_short_fuel" : "float",
                        "gen_short_plant_issue" : "float",
                        "maintenance_remark" : "str",
                        "start_up_date" : "str"})
    
        # Remove unnecessary whitespaces
        for column in df.columns:
            if df[column].dtype != np.number:
                df[column] = [" ".join(name.split()) for name in df[column].str.strip()]

        # Convert start_up_date to Date column
        # df["start_up_date"] = df["start_up_date"].astype(np.datetime64).fillna(pd.NaT)

        # Insert date column at the beginning of the dataframe
        df.insert(loc = 0, column = "report_date", value = date)

        # Load the transformed data
        load_data(df)

# Insert dataframe values to table
def load_data(df):
    """
    Load pandas dataframe and insert the data to the table
    :param table_name: table name in the database to insert the data into
    :param csv_file: path of the csv file to process
    :return: None
    """

    # Create the engine to connect to the PostgreSQL database
    # engine = create_engine("postgres+psycopg2://postgres:postgres@localhost/postgres", echo=True)
    engine = create_engine("postgres+psycopg2://postgres:postgres@postgres:5432/postgres", echo=True)

    # Schema
    data_type = {
        "report_date" : Date,
        "power_station_name" : Text,
        "fuel_type" : Text,
        "producer" : Text,
        "install_capacity" : Text,
        "total_capacity" : Integer,
        "current_capacity" : Integer,
        "prev_day_power_gen_peak" : Integer,
        "prev_ev_power_gen_peak" : Integer,
        "current_day_forecast_peak" : Integer,
        "current_ev_forecast_peak" : Integer,
        "gen_short_fuel" : Integer,
        "gen_short_plant_issue" : Integer,
        "maintenance_remark" : Text,
        "start_up_date" : Text
    }

    try:
        frame = df.to_sql('pgcb', engine, if_exists="append", index=False, dtype=data_type)
    except ValueError as vx:
        print(vx)
    except Exception as ex:  
        print(ex)
    else:
        print("PostgreSQL Table {} has been created successfully.".format("pgcb"))

def main():
    transform_data(URL_LIST)

# Main Function
if __name__ == "__main__":
    main()