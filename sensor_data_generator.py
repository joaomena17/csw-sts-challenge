from flask import Flask, jsonify, request
import paho.mqtt.client as mqtt
import json
import sys
from time import time
import random
import requests
from pytimedinput import timedInput


#variables
CURRENT_OFFICE = ("Lisboa", "Coimbra", "Tomar", "Viseu", "Porto", "Vila Real")
CURRENT_BUILDING = ("Buiding1", "Building2")
CURRENT_ROOM = ("Room1","Room2", "Room3")
OFFICE_CAPACITY = 300
ROOM_CAPACITY = 10


client = mqtt.Client(client_id="meu_cliente")

#Sensor/publisher subscription
client.subscribe("SummerCampSTS/+/+/+/sensores/temperatura", qos=1) # 1: at least once
client.subscribe("SummerCampSTS/+/+/+/sensores/presenca", qos=1) # 1: at least once

#Sensor unsubscription
#client.unsubscribe("sensores/temperatura") 
#client.unsubscribe("sensores/presenca") 



######## Random values generator ########
def temperature_generator():
    i = random.randint(1, 100)
    if i < 5:
        return random.randint(700, 750)  # simulate high temperature
    elif i > 95:
        return random.randint(751, 800)  # simulate very high temperature
    return random.randint(600, 699)  # standard temperature


# implements a random number of new passengers until the capacity is reached
def occupants_generator(curr_occupants):
    if curr_occupants < OFFICE_CAPACITY:
        return curr_occupants + random.randint(1, min(10, OFFICE_CAPACITY - curr_occupants))
    return curr_occupants

# sets a cooldown interval between 1 and 6 minutes      #???
def interval_generator():
    return random.randint(60, 360)


# updates the event with a different temperature value
def change_temperature():
    temp = temperature_generator()
    client.publish("sensores/temperatura",temp) 
    client.publish("SummerCampSTS/+/+/+/sensores/temperatura",temp) ##? 

# updates the event with a different occupants value
def change_occupants():
    occupants = occupants_generator(occupants)
    client.publish("sensores/presenca", occupants) 
    
########end Random values generator########

def main():
    '''
    # start trip
    s = input("Enter any input to start trip.\n")
    if s is None or s == "stop":
        sys.exit("Canceled start")

    '''
    #train_event = start_event()
    status = True
  
    if status == 0:
        print("Exiting program due to post request error.\n")
        return 1

    # initialize timers
    
    temperature_init = time()
    occupants_init = time()

    occupants_timeout = interval_generator()
    temperature_timeout = interval_generator()

    # initialize speedup factor
    speedup_factor = 1

    # continuously change values based on probabilities and time intervals, and consequent post request
    while status is True:
        # save current time and check all timers
        curr_time = time()
        #tirar depois teste
        print(    
            f"temperature: {int(temperature_init + (temperature_timeout) - curr_time)}\n"
            f"passenger: {int(occupants_init + (occupants_timeout) - curr_time)}\n")

       

        if curr_time > temperature_init + (temperature_timeout):
            change_temperature()
            temperature_init = curr_time
            temperature_timeout = interval_generator()

        if curr_time > occupants_init + (occupants_timeout):
            train_event = change_occupants(train_event)
            occupants_init = curr_time
            occupants_timeout = interval_generator()
   
       # status = publish_event(train_event)
        if status == 0:
            print("Exiting program due to post request error.\n")
            return 1


   # status = publish_event(train_event)
    if status == 0:
        print("Exiting program due to post request error.\n")
        return 1

    # program ran correctly
    return 0


if __name__ == '__main__':
    main()