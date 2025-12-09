from pymongo import MongoClient
from datetime import datetime, timezone

# Configurações de conexão com o MongoDB
client = MongoClient('mongodb://admin:admin@localhost:27017/')
db = client['sensor_data']
collection = db['readings']

# Função para formatar e exibir os dados
def display_data(documents):
    for doc in documents:
        print(f"Data/Hora: {doc['timestamp']}, Sensor ID: {doc['sensor_id']}, Valor: {doc['valor']}")

# Função para consultar dados por data/hora e sensor ID
def query_sensor_data(sensor_id, start_datetime, end_datetime):
    query = {
        'sensor_id': sensor_id,
        'timestamp': {
            '$gte': start_datetime,
            '$lt': end_datetime
        }
    }
    results = collection.find(query)
    return results

start_datetime = datetime(2024, 5, 3, 11, 0) 
end_datetime = datetime(2024, 5, 3, 15, 0) 

start_datetime = start_datetime.astimezone(timezone.utc)
end_datetime = end_datetime.astimezone(timezone.utc)

# Executando a consulta
results = query_sensor_data(1, start_datetime, end_datetime)

# Exibindo os dados
display_data(results)
