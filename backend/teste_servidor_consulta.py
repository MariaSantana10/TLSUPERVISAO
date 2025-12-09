import requests
import json

url = 'http://localhost:5001/query'

data = {
    'sensor_id': 1,
    'start_datetime': '2024-05-08T07:00:00',
    'end_datetime': '2024-05-08T08:15:00'
}

response = requests.post(url, json=data)

# Verificar se a requisição foi bem sucedida
if response.status_code == 200:
    # Exibir os dados recebidos
    formatted_data = json.loads(response.text)
    contador = 0
    for entry in formatted_data:
        contador += 1
        print(f"Data/Hora: {entry['timestamp']}, Sensor ID: {entry['sensor_id']}, Valor: {entry['valor']}")
    print(f"Total de registros: {contador}")
else:
    print("Falha ao obter os dados do microserviço.")
