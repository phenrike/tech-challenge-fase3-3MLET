# 🌎 API de Sensores de Qualidade do Ar (OpenAQ)

## 📌 Sobre o Projeto
Esta API fornece dados sobre sensores de **qualidade do ar no Chile**, focando no poluente **PM2.5**. A API consome informações da **OpenAQ API** e permite consultar **sensores disponíveis** e suas **medições dentro de um intervalo de datas**.

Utilizamos também a **WeatherAPI** para trazer **dados do clima** para uma cidade em um determinado período. A API também servirá de ponte para buscarmos **previsões futuras**, funcionalidade que permitirá **prever a qualidade do ar** em um período, numa cidade, com uma **previsão de tempo específica**.

Além disso, a API possui um **endpoint de carga de dados**, que extrai as informações de **qualidade do ar e do tempo**, armazenando-as localmente em um **banco de dados**. Isso permite a posterior **análise** e a criação de **modelos de Machine Learning**.

## 🚀 Funcionalidades
- **Listar sensores de PM2.5 no Chile** (`GET /sensors/pm25/chile`)
- **Obter medições de todos os sensores** (`GET /sensor-data?datetime_from=YYYY-MM-DD&datetime_to=YYYY-MM-DD`)
- **Obter histórico do clima** (`GET /weather-history?city=NOME_DA_CIDADE&date=YYYY-MM-DD`)
- **Obter previsão do clima** (`GET /weather-future?city=NOME_DA_CIDADE&date=YYYY-MM-DD`)
- **Processar e salvar dados** (`POST /orchestrator`)
- **Acompanhar progresso** (`GET /orchestrator/progress`)

---

## 🛠 Tecnologias Utilizadas
- **Python 3**
- **Flask** (para criação da API)
- **Requests** (para consumir a API OpenAQ)
- **Clean Architecture** (separação em camadas)
- **PostgreSQL** (banco de dados)
- **Docker** (containerização)
- **Weather API** (dados climáticos)

---

## 📂 Estrutura do Projeto
```
app/
├── domain/                 # Modelos de dados
│   ├── models.py           # Classes Sensor e Measurement
│
├── interfaces/             # Interfaces para repositórios
│   ├── sensor_repository.py
│   ├── measurement_repository.py
│
├── infra/                 # Implementação de APIs externas
│   ├── openaq_api.py      # Consumo da API OpenAQ
│   ├── weather_api.py     # Consumo da API de Clima
│   ├── database.py        # Conexão com PostgreSQL
│
├── application/           # Regras de negócio
│   ├── services.py        # Serviços para sensores e medições
│   └── progress_manager.py # Gerenciamento de progresso
│
├── presentation/          # Camada de apresentação (controllers)
│   ├── controllers.py     # Rotas da API
│
├── main.py               # Inicialização do Flask
└── README.md
```

---

## 🏗 Como Configurar e Rodar a API

### 1️⃣ Clonar o repositório
```sh
git clone https://github.com/phenrike/tech-challenge-fase3-3MLET.git
cd tech-challenge-fase3-3MLET
```

### 2️⃣ Usando Docker (Recomendado)
```sh
docker-compose up -d
```
A API estará rodando em **http://localhost:8080** 🚀

### 3️⃣ Ou usando ambiente virtual
```sh
python3 -m venv venv
source venv/bin/activate  # (Linux/Mac)
venv\Scripts\activate     # (Windows)
pip install -r requirements.txt
python app/main.py
```

### 4️⃣ Definir chave de API do OpenAQ
Crie um arquivo **.env** na raiz do projeto e adicione:
```sh
X_API_KEY=sua_api_key_aqui
```

---

## 🔥 Como Usar os Endpoints

### 📍 **Listar sensores de PM2.5 no Chile**
```sh
GET http://localhost:8080/sensors/pm25/chile
```
📌 **Resposta:**
```json
{
  "pm25_sensors": [1044, 2045, 3067]
}
```

### 📍 **Obter medições de todos os sensores**
```sh
GET http://localhost:8080/sensor-data?datetime_from=2024-01-01T00:00:00Z&datetime_to=2024-01-31T00:00:00Z
```
📌 **Resposta:**
```json
[
  {
    "sensor_id": 1044,
    "value": 29.1,
    "datetimeFrom_local": "2024-01-01T00:00:00-03:00",
    "datetimeTo_local": "2024-01-02T00:00:00-03:00",
    "city": "Santiago"
  }
]
```

### 📍 **Obter histórico do clima**
```sh
GET http://localhost:8080/weather-history?city=Santiago&date=2024-03-26
```

### 📍 **Obter previsão do clima**
```sh
GET http://localhost:8080/weather-future?city=Santiago&date=2024-03-26
```

### 📍 **Processar e salvar dados**
```sh
POST http://localhost:8080/orchestrator
```

### 📍 **Acompanhar progresso**
```sh
GET http://localhost:8080/orchestrator/progress
```