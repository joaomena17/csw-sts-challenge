import streamlit as st
import requests as r

def get_sensor_data(city, room):
    response = r.get(f"http://localhost:5000/sensors/{city}/{room}")
    data = response.json()
    st.write(data)

get_sensor_data("Porto", "Room 1")