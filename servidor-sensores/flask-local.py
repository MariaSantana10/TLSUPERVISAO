import serial
from flask import Flask, jsonify
import threading
import time
import datetime
from flask_cors import CORS
import paho.mqtt.client as mqtt
import json
import os


metadados = {
    "id_sensor": int(os.getenv('SENSOR_ID', 5)),
    "localizacao": os.getenv('LOCALIZACAO', 'Local'),
    "tipo": "real",
    "unidade": "cm",
    "natureza_sensor": "sonar",
    "variavel": "nivel",
    "versao_servidor": "0.2",
    "versao_firmware": "0.1"
}

porta_serial = os.getenv('PORTA_SERIAL', '/dev/ttyUSB0')
baud_rate = int(os.getenv('BAUD_RATE', 9600))
ultimo_dado = None

def ler_dados():
    global ultimo_dado
    try:
        with serial.Serial(porta_serial, baud_rate, timeout=1) as ser:
            print(f"Lendo dados da porta {porta_serial} a {baud_rate} bps...")
            while True:
                if ser.in_waiting > 0:
                    linha = ser.readline().decode('utf-8').strip()
                    try:
                        valor = float(linha)
                        if valor <= 100: 
                            ultimo_dado = valor
                            print(f"Recebido: {ultimo_dado}")
                    except ValueError:
                        print(f"Dado inválido recebido: {linha}")
    except serial.SerialException as e:
        print(f"Erro ao acessar a porta serial: {e}")
    except KeyboardInterrupt:
        print("\nLeitura encerrada pelo usuário.")

# Inicia a leitura serial em thread separada
threading.Thread(target=ler_dados, daemon=True).start()

MQTT_BROKER_HOST = os.getenv('MQTT_BROKER_HOST','mqtt-broker')
MQTT_BROKER_PORT = int(os.getenv('MQTT_BROKER_PORT',1883))
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'sensor/nivel/local')
PUBLISH_INTERVAL_SECONDS = int(os.getenv('PUBLISH_INTERVAL_SECONDS', 1))

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f'Conectado ao broker MQTT em: {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}')
    else:
        print(f'Erro ao conectar ao broker, código de retorno: {rc}')

def on_publish(client, userdata, mid):
    print(f'Mensagem publicada (mid={mid})')

def on_disconnect(client, userdata, rc):
    print(f'Desconectado do broker MQTT com código: {rc}')
    if rc != 0:
        print('Reconectando...')
        time.sleep(5)
        client.reconnect()

current_data = {}

app = Flask(__name__)
CORS(app) 

@app.route('/')
def get_dados():
    return jsonify(current_data)

def start_mqtt():
    global current_data
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    try:
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
    except Exception as e:
        print(f'Erro ao conectar: {e}')
        exit(1)

    client.loop_start()

    try:
        while True:
            agora = datetime.datetime.now()

            if ultimo_dado is not None: 
                leitura = str(ultimo_dado)

                data = {
                    'id_sensor': metadados['id_sensor'],
                    'variavel': metadados['variavel'],
                    'natureza_sensor': metadados['natureza_sensor'],
                    'tipo': metadados['tipo'], 
                    'unidade': metadados['unidade'],
                    'localizacao': metadados['localizacao'],
                    'leitura': leitura,
                    'timestamp': agora.isoformat(), 
                    'versao_servidor_flask': metadados['versao_servidor'],
                    'versao_firmware': metadados['versao_firmware']
                }

                current_data = data
                payload = json.dumps(data)
                client.publish(MQTT_TOPIC, payload, qos=1)
                print(f"Dados publicados: {data}")
            else:
                print("Nenhum dado disponível para publicar ainda.")

            time.sleep(PUBLISH_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print('Execução interrompida')
    finally:
        client.loop_stop()
        client.disconnect()
        print("Desconectado do broker MQTT.")

if __name__ == '__main__':
    mqtt_thread = threading.Thread(target=start_mqtt)
    mqtt_thread.start()

    PORT = int(os.getenv("API_PORT", 5000))
    app.run(host='0.0.0.0', port=PORT, debug=True, use_reloader=False)
