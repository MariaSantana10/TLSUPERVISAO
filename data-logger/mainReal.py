import os
import json
from datetime import datetime
from pymongo import MongoClient
import paho.mqtt.client as mqtt


client = MongoClient('mongodb://admin:admin@mongo:27017/', serverSelectionTimeoutMS=2000)
db = client['real_data']
print("Conectou ao MongoDB.")


REAL_BROKER = os.getenv("MQTT_BROKER_HOST", "10.57.0.10")
REAL_PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))
REAL_TOPICO = os.getenv("MQTT_TOPIC", "/medidor_nivel/#")
REAL_USER = os.getenv("MQTT_USER", "tht")
REAL_PASS = os.getenv("MQTT_PASS", "senha123")

def save_data(sensor_data, real):
    db[real].insert_one(sensor_data)
    print(f"✔ Dados salvos na coleção '{real}'")

def real_on_connect(client, userdata, flags, rc):
    print("Conectado ao broker REAL!")
    client.subscribe(REAL_TOPICO)
    print(f"Assinado tópico real: {REAL_TOPICO}")


def real_on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())

        registro = {
            "valor": data.get("nivel"),
            "timestamp": datetime.now(),
            "topico": msg.topic,
            "origem": "sensor_real"
        }

        save_data(registro, "real")

    except Exception as e:
        print("Erro ao processar sensor real:", e)


real_client = mqtt.Client()
real_client.username_pw_set(REAL_USER, REAL_PASS)
real_client.on_connect = real_on_connect
real_client.on_message = real_on_message

try:
    real_client.connect(REAL_BROKER, REAL_PORT, 60)
    print(f"Conectando ao broker REAL em {REAL_BROKER}:{REAL_PORT}...")
    real_client.loop_forever()
except Exception as e:
    print("Erro ao conectar ao broker REAL:", e)
