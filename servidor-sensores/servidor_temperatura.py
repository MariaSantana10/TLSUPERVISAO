import numpy as np
from flask import Flask, jsonify
import paho.mqtt.client as mqtt
import datetime
import random 
import math
import time
import json
import os

metadados = {
    'id_sensor': int(os.getenv('SENSOR_ID', 1)),
    'localizacao': os.getenv('LOCALIZACAO', 'Sala'),
    'tipo': 'Simulado',
    'unidade': 'Graus Celsius',
    'natureza_sensor': 'Infravermelho',
    'variavel': 'Temperatura',
    'versao_servidor': '0.1',
    'versao_firmware': None
}


ruido_estado = 0.0
def temperatura_simulada(hora, minuto=0):
    global ruido_estado
    horas_decimais = hora + minuto / 60.0
    media = 22.5
    amplitude = 5.5
    base = media + amplitude * math.sin((horas_decimais - 10) * math.pi / 12)
    alpha = 0.4
    sigma = 1.4
    ruido_branco = random.gauss(0, sigma)
    ruido_estado = alpha * ruido_estado + (1 - alpha) * ruido_branco
    return base + ruido_estado

MQTT_BROKER_HOST = os.getenv('MQTT_BROKER_HOST', 'mqtt-broker')
MQTT_BROKER_PORT = int(os.getenv('MQTT_BROKER_PORT', 1883))
MQTT_TOPIC = os.getenv(
    'MQTT_TOPIC', 
    f"sensor/temp/sala{metadados['id_sensor']}"
)
PUBLISH_INTERVAL_SECONDS = int(os.getenv('PUBLISH_INTERVAL_SECONDS', 10))

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f'Conectado ao broker em {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}')
    else:
        print(f'Falha na conexão com broker, código de retorno: {rc}')
    
def on_publish(client, userdata, mid):
    print(f'Mensagem publicada (mid={mid})')

def on_disconnect(client, userdata, rc):
    print(f'Desconectado do broker MQTT com código: {rc}')
    if rc != 0:
        print('Reconectando...')
        time.sleep(5)
        client.reconnect()

app = Flask(__name__)


current_data = {}

@app.route('/')
def home():
    return "API de dados do sensor de temperatura"

@app.route('/sensor', methods=['GET'])
def get_dados():
    return jsonify(current_data)

# Função para iniciar o cliente MQTT e publicar os dados
def start_mqtt():
    global current_data
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    print(f'Tentando conectar ao broker MQTT em {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}...')
    try:
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
    except Exception as e:
        print(f'Erro ao conectar: {e}')
        exit(1)

    client.loop_start()

    print(f'Publicando dados do sensor de temperatura no tópico "{MQTT_TOPIC}" a cada {PUBLISH_INTERVAL_SECONDS} segundos.')
    try:
        while True:
            agora = datetime.datetime.now()
            leitura = temperatura_simulada(8, 50)

            data = {
                'id_sensor': metadados['id_sensor'],
                'variavel': metadados['variavel'],
                'natureza_sensor': metadados['natureza_sensor'],
                'tipo': metadados['tipo'], 
                'unidade': metadados['unidade'],
                'localizacao': metadados['localizacao'],
                'leitura': round(leitura, 2),
                'timestamp': agora.isoformat(), 
                'versao_publicador': metadados['versao_servidor'],
                'versao_firmware': metadados['versao_firmware']
            }

            current_data = data

            payload = json.dumps(data)
            client.publish(MQTT_TOPIC, payload, qos=1)
            print(f"Dados publicados: {data}")
            time.sleep(PUBLISH_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print('Execução interrompida')
    finally:
        client.loop_stop()
        client.disconnect()
        print("Desconectado do broker MQTT.")

if __name__ == '__main__':
    from threading import Thread
    mqtt_thread = Thread(target=start_mqtt)
    mqtt_thread.start()

    PORT =int(os.getenv("API_PORT", 5000))
    app.run(host='0.0.0.0', port=PORT, debug=True, use_reloader=False)
