from flask import Flask, jsonify, request
import paho.mqtt.client as mqtt
import json
import sys
#import numpy as np
from time import time
import random
import threading
import time
#import requests
#from pytimedinput import timedInput


#variables
OFFICE_LIST = ["Lisboa", "Coimbra", "Tomar", "Viseu", "Porto", "Vila Real"]
BUILDING_LIST = ["Buiding1", "Building2"]
ROOM_LIST = ["Room1","Room2", "Room3", "Building"]

OFFICE_MAX_CAPACITY = 300
ROOM_CAPACITY = 20
connected = False
office_occupants=0
room_occupants=0
timer = 1

# MQTT Broker Configuration
broker_adress = "test.mosquitto.org" # Broker Adress  
broker_port = 1883 # MQTT port
      
# sets a cooldown interval between 1 and 6 minutes      
def interval_generator():
    return random.randint(60, 360)

######## Random values generator ########
def temperature_generator():
    i = random.randint(1, 100)
    if i < 50:
        return random.randint(15, 20)  # simulate high temperature
    elif i > 90:
        return random.randint(30, 35)  # simulate very high temperature
    return random.randint(20, 30)  # standard temperature

def office_generator():
    i = random.randint(0, 5)
    cur_office = OFFICE_LIST[i]
    return cur_office

def building_generator():
    i = random.randint(0,1)
    cur_building = BUILDING_LIST[i]  
    return cur_building

def room_and_occupants_generator(curr_office_occupants, curr_room_occupants):
    i = random.randint(0, 3)
    cur_room = ROOM_LIST[i]
    
    if (cur_room == "Building"):           
        if curr_office_occupants < OFFICE_MAX_CAPACITY:        
            curr_office_occupants = curr_office_occupants + random.randint(1, min(10, OFFICE_MAX_CAPACITY - curr_office_occupants))            
    else: 
        #curr_room_occupants = curr_room_occupants + random.randint(1, min(2, ROOM_CAPACITY - curr_room_occupants))
        curr_room_occupants = curr_room_occupants + random.randint(1, min(10, ROOM_CAPACITY - curr_room_occupants))   
    return cur_room, curr_office_occupants,curr_room_occupants

def room_temp_generator() :
    i = random.randint(0, 3)
    cur_room = ROOM_LIST[i]
    
    return cur_room

# updates the event with a different temperature value
def change_temperature():
    office = office_generator()
    building = building_generator()
    room = room_temp_generator()
    
    temp = temperature_generator()
    return office,building,room,temp
   

# updates the event with a different occupants value
def change_occupants(office_occupants,room_occupants):
    office = office_generator()
    building = building_generator()
    result = room_and_occupants_generator(office_occupants,room_occupants)
    room = result[0] 
    office_occupants = result[1]
    room_occupants = result[2] 
    
    if (room == "Building"):
        occupants = office_occupants
    else:
        occupants = room_occupants
    
    return office,building,room,occupants

def connect_sensor(timer):
    result1 = change_temperature()           
    #print ("SummerCampSTS/{}/{}/{}/CW_{}_sensores/temperatura".format(result1[0],result1[1],result1[2],result1[2]), result1[3])
    client.publish("SummerCampSTS/{}/{}/{}/CW_{}_sensores/temperatura".format(result1[0],result1[1],result1[2],result1[2]), result1[3])
    
    result2 = change_occupants(office_occupants,room_occupants)
    #print ("SummerCampSTS/{}/{}/{}/CW_{}_sensores/presenca".format(result2[0],result2[1],result2[2],result2[2]), result2[3])
    client.publish("SummerCampSTS/{}/{}/{}/CW_{}_sensores/presenca".format(result2[0],result2[1],result2[2],result2[2]), result2[3])
    status_report()
        
def on_connect(client, userdata, flags, rc): 
    print("Conectado ao broker com resultado de conexão: " + str(rc))

   
def status_report():
   
    th = threading.Timer(timer, status_report)
    th.start()
    
    result1 = change_temperature()           
    print ("SummerCampSTS/{}/{}/{}/CW_{}_sensores/temperatura".format(result1[0],result1[1],result1[2],result1[2]), result1[3])
    client.publish("SummerCampSTS/{}/{}/{}/CW_{}_sensores/temperatura".format(result1[0],result1[1],result1[2],result1[2]), result1[3])
    
    result2 = change_occupants(office_occupants,room_occupants)
    print ("SummerCampSTS/{}/{}/{}/CW_{}_sensores/presenca".format(result2[0],result2[1],result2[2],result2[2]), result2[3])
    client.publish("SummerCampSTS/{}/{}/{}/CW_{}_sensores/presenca".format(result2[0],result2[1],result2[2],result2[2]), result2[3])
    
client = mqtt.Client(client_id="cliente_1")
client.on_connect = on_connect  
result = client.connect(broker_adress, broker_port) # Connects MQTT client to a MQTT Broker
print(result)  

connect_sensor(timer)
    
