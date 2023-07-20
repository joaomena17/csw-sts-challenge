from flask import Flask, jsonify, request
import paho.mqtt.client as mqtt
import json
import sys
#import numpy as np
from time import time
import random
#import requests
#from pytimedinput import timedInput


#variables
OFFICE_LIST = ["Lisboa", "Coimbra", "Tomar", "Viseu", "Porto", "Vila Real"]
BUILDING_LIST = ["Buiding1", "Building2"]
ROOM_LIST = ["Room1","Room2", "Room3", "Building"]

OFFICE_MAX_CAPACITY = 300
ROOM_CAPACITY = 20
office_occupants=0
room_occupants=0
temperature_init = time()
occupants_init = time()


# sets a cooldown interval between 1 and 6 minutes      #???
def interval_generator():
    return random.randint(60, 360)

occupants_timeout = interval_generator()
temperature_timeout = interval_generator()

temperature_init = time()
occupants_init = time() 
#status = True
curr_time = time()

# MQTT Broker Configuration
broker_adress = "test.mosquitto.org" # Broker Adress  
broker_port = 1883 # MQTT port


client = mqtt.Client(client_id="cliente_1")

result = client.connect(broker_adress, broker_port) # Connects MQTT client to a MQTT Broker

print(result)

#Sensor/publisher subscription
client.subscribe("sensores/temperatura", qos=1) # 1: at least once
client.subscribe("sensores/presenca", qos=1) # 1: at least once

#Sensor unsubscription
#client.unsubscribe("sensores/temperatura") 
#client.unsubscribe("sensores/presenca") 

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
    #print(cur_office)
    return cur_office

def building_generator():
    i = random.randint(0,1)
    cur_building = BUILDING_LIST[i]
    #print(cur_building)
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
    
    print ("SummerCampSTS/{}/{}/{}/sensores/temperatura".format(office,building,room), temp)
    client.publish("SummerCampSTS/{}/{}/{}/sensores/temperatura".format(office,building,room), temp)
    
    #client.publish("sensores/temperatura",temp) 
   

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
   
    print ("SummerCampSTS/{}/{}/{}/sensores/presenca".format(office,building,room), occupants)
    #client.publish("sensores/presenca", office_occupants) 
    client.publish("SummerCampSTS/{}/{}/{}/sensores/temperatura".format(office,building,room), occupants)

def publisher():   
    if curr_time > temperature_init + (temperature_timeout):
        change_temperature()
        temperature_init = curr_time
        temperature_timeout = interval_generator()

    if curr_time > occupants_init + (occupants_timeout):
        change_occupants(office_occupants,room_occupants)
        occupants_init = curr_time
        occupants_timeout = interval_generator()
        
client.publisher = publisher
       
client.loop_forever()   
    
########end Random values generator########


"""
def main():
    '''
    # start trip
    s = input("Enter any input to start trip.\n")
    if s is None or s == "stop":
        sys.exit("Canceled start")

    '''
    #train_event = start_event()
   # status = True
    
    if status == 0:
        print("Exiting program due to post request error.\n")
        return 1

    office_occupants=0
    room_occupants=0
    # initialize timers
    #change_occupants(office_occupants,room_occupants)
    #change_temperature()
    temperature_init = time()
    occupants_init = time()

    occupants_timeout = interval_generator()
    temperature_timeout = interval_generator()

    # initialize speedup factor
    #speedup_factor = 1

    # continuously change values based on probabilities and time intervals, and consequent post request
    while status is True:
        # save current time and check all timers
        curr_time = time()
               
        """
       
        #print(    
        #    f"temperature: {int(temperature_init + (temperature_timeout) - curr_time)}\n"
        #    f"passenger: {int(occupants_init + (occupants_timeout) - curr_time)}\n")     
        #"""
        #if curr_time > temperature_init + (temperature_timeout):
        #    change_temperature()
        #    temperature_init = curr_time
        #    temperature_timeout = interval_generator()
#
        #if curr_time > occupants_init + (occupants_timeout):
        #    change_occupants(office_occupants,room_occupants)
        #    occupants_init = curr_time
        #    occupants_timeout = interval_generator()
       
       # status = publish_event(train_event)
        if status == 0:
            print("Exiting program due to post request error.\n")
            return 1
        """

   # status = publish_event(train_event)
    """
    if status == 0:
        print("Exiting program due to post request error.\n")
        return 1
    """
    # program ran correctly
    #print()
    ''' return 0


if __name__ == '__main__':
    main()
    """
    '''
   