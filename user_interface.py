import streamlit as st
import requests as r
         
def get_sensor_data(sensor_id):
    r.get("http://localhost:5000", sensor_id)

get_sensor_data(1234)