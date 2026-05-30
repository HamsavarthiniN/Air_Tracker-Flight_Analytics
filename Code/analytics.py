import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
import numpy as np

from database import get_connection
from sql_queries import (query1, query2, query3, query4, query5, query6, query7, query8, query9, query10, query11)

conn=get_connection()

def show_analytics():
    st.title("📋 Frequently Asked questions")
    queries = {
        "1. Show the total number of flights for each aircraft model, listing the model and its count":query1,
        "2. List all aircraft (registration, model) that have been assigned to more than 5 flights":query2,
        "3. For each airport, display its name and the number of outbound flights, but only for airports with more than 5 flights":query3,
        "4. Find the top 3 destination airports (name, city) by number of arriving flights, sorted by count descending":query4,
        "5. Show for each flight: number, origin, destination, and a label 'Domestic' or 'International' using CASE WHEN on country match":query5,
        "6. Show the 5 most recent arrivals at “DEL” airport including flight number, aircraft, departure airport name, and arrival time, ordered by latest arrival":query6,
        "7. Find all airports with no arriving flights (never used as a destination in flights table)":query7,
        "8. For each airline, count the number of flights by status (e.g., 'On Time', 'Delayed', 'Cancelled') using CASE WHEN":query8,
        "9. Show all cancelled flights, with aircraft and both airports, ordered by departure time descending":query9,
        "10. List all city pairs (origin-destination) that have more than 2 different aircraft models operating flights between them":query10,
        "11. For each destination airport, compute the % of delayed flights (status='Delayed') among all arrivals, sorted by highest percentage":query11
    }

    def get_data(query):
        df=pd.read_sql(query, conn)
        return df
    
    selected_query = st.selectbox("Choose", list(queries.keys()))
    query_result= get_data(queries[selected_query])
    
    st.write("Result")
    st.dataframe(query_result, height=200)
    
    if selected_query == "1. Show the total number of flights for each aircraft model, listing the model and its count":
        st.bar_chart(query_result.set_index("model")["Total_flights"])
    elif selected_query == "2. List all aircraft (registration, model) that have been assigned to more than 5 flights":
        fig, ax = plt.subplots(figsize=(4, 2))
        
        sns.barplot(data=query_result, x="model", y="flight_count", ax=ax)
        
        ax.set_xlabel("Model")
        ax.set_ylabel("Number of Flights")

        st.pyplot(fig)
    elif selected_query == "3. For each airport, display its name and the number of outbound flights, but only for airports with more than 5 flights":
        fig, ax = plt.subplots(figsize=(4, 4))
        
        sns.barplot(data=query_result, x="number_of_outbound_flights", y="name", color="#a8325c", ax=ax)
        
        ax.set_xlabel("Number of Outbound Flights")
        ax.set_ylabel("Name")

        st.pyplot(fig)
    elif selected_query == "4. Find the top 3 destination airports (name, city) by number of arriving flights, sorted by count descending":
        fig, ax = plt.subplots(figsize=(4,2))
        
        sns.barplot(data=query_result, x="arriving_flights", y="name", color = "#71a832", ax=ax)
        
        ax.set_xlabel("Number of Arriving Flights")
        ax.set_ylabel("Name")

        st.pyplot(fig)
    elif selected_query == "5. Show for each flight: number, origin, destination, and a label 'Domestic' or 'International' using CASE WHEN on country match":
        flight_counts = query_result["flight_type"].value_counts()
        fig, ax = plt.subplots(figsize=(1.5,1.5))
        
        ax.pie(flight_counts.values, labels = flight_counts.index, autopct="%1.1f%%")    
        
        st.pyplot(fig)
    elif selected_query == "7. Find all airports with no arriving flights (never used as a destination in flights table)":
        st.write("No City Found")
    elif selected_query == "8. For each airline, count the number of flights by status (e.g., 'On Time', 'Delayed', 'Cancelled') using CASE WHEN":
        #CREATE POSITIONs
        y = np.arange(len(query_result["airline"]))
        width = 0.2
        height = 0.3
        fig, ax = plt.subplots(figsize=(10,10))
        ax.barh(y - 1.5*width, query_result["delayed_departure"], label="Delayed Departure", height = height)
        ax.barh(y - 0.5*width, query_result["on_time_departure"], label="On-time Departure", height = height)

        ax.barh(y + 0.5*width, query_result["delayed_arrival"], label="Delayed Arrival", height = height)
        ax.barh(y + 1.5*width, query_result["on_time_arrival"],  label="On-time Arrival", height = height)

        ax.set_yticks(y)
        ax.set_yticklabels(query_result["airline"], rotation=45)
        ax.legend()
        ax.set_title("Airline Delay Analysis")

        st.pyplot(fig)
    elif selected_query == "10. List all city pairs (origin-destination) that have more than 2 different aircraft models operating flights between them":
        print("wait")
    elif selected_query == "11. For each destination airport, compute the % of delayed flights (status='Delayed') among all arrivals, sorted by highest percentage":
        print("wait")

    
    




