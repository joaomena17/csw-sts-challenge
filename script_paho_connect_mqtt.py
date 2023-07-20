import paho.mqtt.client as mqtt

client = mqtt.Client(client_id="cliente_1")

# MQTT Broker Configuration
broker_adress = "test.mosquitto.org" # Broker Adress  
broker_port = 1883 # MQTT port

client.connect(broker_adress, broker_port) # Connects MQTT client to a MQTT Broker

#client.subscribe("SummerCampSTS/#", qos= 1) # Subscribes to a MQTT topic

# This method is a callback that's called when a new message is received
# Is used to process received messages and to execute actions based on those messages
def on_connect(client, userdata, flags, rc): 
    print("Conectado ao broker com resultado de conexão: " + str(rc))
    client.subscribe("SummerCampSTS/#", qos= 1) # Subscribes to a MQTT topic

client.on_connect = on_connect

def on_message(client, userdata, msg):
    print("Nova mensagem recebida no tópico: " + msg.topic)
    print("Conteúdo da mensagem: " + msg.payload.decode())
    
    #insert database
    #cria cursor

client.on_message = on_message