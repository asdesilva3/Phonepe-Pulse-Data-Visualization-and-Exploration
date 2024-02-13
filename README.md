# Phonepe Pulse Data Visualization and Exploration

## Table of Contents
1. [Introduction](#introduction)
2. [Technologies Used](#technologies-used)
3. [Guide](#guide)
4. [Domain](#domain)
5. [Problem Statement](#problem-statement)
6. [Solution Steps](#solution-steps)
7. [Approach](#approach)
8. [Dataset](#dataset)

## Introduction
This project aims to create a user-friendly tool for visualizing and exploring data from the Phonepe Pulse GitHub repository. The Phonepe Pulse repository contains a vast amount of data related to various metrics and statistics. The goal here is to extract this data, process it, and visualize it in an interactive and visually appealing manner using Streamlit and Plotly.

## Technologies Used
For this project, we'll be utilizing technologies such as:
- GitHub Cloning
- Python
- Pandas
- MySQL
- mysql-connector-python
- Streamlit
- Plotly
  
## Guide
- Aggregated: Aggregated values of various payment categories as shown under Categories section
- Map: Total values at the State and District levels.
- Top: Totals of top States / Districts /Pin Codes

## Domain
Fintech

## Problem Statement
The Phonepe Pulse GitHub repository contains a large amount of data related to various metrics and statistics. Our aim is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.

### Solution Steps:
1. **Data Extraction**: We'll clone the GitHub repository using scripting to fetch the data and store it.
2. **Data Transformation**: Using Python and Pandas, we'll clean and preprocess the data.
3. **Database Insertion**: We'll insert the transformed data into a MySQL database for efficient storage and retrieval.
4. **Dashboard Creation**: Using Streamlit and Plotly, we'll create an interactive dashboard to display the data.
5. **Data Retrieval**: We'll fetch data from the MySQL database to display in the dashboard.
6. **User Interface**: Providing dropdown options for users to select different facts and figures to display on the dashboard.

## Approach
Approach involves the following steps:

1. **Data Extraction**: Scripting to fetch data from GitHub repository.
2. **Data Transformation**: Using Python and Pandas for data cleaning and preprocessing.
3. **Database Insertion**: Utilizing mysql-connector-python to insert data into MySQL.
4. **Dashboard Creation**: Creating an interactive dashboard using Streamlit and Plotly.
5. **Data Retrieval**: Fetching data from MySQL using mysql-connector-python.
6. **Deployment**: Ensuring security, efficiency, and user-friendliness, then deploying the dashboard.

## Dataset
- Dataset Link: [Data Link](https://github.com/PhonePe/pulse)
- Inspired From: [PhonePe Pulse](https://www.phonepe.com/pulse/)
