import requests
import json

# URL do endpoint (substitua pelo endereço do seu servidor)
url = "http://localhost:5005/get_sensor_data"

# Dados JSON a serem enviados
data = {
    "sensor_id": 1,
    "start_datetime": "2025-05-01T10:00",
    "end_datetime": "2025-05-10T12:00"
}

# Cabeçalhos da requisição
headers = {
    'Content-Type': 'application/json'
}

# Função para testar o endpoint
def test_get_sensor_data():
    try:
        # Envia a requisição POST com os dados JSON
        response = requests.post(url, data=json.dumps(data), headers=headers)

        # Verifica se a requisição foi bem-sucedida (código 200)
        if response.status_code == 200:
            print("Requisição bem-sucedida!")
            print("Resposta do servidor:")
            print(json.dumps(response.json(), indent=4))  # Formata a resposta em JSON
        else:
            print(f"Erro: Código {response.status_code}")
            print("Mensagem de erro:", response.text)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Chama a função para testar o endpoint
test_get_sensor_data()
