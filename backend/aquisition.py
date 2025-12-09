import time
from pymongo import MongoClient
import requests
from datetime import datetime

# Configuração do cliente MongoDB
client = MongoClient('mongodb://admin:admin@localhost:27017/')
db = client['sensor_data']  # Banco de dados
collection = db['readings']  # Coleção

print( "conectou")

# Função para obter dados do sensor
def get_sensor_data():
    print("dnetro da funcao")
    response = requests.get('http://127.0.0.1:5000/sensor')
    data = response.json()
    print("Data:", data)    
    return {
        'sensor_id': data['id_sensor'],
        'tipo': data['natureza_sensor'],
        'valor': data['leitura'],
        'timestamp': datetime.strptime(data['timestamp'], "%Y-%m-%d %H:%M:%S.%f"),
        'localizacao': data['localizacao'],
        'metadados': {
            'tipo': data['tipo'],
            'unidade': data['unidade'],
            'variavel': data['variavel'],
            'versao_firmware': data['versao_firmware'],
            'versao_servidor_flask': data['versao_servidor_flask']
        }
    }

# Função para salvar dados no MongoDB
def save_data(data):
    collection.insert_one(data)

# Loop principal para obter e salvar dados periodicamente
try:
    while True:        
        sensor_data = get_sensor_data()
        print("Dados do sensor:", sensor_data)
        save_data(sensor_data)
        print("Dados salvos no Banco de dados")
        time.sleep(60)  # Espera por 1 segundo antes de repetir
except KeyboardInterrupt:
    print("Programa interrompido manualmente.")
