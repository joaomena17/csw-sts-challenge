import streamlit as st
import requests as r
         
def get_sensor_data(sensor_id):
    r.get(f"http://localhost:5000/sensors/{sensor_id}")

get_sensor_data(1234)