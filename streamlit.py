import streamlit as st
from home import show_home
from airport_details import show_airport_details
from aircraft_details import show_aircraft_details
from analytics import show_analytics


st.set_page_config(page_title="✈️Air Tracker-Flight Analytics", layout="wide")

st.sidebar.title("Go To")
page = st.sidebar.radio("Select", ["Home", "Airport Details", "Aircraft Details", "Analytics"])

# -------------------------------- PAGE 1: Homepage --------------------------------
if page == "Home":
    show_home()
    st.image(r"airport_route.png", width="stretch")

# -------------------------------- PAGE 2: Airport Details --------------------------------
elif page == "Airport Details":
    show_airport_details()    

# -------------------------------- PAGE 3: Aircraft Details -------------------------------- 
elif page == "Aircraft Details":
    show_aircraft_details()

# -------------------------------- PAGE 4: Analytics -------------------------------- 
elif page == "Analytics":
    show_analytics()
     