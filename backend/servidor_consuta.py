from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime, timezone

app = Flask(__name__)

# Configurações de conexão com o MongoDB
client = MongoClient('mongodb://admin:admin@localhost:27017/')
db = client['sensor_data']
collection = db['readings']

# Função para formatar e exibir os dados
def display_data(documents):
    data = []
    for doc in documents:
        data.append({
            'timestamp': doc['timestamp'].isoformat(),
            'sensor_id': doc['sensor_id'],
            'valor': doc['valor']
        })
    return data

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

@app.route('/query', methods=['POST'])
def query_data():
    data = request.json
    sensor_id = data['sensor_id']
    start_datetime = datetime.fromisoformat(data['start_datetime'])
    end_datetime = datetime.fromisoformat(data['end_datetime'])

    # Executando a consulta
    results = query_sensor_data(sensor_id, start_datetime, end_datetime)

    formatted_data = display_data(results)
    return jsonify(formatted_data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
