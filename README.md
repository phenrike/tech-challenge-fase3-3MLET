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
|
├── docker/                # Conteúdo do Docker
│   ├── postgres/          # Conteúdo do banco de dados
│   |   └── Dockerfile     # Arquivo Docker do banco de dados
|   |   └── init.sql       # Configuração do banco de dados
|   ├── docker-compose.yml # Configuração do Docker
|   ├── Dockerfile         # Arquivo Docker
|
├── best_rf_model.pk       # Arquivo com o modelo treinado
├── main.py                # Inicialização do Flask
├── notebook.ipynb         # Notebook para tratamento de dados e treinamento do modelo de ML
├── predict.py             # Função para prever índice de poluição
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
cd docker
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
  "pm25_sensors": [
    {
      "city": "Santiago",
      "id": 1044
    },
    {
      "city": "Valparaíso",
      "id": 67
    },
    {
      "city": "Puerto Montt",
      "id": 491
    },
    {
      "city": "Viña del Mar",
      "id": 1762
    },
    {
      "city": "Puerto Montt",
      "id": 21638
    },
    {
      "city": "Puerto Varas",
      "id": 28507
    }
  ]
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
    "city": "Santiago",
    "datetimeFrom_local": "2023-12-31T00:00:00-03:00",
    "datetimeTo_local": "2024-01-01T00:00:00-03:00",
    "sensor_id": 1044,
    "value": 19.3
  }
]
```

### 📍 **Obter histórico do clima**
```sh
GET http://localhost:8080/weather-history?city=Santiago&date=2024-03-26
```

📌 **Resposta:**
```json
{
  "data": [
    {
      "avg_humidity": 40,
      "avg_temp_c": 20.3,
      "avg_vis_km": 10.0,
      "city": "Santiago",
      "date": "2024-03-28",
      "max_wind_kph": 13.7,
      "pressure_mb": 1014.75,
      "total_precip_mm": 0.0
    }
  ]
}
```

### 📍 **Obter previsão do clima**
```sh
GET http://localhost:8080/weather-future?city=Santiago&date=2025-04-05
```

📌 **Resposta:**
```json
{
  "data": {
    "avg_humidity": 32,
    "avg_temp_c": 18.5,
    "avg_vis_km": 10.0,
    "city": "Santiago",
    "date": "2025-04-05",
    "max_wind_kph": 7.9,
    "pressure_mb": 1014.2083333333334,
    "total_precip_mm": 0.0
  }
}
```

### 📍 **Processar e salvar dados**
```sh
POST http://localhost:8080/orchestrator
```

### 📍 **Acompanhar progresso**
```sh
GET http://localhost:8080/orchestrator/progress
```

📌 **Resposta:**
```json
{
    "elapsed_time_seconds": 437.92,
    "errors": [],
    "measurements": {
        "processed_cities": 5,
        "progress_percentage": 100.0,
        "total_inserted": 1947
    },
    "weather": {
        "cities": [
            {
                "city": "Valparaíso",
                "total_inserted": 365
            },
            {
                "city": "Puerto Montt",
                "total_inserted": 365
            },
            {
                "city": "Viña del Mar",
                "total_inserted": 365
            },
            {
                "city": "Puerto Varas",
                "total_inserted": 365
            },
            {
                "city": "Santiago",
                "total_inserted": 365
            }
        ],
        "progress_percentage": 100.0
    }
}
```
### 📍 **Após treinar e salvar o modelo**
```sh
cd tech-challenge-fase3-3MLET/app
python predict.py
```

### 📍 **Endpoint de predição**
```sh
GET http://localhost:5000/predict-pm25?city=Santiago&date=2025-04-05
```

📌 **Resposta:**
```sh
{
   "city": "Santiago",
   "date": "2025-04-12",
   "predicted_pm25": 43,
   "weather_data": {
      "humidity": 39,
      "precipitation": 0.0,
      "pressure": 1014,
      "temperature": 21.3,
      "visibility": 10.0,
      "wind_speed": 13.0
  }
}
```

Storytelling

---

#### **Introdução**
Imagine que você está planejando uma viagem para uma das cidades do Chile, como Santiago ou Puerto Montt, e deseja saber como estará a qualidade do ar nos próximos dias. A poluição do ar, especialmente o índice de partículas PM2.5, pode impactar diretamente a saúde, especialmente para pessoas com problemas respiratórios. Pensando nisso, desenvolvemos uma solução que combina ciência de dados, aprendizado de máquina e tecnologia para prever o índice de poluição PM2.5 com até 14 dias de antecedência.

---

#### **Objetivo**
O objetivo deste projeto é criar uma aplicação que permita aos usuários consultar a previsão do índice de poluição PM2.5 em tempo real para diferentes cidades do Chile. A aplicação utiliza dados climáticos históricos e futuros para treinar um modelo de aprendizado de máquina que realiza previsões precisas. Além disso, os dados são armazenados em um banco de dados para facilitar consultas e análises futuras.

---

#### **Etapas do Projeto**

1. **Coleta de Dados**
   - Utilizamos APIs públicas, como a WeatherAPI e a OpenAQ, para coletar dados climáticos e de qualidade do ar em tempo real.
   - Os dados incluem informações como temperatura média, umidade, velocidade do vento, visibilidade, pressão atmosférica, precipitação e o índice de PM2.5.

2. **Armazenamento de Dados**
   - Os dados coletados são armazenados em um banco de dados PostgreSQL, estruturado para suportar consultas eficientes.
   - Criamos tabelas específicas para armazenar o histórico climático (`tbl_weather_history`) e as medições de sensores de poluição (`tbl_measurements`).

3. **Análise Exploratória**
   - Exploramos os dados para entender a distribuição das variáveis climáticas e sua relação com o índice de PM2.5.
   - Identificamos padrões e outliers nos dados para garantir a qualidade do conjunto de treinamento.

4. **Pré-Processamento**
   - Realizamos o tratamento de valores ausentes e duplicados.
   - Codificamos variáveis categóricas, como o nome das cidades, e removemos colunas irrelevantes, como `ano`, `mes` e `dia`.
   - Padronizamos os dados para garantir que todas as variáveis estejam na mesma escala.

5. **Treinamento do Modelo**
   - Utilizamos um modelo de aprendizado de máquina baseado em Random Forest Regressor, que foi escolhido por sua robustez e capacidade de lidar com dados não lineares.
   - O modelo foi treinado com as seguintes features climáticas:
     - Umidade média (`qt_avg_humidity`)
     - Temperatura média (`qt_avg_temp_c`)
     - Visibilidade média (`qt_avg_vis_km`)
     - Velocidade máxima do vento (`qt_max_wind_kph`)
     - Precipitação total (`qt_total_precip_mm`)
     - Pressão atmosférica média (`qt_pressure_mb`)
   - Avaliamos o modelo utilizando métricas como RMSE (Root Mean Squared Error) e MAPE (Mean Absolute Percentage Error).

6. **Desenvolvimento da API**
   - Criamos uma API RESTful utilizando Flask para permitir que os usuários consultem a previsão do índice PM2.5.
   - A API coleta dados climáticos em tempo real, processa-os e utiliza o modelo treinado para realizar a previsão.
   - Endpoints principais:
     - `/predict-pm25`: Retorna a previsão do índice PM2.5 para uma cidade e data específicas.
     - `/weather-history`: Retorna o histórico climático de uma cidade.
     - `/weather-future`: Retorna a previsão climática futura de uma cidade.

7. **Armazenamento e Orquestração**
   - Implementamos um serviço de orquestração que coleta dados automaticamente, processa-os e os armazena no banco de dados.
   - Isso garante que o modelo esteja sempre atualizado com os dados mais recentes.

8. **Visualização**
   - Criamos gráficos e visualizações para contar a história dos dados e do modelo.
   - Exemplos:
     - Distribuição da temperatura média e do índice PM2.5.
     - Comparação entre os valores reais e previstos do índice PM2.5.
   - As visualizações podem ser integradas a um dashboard ou apresentadas em um vídeo explicativo.

---

#### **Demonstração da Aplicação**
1. **Consulta de Previsão**
   - O usuário acessa a API ou o dashboard e insere a cidade e a data desejadas (até 14 dias no futuro).
   - A aplicação retorna a previsão do índice PM2.5, juntamente com os dados climáticos utilizados na previsão.

2. **Exemplo de Uso**
   - **Requisição**: `GET /predict-pm25?city=Santiago&date=2025-04-05`
   - **Resposta**:
     ```json
     {
         "city": "Santiago",
         "date": "2025-04-05",
         "predicted_pm25": 35,
         "weather_data": {
             "temperature": 25.0,
             "humidity": 60.0,
             "wind_speed": 5.2,
             "visibility": 10.0,
             "pressure": 1013.0,
             "precipitation": 0.1
         }
     }
     ```

3. **Benefícios**
   - Permite que os usuários planejem suas viagens com base na qualidade do ar.
   - Ajuda a conscientizar sobre os impactos das condições climáticas na poluição.

---

#### **Conclusão**
Este projeto combina ciência de dados, aprendizado de máquina e desenvolvimento de software para criar uma solução prática e útil. Ele não apenas prevê a qualidade do ar, mas também fornece insights sobre como as condições climáticas influenciam a poluição. A aplicação pode ser expandida para incluir mais cidades e variáveis, tornando-a uma ferramenta ainda mais poderosa para planejamento e conscientização ambiental.

---

#### **Próximos Passos**
- Expandir o modelo para incluir mais cidades e fontes de dados.
- Melhorar o modelo com técnicas avançadas de aprendizado de máquina, como redes neurais.

---
