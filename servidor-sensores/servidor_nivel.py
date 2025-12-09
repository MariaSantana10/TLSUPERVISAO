# mqtt_sensor.py
import numpy as np
import datetime
import paho.mqtt.client as mqtt
import time
import os


metadados = {
    'id_sensor': int(os.getenv('SENSOR_ID', 4)),
    "localizacao": "Tanque 1",
    "tipo": "simulado",
    "unidade": "cm",
    "natureza_sensor": "sonar",
    "variavel": "nivel",
    "versao_servidor": "0.1",
    "versao_firmware": None
}

MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "mqtt-broker")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "sensor/nivel/tanque1") 
PUBLISH_INTERVAL_SECONDS = int(os.getenv("PUBLISH_INTERVAL_SECONDS", 10))


def generate_gaussian_sample(mean, variance):
    return np.random.normal(mean, np.sqrt(variance))


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Conectado ao broker MQTT em {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}")
    else:
        print(f"Falha na conexão ao broker MQTT, código de retorno: {rc}")


def on_publish(client, userdata, mid):
    print(f"Mensagem publicada (mid={mid})")

def on_disconnect(client, userdata, rc):
    print(f"Desconectado do broker MQTT com código: {rc}")
    if rc != 0:
        print("Reconectando...")
        time.sleep(5) 
        client.reconnect()


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    print(f"Tentando conectar ao broker MQTT em {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}...")
    try:
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
    except Exception as e:
        print(f"Não foi possível conectar ao broker: {e}")
        exit(1)

    # Inicia o loop em uma thread separada para que as callbacks funcionem
    client.loop_start()

    print(f"Publicando dados no tópico '{MQTT_TOPIC}' a cada {PUBLISH_INTERVAL_SECONDS} segundos...")
    try:
        while True:
            agora = datetime.datetime.now()
            
            # Gera os dados do sensor
            leitura_sensor = generate_gaussian_sample(70, 45)

            # Prepara o payload JSON para MQTT
            data = {
                'id_sensor': metadados['id_sensor'],
                'variavel': metadados['variavel'],
                'natureza_sensor': metadados['natureza_sensor'],
                'tipo': metadados['tipo'], 
                'unidade': metadados['unidade'],
                'localizacao': metadados['localizacao'],
                'leitura': round(leitura_sensor, 2),
                'timestamp': agora.isoformat(),
                'versao_publicador_mqtt': metadados['versao_servidor'], 
                'versao_firmware': metadados['versao_firmware']
            }
            
            import json
            payload = json.dumps(data)

            client.publish(MQTT_TOPIC, payload, qos=1) 
            print(f"Publicado: {payload} no tópico '{MQTT_TOPIC}'", flush=True)

            
            time.sleep(PUBLISH_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("Publicador interrompido. Desconectando do broker MQTT.")
    finally:
        client.loop_stop()
        client.disconnect()
        print("Desconectado do broker MQTT.")