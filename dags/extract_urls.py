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

# Libraries to extract files
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime
import json

# Initialization & constants
TARGET_URL = "http://pgcb.gov.bd/site/page/0dd38e19-7c70-4582-95ba-078fccb609a8/-"
# DOWNLOAD_DIR = "../excel_files"
URL_LIST = "/opt/airflow/logs/url_list.json"

# Function to get file URLs
def extract_files(TARGET_URL, URL_LIST):
# def extract_files():
    """
    This function gets the list of links for the files that are needed to be 
    downloaded from a webpage.
    :param TARGET_URL: webpage url
    :param LOG_PATH: directory where log file of last downloaded URLs
    :type TARGET_URL: string
    :type LOG_PATH: list
    :return msg: function completion message
    :rtype msg: string
    """
    
    # Check the status of the download operation
    if Path(URL_LIST).exists():
        with open(URL_LIST, "r") as file:
            last_status = json.load(file)
            url_list = last_status["url_list"]
    else:
        url_list = []

    try:
        # Retrieve webpage HTML code
        response = requests.get(TARGET_URL)
        response.raise_for_status()
        
        # Parse the webpage HTML code
        soup = BeautifulSoup(response.content, "html.parser")
        
        # The downloadable files are inside iframe tag and can be identified by report_by_category
        for frame in soup.find_all("iframe"):
            if "report_by_category" in frame["src"]:
                repository = frame["src"]
                
        # Retrieve repository HTML code
        response = requests.get(repository)
        response.raise_for_status()

        # Parse the HTML code
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Iterate through all the href to find relevant data (.xls/.xlsm)
        for link in soup.find_all("a", target = "_blank"):
            url = link.get("href")
            url = url.strip()
            if url not in url_list:
                url_list.append(url)
        msg = "URL extraction successful"

    except requests.exceptions.RequestException as e:
        print(e)
        msg = "URL extraction failed"
        url_list = []
    finally:
        # Store the status of the extraction
        status = {
            "last_operation" : datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "url_list" : url_list,
            "msg" : msg
        }
        with open(URL_LIST, "w") as file:
            json.dump(status, file, indent = 4)

        print("URL extraction complete")

def main():
    extract_files(TARGET_URL, URL_LIST)

# Main Function
if __name__ == "__main__":
    main()