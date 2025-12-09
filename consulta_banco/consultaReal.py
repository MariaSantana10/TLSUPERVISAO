from pymongo import MongoClient
from datetime import datetime, timezone
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb://admin:admin@mongo:27017/', serverSelectionTimeoutMS=2000)
db = client['real_data']

TOPICOS_COLECOES = {
    "/medidor_nivel/#": "real"
}

def query_real_data(collection_name, start_datetime, end_datetime):
    collection = db[collection_name]
    query = {
        'timestamp': {
            '$gte': start_datetime,
            '$lt': end_datetime
        }
    }
    return collection.find(query)

@app.route("/")
def home():
    return "Servidor de Consulta de Dados Reais"

@app.route("/get_real_data", methods=["POST"])
def get_real_data():
    try:
        data = request.get_json()

        collection_name = data.get("collection_name")
        if collection_name not in TOPICOS_COLECOES.values():
            return jsonify({"error": "Coleção inválida"}), 400

        start_datetime = datetime.fromisoformat(data.get("start_datetime")).astimezone(timezone.utc)
        end_datetime = datetime.fromisoformat(data.get("end_datetime")).astimezone(timezone.utc)

        results = query_real_data(collection_name, start_datetime, end_datetime)

        response = []
        for doc in results:
            response.append({
                "timestamp": doc["timestamp"].isoformat(),
                "valor": doc["valor"],
                "topico": doc.get("topico", "real"),
                "origem": doc.get("origem", "sensor_real")
            })

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)