import os
import json
from datetime import datetime
from pymongo import MongoClient
import paho.mqtt.client as mqtt


client = MongoClient('mongodb://admin:admin@mongo:27017/', serverSelectionTimeoutMS=2000)

db = client['sensor_data']
print("Conectou ao MongoDB.")


TOPICOS_COLECOES = {
    'sensor/temp/sala1': 'temp1',
    'sensor/lampada/sala1': 'luz1',
    'sensor/presenca/sala1': 'ar1',
    'sensor/nivel/tanque1': 'nivel1',
    'sensor/nivel/local': 'local',
    'sensor/temp/sala2': 'temp2',
    'sensor/lampada/sala2': 'luz2',
    'sensor/presenca/sala2': 'ar2',
}

MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "mqtt-broker")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))

print(f'Conectando ao broker MQTT em {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}...')


def save_data(sensor_data, temp1):
    collection = db[temp1]
    collection.insert_one(sensor_data)
    print(f'Dados salvos na coleção "{temp1}"')


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT com sucesso!")
        for topico in TOPICOS_COLECOES.keys():
            client.subscribe(topico)
            print(f'Assinado o tópico: {topico}')
    else:
        print(f"Falha ao conectar ao broker MQTT. Código de retorno: {rc}")

def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode('utf-8')
        sensor_data = json.loads(payload_str)

        print(f'\nMensagem recebida do tópico: {msg.topic}')
        print(f'Dados brutos: {sensor_data}')

        if 'timestamp' in sensor_data:
            sensor_data['timestamp'] = datetime.fromisoformat(sensor_data['timestamp'])

        dado_formatado = {
            'sensor_id': sensor_data['id_sensor'],
            'natureza_sensor': sensor_data['natureza_sensor'],
            'valor': sensor_data['leitura'],
            'timestamp': sensor_data['timestamp'],
            'localizacao': sensor_data['localizacao'],
            'metadados': {
                'tipo': sensor_data['tipo'],
                'unidade': sensor_data['unidade'],
                'variavel': sensor_data['variavel'],
                'versao_firmware': sensor_data.get('versao_firmware'),
                'versao_servidor': sensor_data.get('versao_servidor')
            }
        }


        colecao = TOPICOS_COLECOES.get(msg.topic)
        if colecao:
            save_data(dado_formatado, colecao)
        else:
            print(f"Tópico desconhecido: {msg.topic}. Mensagem ignorada.")

    except Exception as e:
        print(f"Erro ao processar mensagem MQTT: {e}")
        print(f"Payload original: {msg.payload.decode('utf-8')}")


client_mqtt = mqtt.Client()
client_mqtt.on_connect = on_connect
client_mqtt.on_message = on_message


try:
    client_mqtt.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
    client_mqtt.loop_forever()
except Exception as e:
    print(f"Erro ao conectar ao broker: {e}")