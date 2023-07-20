from webbrowser import get
import streamlit as st
import requests as r
from flask import request

st.write("""
# STS Challenge - IoT Project
# """)

def get_sensor_data(sensor_id):
    r.get("http://localhost:5000", sensor_id)

get_sensor_data(1234)