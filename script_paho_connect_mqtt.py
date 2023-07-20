import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime 


# MQTT Broker Configuration
broker_adress = "test.mosquitto.org" # Broker Adress  
broker_port = 1883 # MQTT port

#client.subscribe("SummerCampSTS/#", qos= 1) # Subscribes to a MQTT topic

# This method is a callback that's called when a new message is received
# Is used to process received messages and to execute actions based on those messages

def on_connect(client, userdata, flags, rc): 
    print("Conectado ao broker com resultado de conexão: " + str(rc))
    client.subscribe("SummerCampSTS/#", qos=0) # Subscribes to a MQTT topic


def on_message(client, userdata, msg):
    print("Nova mensagem recebida no tópico: " + msg.topic)
    print("Conteúdo da mensagem: " + msg.payload.decode())

    try:
        conn = sqlite3.connect("sensors.db", check_same_thread=False)
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        value = msg.payload.decode()
    
        #através da msg topic, ir buscar o id associado aos vários campos
        topic = msg.topic
        str = topic.split("/")
        if len(str) == 6:

            #PLANO:
            #através da msg topic, ir buscar o id associado aos vários campos
            #depois ir à tabela dos sensor_values e inserir uma linha com:
            # id anterior(sensor) | timestamp | value (conteudo da mensagem -> msg.payload.decode())
        
            cursor.execute("""INSERT INTO sensor_values (sensor, timestamp, value)
                            VALUES ((select id from sensors where name = ?), ? , ?)""",
                        (str[4], timestamp , value))

            conn.commit()

    finally:
        cursor.close()
        conn.close()
        

def initialize_db():

    try:
        # Connect to SQLite database - this will create a new database file if it doesn't exist

        conn = sqlite3.connect("sensors.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(""" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='sensors' """)

        #if the count is 1, then table exists

        if cursor.fetchone()[0] == 1:

            print("DB already exists, skipping initialization.")

        else:
            # Create tables
            cursor.execute("""

                CREATE TABLE IF NOT EXISTS "sensors" (
                    "id" INTEGER PRIMARY KEY,
                    "name" TEXT COLLATE NOCASE,
                    "type" TEXT COLLATE NOCASE,
                    "office" TEXT COLLATE NOCASE,
                    "building" TEXT COLLATE NOCASE,
                    "room" TEXT COLLATE NOCASE,
                    "units" TEXT COLLATE NOCASE
                )
            """)

            cursor.execute("""
              CREATE TABLE IF NOT EXISTS "sensor_values" (
                "sensor" INTEGER,
                "timestamp" TEXT,
                "value" REAL
              )
            """)

            conn.commit()
    finally:
        cursor.close()
        conn.close()


initialize_db()

client = mqtt.Client(client_id="cliente_1")

client.on_connect = on_connect

client.on_message = on_message

result = client.connect(broker_adress, broker_port) # Connects MQTT client to a MQTT Broker

print(result)

client.loop_forever()


