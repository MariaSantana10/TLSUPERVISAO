# 📦 Projeto Super - Sistema de Supervisão do campus IFRN/CM

Este repositório organiza e gerencia um sistema distribuído composto por múltiplos serviços:
- **Banco de dados** (MongoDB)
- **Sensores virtuais** (temperatura, umidade, nível e movimento)
- **Data Logger** (coleta e armazena dados no banco)
- **Orquestração completa** via Docker Compose

Cada componente do sistema é versionado em seu próprio repositório Git, e todos são integrados aqui utilizando **Git Submodules**.

---

## 📂 Estrutura do Projeto

```
super/
├── backend/              # Submódulo - Backend (inicialmente responsável apenas pelo MongoDB)
├── data-logger/          # Submódulo - Coletor de dados dos sensores
├── servidor-sensores/    # Submódulo - Servidores Flask dos sensores virtuais
├── docker-compose.yml    # Orquestração principal dos serviços
└── start.sh              # Script para iniciar todo o sistema
```

---

## 🚀 Instruções para Clonar e Rodar o Projeto

> ⚡ Importante: todo o processo utiliza **SSH** para acessar os repositórios.

### 1. Clonar o repositório principal **com os submódulos**

```bash
git clone --recurse-submodules git@github.com:IFRN-auto-cm/super.git
```

Caso já tenha clonado sem `--recurse-submodules`, inicialize os submódulos manualmente:

```bash
cd super
git submodule update --init --recursive
```

---

### 2. (Opcional) Atualizar todos os submódulos para a última versão

Caso queira sincronizar todos os submódulos para a última versão dos seus branches remotos:

```bash
git submodule update --remote
```

---

### 3. Subir todos os containers

Dentro da pasta `super/`, execute:

```bash
docker compose up --build
```

Ou para rodar em background:

```bash
docker compose up -d --build
```

Isso irá:
- Subir o MongoDB
- Subir todos os sensores
- Subir o Data Logger

Todos os containers estarão na mesma rede Docker (`super-network`).

---

## 📜 Dependências

- [Docker](https://www.docker.com/)
- [Docker Compose v2](https://docs.docker.com/compose/)

---

## 🛠️ Manutenção dos Submódulos

| Ação                        | Comando                                  |
|------------------------------|-----------------------------------------|
| Clonar já com submódulos     | `git clone --recurse-submodules <url>`   |
| Inicializar submódulos       | `git submodule update --init --recursive` |
| Atualizar para último commit | `git submodule update --remote`          |

---

## 📌 Observações

- Toda comunicação entre os containers é feita usando o **nome dos serviços** (e não `localhost`), graças à rede Docker.
- Para acessar o MongoDB, sensores ou o data logger de fora do Docker, utilize as **portas expostas** no `docker-compose.yml`.
- As autenticações entre Git e repositórios são realizadas **exclusivamente via SSH**.

---

## 📣 Contato

Projeto desenvolvido e mantido por [IFRN-auto-cm](https://github.com/IFRN-auto-cm).