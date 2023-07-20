from flask import Flask, jsonify, request
import paho.mqtt.client as mqtt
import json
import sys
from time import time
import random
import requests
from pytimedinput import timedInput


# siddhi event processor
target_url = "http://0.0.0.0:7370/SummerCampSTS"         #alterar?

#variables
CURRENT_OFFICE_ID = 5467  # get real  ID?
OFFICE_CAPACITY = 300
ROOM_CAPACITY = 10


client = mqtt.Client(client_id="meu_cliente")

#Sensor/publisher subscription
client.subscribe("sensores/temperatura", qos=1) # 1: at least once
client.subscribe("sensores/presenca", qos=1) # 1: at least once

#Sensor unsubscription
client.unsubscribe("sensores/temperatura") 
client.unsubscribe("sensores/presenca") 

#Random values generator
def temperature_generator():
    i = random.randint(1, 100)
    if i < 5:
        return random.randint(700, 750)  # simulate high temperature
    elif i > 95:
        return random.randint(751, 800)  # simulate very high temperature
    return random.randint(600, 699)  # standard temperature


# implements a random number of new passengers until the capacity is reached
def passengers_generator(curr_occupants):
    if curr_occupants < OFFICE_CAPACITY:
        return curr_occupants + random.randint(1, min(10, OFFICE_CAPACITY - curr_occupants))
    return curr_occupants

# sets a cooldown interval between 1 and 6 minutes      #???
def interval_generator():
    return random.randint(60, 360)

# initializes the event         #change specific case
def profiler():
    return {
        'office_id': f'{CURRENT_OFFICE_ID}',    
        'temp': random.randint(600, 699),
        'occupants': random.randint(150, 250)
    }

# event with all attributes set to one to indicate trip start
def start_event():
    return {
        'office_id': f'{CURRENT_OFFICE_ID}',     
        'temp': 1,
        'occupants': 1
    }
# event with all attributes set to zero to indicate trip end
def end_event():
    return {
        'office_id': f'{CURRENT_OFFICE_ID}',    
        'temp': 0,
        'occupants': 0
    }


# updates the event with a different temperature value
def change_temperature(event):
    event['temp'] = temperature_generator()
    return event


# updates the event with a different occupants value
def change_passengers(event):
    event['occupants'] = passengers_generator(event['occupants'])
    return event


# post request with event data do siddhi event processor
def publish_event(event):
    # post updated event
    r = requests.post(url=target_url, data=json.dumps(event), headers={"Content-Type": "application/json; "
                                                                                       "charset=utf-8"})
    # check response
    if r.status_code == 200:
        return True
    return False


#Publish topic              #insert random values?
client.publish("sensores/temperatura","20")