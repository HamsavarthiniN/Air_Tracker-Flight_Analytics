import streamlit as st
import pandas as pd

from database import get_connection

conn = get_connection()

def show_airport_details():

    # LOAD DATA FROM SQL
    @st.cache_data
    def load_airports():
        query = "SELECT * FROM airport"
        return pd.read_sql(query, conn)

    @st.cache_data
    def load_flights():

        query = """SELECT flight_id, flight_number, aircraft_registration, origin_icao, destination_icao, 
                    scheduled_departure, actual_departure, scheduled_arrival, actual_arrival, status, airline_code
                    FROM flight LEFT JOIN aircraft
                    ON flight.aircraft_registration = aircraft.aircraft_code"""

        df = pd.read_sql(query, conn)

        # Convert datetime columns
        datetime_cols = ["scheduled_departure", "actual_departure", "scheduled_arrival", "actual_arrival"]

        for col in datetime_cols:
            df[col] = pd.to_datetime(df[col], errors="coerce")

        return df

    airport_df = load_airports()
    flight_df = load_flights()
    

    st.sidebar.title("Air Tracker")

    selected_airport = st.sidebar.selectbox("Select Airport", sorted(airport_df["icao_code"].dropna().unique()))

    selected_flight_type = st.sidebar.selectbox("Select Flight Type", ["All", "Departure", "Arrival"])

    if selected_flight_type == "All":

        filtered_flights_df = flight_df[(flight_df["origin_icao"] == selected_airport) |
                                        (flight_df["destination_icao"] == selected_airport)]

    elif selected_flight_type == "Departure":

        # Match selected airport against the origin column
        filtered_flights_df = flight_df[flight_df["origin_icao"] == selected_airport]

    else:

        # Match selected airport against the destination column
        filtered_flights_df = flight_df[flight_df["destination_icao"] == selected_airport]

    # Extract only the unique flight numbers
    dynamic_flight_list = (filtered_flights_df["flight_number"].dropna().unique())

    # Pass the dynamic list to the selectbox
    selected_flight = st.sidebar.selectbox("Select Flight", ["All Flights"] + list(dynamic_flight_list))

    # AIRPORT EXPLORATION
    st.header("🌍 Airport Details")

    airport_info = airport_df[airport_df["icao_code"] == selected_airport]

    if not airport_info.empty:

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Airport", str(airport_info.iloc[0]["name"]))

        with col2:
            st.metric("City", airport_info.iloc[0]["city"])

        with col3:
            st.metric("Timezone", airport_info.iloc[0]["timezone"])

        st.dataframe(airport_info.iloc[:, 1:], use_container_width=True)

    # ---------------- ALL ----------------

    if selected_flight_type == "All":

        st.header("🛫 Departure Flights")

        # Departure filter
        if selected_flight == "All Flights":

            flight_departure_info = flight_df[flight_df["origin_icao"] == selected_airport]

        else:

            flight_departure_info = flight_df[(flight_df["origin_icao"] == selected_airport) &
                                              (flight_df["flight_number"] == selected_flight)]

        if not flight_departure_info.empty:

            st.dataframe(flight_departure_info.iloc[:, [1, 3, 4, 5, 6, 9]], use_container_width=True)

        else:
            st.info("No matching departure flights found.")

        st.header("🛬 Arrival Flights")

        # Arrival filter
        if selected_flight == "All Flights":

            flight_arrival_info = flight_df[flight_df["destination_icao"] == selected_airport]

        else:

            flight_arrival_info = flight_df[(flight_df["destination_icao"] == selected_airport) &
                                            (flight_df["flight_number"] == selected_flight)]

        if not flight_arrival_info.empty:

            st.dataframe(flight_arrival_info.iloc[:, [1, 3, 4, 7, 8, 9]], use_container_width=True)

        else:
            st.info("No matching arrival flights found.")

    # ---------------- DEPARTURE ----------------

    elif selected_flight_type == "Departure":

        st.header("🛫 Departure Flights")

        if selected_flight == "All Flights":

            flight_departure_info = flight_df[flight_df["origin_icao"] == selected_airport]

        else:

            flight_departure_info = flight_df[(flight_df["origin_icao"] == selected_airport) &
                                              (flight_df["flight_number"] == selected_flight)]

        if not flight_departure_info.empty:

            st.dataframe(flight_departure_info.iloc[:, [1, 3, 4, 5, 6, 9]], use_container_width=True)

        else:
            st.info("No matching departure flights found.")

    # ---------------- ARRIVAL ----------------

    elif selected_flight_type == "Arrival":

        st.header("🛬 Arrival Flights")

        if selected_flight == "All Flights":

            flight_arrival_info = flight_df[flight_df["destination_icao"] == selected_airport]

        else:

            flight_arrival_info = flight_df[(flight_df["destination_icao"] == selected_airport) &
                                            (flight_df["flight_number"] == selected_flight)]

        if not flight_arrival_info.empty:

            st.dataframe(flight_arrival_info.iloc[:, [1, 3, 4, 7, 8, 9]], use_container_width=True)

        else:
            st.info("No matching arrival flights found.")