# Importa o módulo para manipular arquivos
from pathlib import Path

# Caminho para o arquivo .env
env_file = Path('.env')

# Escreve a variável no arquivo .env
with env_file.open('w') as f:
    f.write('SENSOR_NIVEL=http://10.58.1.50:5003\n')

print("Arquivo .env criado com a variável SENSOR_IP.")
