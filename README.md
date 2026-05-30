# Air_Tracker-Flight_Analytics
## Table of Contents
- [Project Overview](#project-overview)
- [Objectives](#objectives)
- [Libraries](#libraries)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)

## Project Overview

The Air_Tracker-Flight_Analytics is a data analytics application built using Python, MySQL, and Streamlit. It provides insights into airport operations, flight performance, delays, aircraft usage, and route activity through interactive visualizations and SQL-powered analytics.

The dashboard enables users to explore flight data, identify trends, and monitor airline and airport performance.

## Objectives
The project aims to:
- Analyze airport and flight operations data.
- Track departure and arrival delays.
- Monitor airline performance.
- Visualize flight statistics using interactive charts.
- Demonstrate SQL querying, data analysis, and dashboard development skills.

## Libraries

- Python
- Pandas
- MySQL
- Streamlit
- NumPy
- Matplotlib
- Seaborn

## Project Structure
```text
Air Tracker-Flight Analytics/
│
├─streamlit.py
├─requirement.txt
├─database.py
├─datasources/
    ├─home.py
    ├─airport_details.py
    ├─aircraft_details.py
    └─analytics.py
├─sql_queries.py
└─assest/
    └─airport_route.png
```
## Setup Instructions
1. **Clone the Repository**-git clone https://github.com/HamsavarthiniN/Air_Tracker-Flight_Analytics.git
2. **Create a Virtual Environment**- python -m venv myenv
   - *Activate-Windows*-copy path of Activate.ps1 and paste in terminal  
4. **Install Dependencies**- pip install -r requirement.txt
5. **Configure Database**
   - Create a MySQL database:
   - CREATE DATABASE AeroDataBox;
   - Update database credentials in the project:
   * host="localhost"
   * user="root"
   * password="your_password"
   * database="AeroDataBox" 
7. **Running the Application**
   - streamlit run streamlit.py
