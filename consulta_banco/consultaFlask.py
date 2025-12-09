from pymongo import MongoClient
from datetime import datetime, timezone
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

client = MongoClient('mongodb://admin:admin@mongo:27017/', serverSelectionTimeoutMS=2000)

db = client['sensor_data']

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

def query_sensor_data(collection_name, sensor_id, start_datetime, end_datetime):
    collection = db[collection_name]
    query = {
        'sensor_id': sensor_id,
        'timestamp': {
            '$gte': start_datetime,
            '$lt': end_datetime
        }
    }
    results = collection.find(query)
    return results

@app.route('/')
def aquisicao():
    return 'Servidor de Aquisição'

@app.route('/get_sensor_data', methods=['POST'])
def get_sensor_data():
    try:
        data = request.get_json()
        collection_name = data.get('collection_name')

        if collection_name not in TOPICOS_COLECOES.values():
            return jsonify({'error': 'Coleção inválida'}), 400

        sensor_id = data.get('sensor_id')
        start_datetime = datetime.fromisoformat(data.get('start_datetime')).astimezone(timezone.utc)
        end_datetime = datetime.fromisoformat(data.get('end_datetime')).astimezone(timezone.utc)

        results = query_sensor_data(collection_name, sensor_id, start_datetime, end_datetime)

        response_data = [{'timestamp': doc['timestamp'].isoformat(), 'sensor_id': doc['sensor_id'], 'valor': doc['valor']} for doc in results]

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
