import streamlit as st
import pandas as pd

from database import get_connection
from sql_queries import query8


def show_home():

    st.title("✈️ Air Tracker - Flight Analytics")
    st.subheader("Streamlit App for Exploration")

    conn = get_connection()

    # TOTAL AIRPORTS
    airport_query = "SELECT COUNT(icao_code) AS total_airports FROM airport"

    total_airport_df = pd.read_sql(airport_query, conn)

    # TOTAL FLIGHTS
    flight_query = "SELECT COUNT(flight_number) AS total_flights FROM flight"

    total_flight_df = pd.read_sql(flight_query, conn)

    # AVERAGE DELAY DATA
    avg_delay_df = pd.read_sql(query8, conn)

    conn.close()

    # VALUES
    total_airports = total_airport_df["total_airports"][0]

    total_flights = total_flight_df["total_flights"][0]

    avg_delay_df["delayed_departure"]=pd.to_numeric(avg_delay_df["delayed_departure"], errors="coerce")
    avg_delay_df["delayed_arrival"]=pd.to_numeric(avg_delay_df["delayed_arrival"], errors="coerce")

    avg_dep_delay = round(avg_delay_df["delayed_departure"].mean(), 2)

    avg_arr_delay = round(avg_delay_df["delayed_arrival"].mean(), 2)

    # METRICS
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Airports", total_airports)

    col2.metric("Total Flights", total_flights)

    col3.metric("Avg Departure Delay (min)", avg_dep_delay)

    col4.metric("Avg Arrival Delay (min)", avg_arr_delay)
    

    