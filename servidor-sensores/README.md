# Servidor Sensores

Este repositório contém os códigos referentes ao sistema responsável para disponibilizar um servidor com a leitura de um sensor em um endpoint num servidor-web. Foi utilizado Flask para servir dados de diferentes naturezas: temperatura, umidade, nível e presença. Cada servidor está configurado para rodar em um container Docker separado. O projeto inclui instruções detalhadas para configurar e executar o sistema utilizando Docker Compose.

### Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Configuração do Projeto](#configuração-do-projeto)
3. [Estrutura dos Arquivos](#estrutura-dos-arquivos)
4. [Construção e Execução dos Containers](#construção-e-execução-dos-containers)
5. [Endpoints Disponíveis](#endpoints-disponíveis)
6. [Acesso aos Dados do Sensor](#acesso-aos-dados-do-sensor)
7. [Customização dos Sensores](#customização-dos-sensores)
8. [Considerações Finais](#considerações-finais)

### Pré-requisitos

- **Docker**: Certifique-se de ter o Docker instalado. Você pode fazer o download e seguir as instruções de instalação no site oficial do [Docker](https://www.docker.com/get-started).
- **Docker Compose**: Também é necessário ter o Docker Compose instalado. Ele geralmente vem junto com o Docker Desktop.


Deve ser usado um Docker Host no Ubuntu linux para facilitar a configuração de rede dos containers.

### Configuração do Projeto

1. Clone o repositório para sua máquina local; Esse clone deve ser feito cadastrando uma chave ssh.

2. Crie um arquivo `Dockerfile` para cada sensor (temperatura, umidade e nível). Um exemplo genérico de `Dockerfile` para o sensor de nível seria:

   ```dockerfile
   # Dockerfile para sensor de nível
   FROM python:3.9-slim

   WORKDIR /app

   COPY . .

   RUN pip install Flask Flask-Cors numpy

   CMD ["python", "servidor_nivel.py"]
   ```

   Certifique-se de ajustar o `Dockerfile` conforme o nome do arquivo de script correspondente para cada sensor.


Você pode executar um único Dockerfile ou usar o Docker-compose para subir todos os servidores ao mesmo tempo.

### Estrutura dos Arquivos

O repositório contém os seguintes arquivos e diretórios:

- `servidor_temperatura.py`: Script Flask para simulação do sensor de temperatura.
- `servidor_umidade.py`: Script Flask para simulação do sensor de umidade.
- `servidor_nivel.py`: Script Flask para simulação do sensor de nível.
- `Dockerfile`: Arquivo Docker para construir imagens dos sensores.
- `docker-compose.yml`: Arquivo Docker Compose para orquestrar todos os serviços.
- `templates/metadados.html`: Template HTML para exibir os metadados dos sensores.

### Construção e Execução dos Containers

Para construir e iniciar todos os containers de uma só vez, execute:

```bash
docker-compose up --build
```

Este comando cria e inicia os containers para cada sensor. Cada container irá rodar um serviço Flask em uma porta diferente mapeada para a sua máquina host.

No servidor, é necessário usar a opção -d (detached head ou headless) para poder desconcetar do ssh e deixar o container em operação.

### Endpoints Disponíveis

Cada sensor expõe dois endpoints:

1. `/`: Exibe um template HTML com metadados sobre o sensor.
2. `/sensor`: Retorna um JSON com dados simulados do sensor.

**Portas e Endpoints:**

- **Sensor de Temperatura:** `http://localhost:5001/` e `http://localhost:5001/sensor`
- **Sensor de Umidade:** `http://localhost:5002/` e `http://localhost:5002/sensor`
- **Sensor de Nível:** `http://localhost:5003/` e `http://localhost:5003/sensor`


Essas portas foram configuradas no aruqivo docker-compose.yaml

### Acesso aos Dados do Sensor

Você pode acessar os dados dos sensores diretamente através do navegador ou utilizando ferramentas como `curl` ou `Postman`.

Exemplo de comando `curl` para acessar os dados do sensor de nível:

```bash
curl http://localhost:5003/sensor
```

Outro software que pode ser usado é o Insomnia.

### Customização dos Sensores

Você pode facilmente customizar os scripts para alterar o comportamento dos sensores. Por exemplo, para modificar a média e a variância dos dados gerados para o sensor de nível, altere os valores na função `generate_gaussian_sample` no arquivo `servidor_nivel.py`.

### Considerações Finais

Este projeto serve como uma base para sistemas simulados de monitoramento de sensores. Ele pode ser estendido para incluir mais sensores, diferentes modelos de dados, ou integrados a sistemas de armazenamento de dados para análise posterior.

