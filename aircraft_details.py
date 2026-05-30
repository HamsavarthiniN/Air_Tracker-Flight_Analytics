import streamlit as st
import pandas as pd

from database import get_connection

conn = get_connection()

def show_aircraft_details():
    
    @st.cache_data
    def load_aircraft():
        query = """SELECT model, aircraft_code, aircraft_type, airline, engine, flight_number, origin_icao AS origin,
                    destination_icao as destination
                    FROM aircraft LEFT JOIN flight ON aircraft_code = aircraft_registration"""
        return pd.read_sql(query, conn)
    
    aircraft_df = load_aircraft()

    st.sidebar.title("Model")
    selected_model = st.sidebar.selectbox("Select Model", aircraft_df["model"].unique())
        
    #FILTERED FLIGHTS FOR THAT PARTICULAR AIRPORT
    filtered_flights=aircraft_df[aircraft_df["model"]==selected_model]

    #EXTRACT FLIGHT NUMBERS
    filtered_number = sorted(filtered_flights["flight_number"].dropna().unique())

    st.header("🛫 Aircrafts") 
    aircraft_info =aircraft_df[aircraft_df["model"]==selected_model]
    if not aircraft_info.empty:
        st.dataframe(filtered_flights)

