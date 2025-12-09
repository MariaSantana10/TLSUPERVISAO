import os
import json
import time
import datetime
from threading import Thread
from flask import Flask, jsonify
import paho.mqtt.client as mqtt
from flask_cors import CORS 

MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "10.57.0.10")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "/medidor_nivel/#")

MQTT_USER = os.getenv("MQTT_USER", "tht")
MQTT_PASS = os.getenv("MQTT_PASS", "senha123")

current_data = {}


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Conectado ao broker MQTT em {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}")
        client.subscribe(MQTT_TOPIC)
        print(f"Inscrito no tópico: {MQTT_TOPIC}")
    else:
        print(f"Falha na conexão ao broker MQTT. Código: {rc}")

def on_message(client, userdata, msg):
    global current_data
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)

        current_data = data 

        print(f"[MSG] {msg.topic} → {payload}")

    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

def on_disconnect(client, userdata, rc):
    print(f"Desconectado do MQTT. Código: {rc}")
    if rc != 0:
        print("Tentando reconectar...")
        time.sleep(3)
        try:
            client.reconnect()
        except:
            pass

def start_mqtt():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASS)

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    print(f"🔌 Conectando ao broker MQTT {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}...")
    try:
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
    except Exception as e:
        print(f"Erro ao conectar ao broker: {e}")
        return

    client.loop_forever()

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "API de consumo do medidor de nível"

@app.route("/dados", methods=["GET"])
def dados():
    if current_data:
        return jsonify(current_data)
    return jsonify({"status": "Aguardando dados do MQTT..."})

if __name__ == "__main__":
    mqtt_thread = Thread(target=start_mqtt)
    mqtt_thread.start()

    PORT = int(os.getenv("API_PORT", 5001))
    app.run(host="0.0.0.0", port=PORT, debug=True, use_reloader=False)
