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
- **Prevê valor de PM2.5** (`GET /forecast_pm25?city=Santiago&date=2025-04-05`)

---

## 🛠 Tecnologias Utilizadas
- **Python 3**
- **Flask** (para criação da API)
- **Requests** (para consumir a API OpenAQ)
- **Clean Architecture** (separação em camadas)
- **PostgreSQL** (banco de dados)
- **Docker** (containerização)
- **Weather API** (dados climáticos)
- **React** (front-end)

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
│   ├── openaq_api.py      # Consumo das APIs OpenAQ e Weather
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
├── best_rf_model.pkl      # Arquivo com o modelo treinado
├── main.py                # Inicialização do Flask
├── notebook.ipynb         # Notebook para tratamento de dados e treinamento do modelo de ML
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
```

### 📍 **Endpoint de predição**
```sh
GET http://localhost:8080/forecast_pm25?city=Santiago&date=2025-04-05
```

📌 **Resposta:**
```sh
{
        "qt_avg_humidity": 34.0,
        "qt_avg_temp_c": 13.3,
        "qt_avg_vis_km": 10.0,
        "qt_max_wind_kph": 10.4,
        "qt_total_precip_mm": 0.1,
        "qt_pressure_mb": 1017.5416666667,
        "qt_pm25": 27.732,
        "ano": 2025,
        "mes": 4,
        "dia": 28,
        "qt_pm25_ma3": 28.1203333333,
        "qt_pm25_ma7": 28.2025714286,
        "qt_pm25_ma14": 28.08375,
        "qt_pm25_ema": 28.127782421,
        "qt_pm25_std7": 0.3547133148,
        "qt_pm25_trend": 0.0822380952,
        "dia_semana": 0,
        "mes_ano": 4,
        "estacao": 2,
        "temp_umidade": 452.2,
        "pressao_umidade": 34596.4166666667,
        "vento_umidade": 353.6,
        "ds_city_Puerto Montt": 0.0,
        "ds_city_Puerto Varas": 0.0,
        "ds_city_Santiago": 1.0,
        "ds_city_Valparaiso": 0.0
    }
}
```

## Contexto da Aplicação

#### **Introdução**
Imagine que você está planejando uma viagem para uma das cidades do Chile, como Santiago ou Puerto Montt, e deseja saber como estará a qualidade do ar nos próximos dias. A poluição do ar, especialmente o índice de partículas PM2.5, pode impactar diretamente a saúde, especialmente para pessoas com problemas respiratórios. Pensando nisso, desenvolvemos uma solução que combina ciência de dados, aprendizado de máquina e tecnologia para prever o índice de poluição PM2.5.

---

#### **Objetivo**
O objetivo deste projeto é criar uma aplicação que permita aos usuários consultar a previsão do índice de poluição PM2.5 em tempo real para diferentes cidades do Chile. A aplicação utiliza dados climáticos históricos para treinar um modelo de aprendizado de máquina que realiza previsões precisas. Além disso, os dados são armazenados em um banco de dados para facilitar consultas e análises futuras.

---

#### **Etapas do Projeto**

1. **Coleta de Dados**
   - Utilizamos APIs públicas, como a WeatherAPI e a OpenAQ, para coletar dados climáticos e de qualidade do ar em tempo real.
   - Os dados incluem informações como temperatura média, umidade, velocidade do vento, visibilidade, pressão atmosférica, precipitação e o índice de PM2.5.

2. **Armazenamento de Dados**
   - Os dados coletados são armazenados em um banco de dados PostgreSQL, estruturado para suportar consultas eficientes.
   - Criamos tabelas específicas para armazenar o histórico climático (`tbl_weather_history`) e as medições de sensores de poluição (`tbl_measurements`).

3. **Pré-Processamento e Preparação dos Dados**
   - Verificamos a necessidade de tratamento de valores ausentes e duplicados.
   - Codificamos variáveis categóricas, como o nome das cidades.
   - Padronizamos os dados para garantir que todas as variáveis estejam na mesma escala.
   - Unimos as duas tabelas em um único dataframe para utilizar no treinamento do modelo.

4. **Treinamento do Modelo**
   - Utilizamos um modelo de aprendizado de máquina baseado em Random Forest Regressor, que foi escolhido por sua robustez e capacidade de lidar com dados não lineares.
   - O modelo foi treinado com as seguintes features climáticas:
     - Umidade média (`qt_avg_humidity`)
     - Temperatura média (`qt_avg_temp_c`)
     - Visibilidade média (`qt_avg_vis_km`)
     - Velocidade máxima do vento (`qt_max_wind_kph`)
     - Precipitação total (`qt_total_precip_mm`)
     - Pressão atmosférica média (`qt_pressure_mb`)
   - Avaliamos o modelo utilizando métricas como RMSE (Root Mean Squared Error) e MAPE (Mean Absolute Percentage Error).

5. **Melhorando a Previsão do Modelo - Feature Engineering**
   - Ao realizar as primeiras previsões, notamos que o valor target ficava constante para diferentes datas futuras.
   - Com pesquisas, notamos que o modelo que estávamos utilizando não capturava a tendência e fazia apenas uma previsão pontual.
   - Implementamos mais variáveis com a intenção de capturar a tendência dos dados e melhorar a previsão.
   - Features de médias móveis:
     - Média móvel de 3 dias (`qt_pm25_ma3`)
     - Média móvel de 7 dias (`qt_pm25_ma7`)
     - Média móvel de 14 dias (`qt_pm25_ma14`)
     - Média móvel exponencial com um período de suavização de 7 dias (`qt_pm25_ema`)
     - Desvio padrão de 7 dias (`qt_pm25_std7`)
     - Tendência - diferença entre média móvel de 7 dias e média móvel de 3 dias (`qt_pm25_trend`)
   - Features de sazonalidade:
     - Dia da semana (`dia_semana`)
     - Mês do ano (`dia_semana`)
     - Estação (`dia_semana`)
   - Features de interação entre as variáveis climáticas:
     - Produto de temperatura e umidade (`temp_umidade`)
     - Produto de pressão e umidade (`pressao_umidade`)
     - Pressão de vento e umidade (`vento_umidade`)

6. **Desenvolvimento da API**
   - Criamos uma API RESTful utilizando Flask para permitir que os usuários consultem a previsão do índice PM2.5.
   - A API coleta dados climáticos em tempo real, processa-os e utiliza o modelo treinado para realizar a previsão.
   - Endpoints principais:
     - `/forecast-pm25`: Retorna a previsão do índice PM2.5 para uma cidade e data específicas.
     - `/weather-history`: Retorna o histórico climático de uma cidade.
     - `/weather-future`: Retorna a previsão climática futura de uma cidade.

7. **Armazenamento e Orquestração**
   - Implementamos um serviço de orquestração que coleta dados, processa-os e os armazena no banco de dados.

8. **Visualização**
   - Criamos uma interface em que o usuário pode escolher a cidade e a data desejada.
   - É gerada uma visualização que mostra a previsão de PM 2.5, bem como um indicador visual sobre o nível da qualidade do ar.
   - Além da cor, existe um campo que traz a qualidade do ar e um outro campo com a recomendação a respeito desse nível de PM2.5

---

#### **Demonstração da Aplicação**
1. **Consulta de Previsão**
   - O usuário acessa a Aplicação e insere a cidade e a data desejadas.
   - A aplicação retorna a previsão do índice PM2.5, juntamente com os dados climáticos utilizados na previsão.

2. **Exemplo de Uso**
   - **Requisição**: `GET \forecast_pm25?city=Santiago&date=2025-04-28`
   - **Resposta**:
     ```json
     {
        "qt_avg_humidity": 34.0,
        "qt_avg_temp_c": 13.3,
        "qt_avg_vis_km": 10.0,
        "qt_max_wind_kph": 10.4,
        "qt_total_precip_mm": 0.1,
        "qt_pressure_mb": 1017.5416666667,
        "qt_pm25": 27.732,
        "ano": 2025,
        "mes": 4,
        "dia": 28,
        "qt_pm25_ma3": 28.1203333333,
        "qt_pm25_ma7": 28.2025714286,
        "qt_pm25_ma14": 28.08375,
        "qt_pm25_ema": 28.127782421,
        "qt_pm25_std7": 0.3547133148,
        "qt_pm25_trend": 0.0822380952,
        "dia_semana": 0,
        "mes_ano": 4,
        "estacao": 2,
        "temp_umidade": 452.2,
        "pressao_umidade": 34596.4166666667,
        "vento_umidade": 353.6,
        "ds_city_Puerto Montt": 0.0,
        "ds_city_Puerto Varas": 0.0,
        "ds_city_Santiago": 1.0,
        "ds_city_Valparaiso": 0.0
      }
4. **Visão da Aplicação**
  ![alt text](image.png)
4. **Benefícios**
   - Permite que os usuários planejem suas viagens com base na qualidade do ar.
   - Ajuda a conscientizar sobre os impactos das condições climáticas na poluição.

---

#### **Conclusão**
Este projeto combina ciência de dados, aprendizado de máquina e desenvolvimento de software para criar uma solução prática e útil. Ele não apenas prevê a qualidade do ar, mas também fornece insights sobre como as condições climáticas influenciam a poluição. A aplicação pode ser expandida para incluir mais cidades e variáveis, tornando-a uma ferramenta ainda mais poderosa para planejamento e conscientização ambiental.

---

#### **Próximos Passos**
- Expandir o modelo para incluir mais cidades e fontes de dados.
- Melhorar o modelo com técnicas avançadas de aprendizado de máquina, como redes neurais.
- Automatizar a coleta de dados, para que novos dados sejam incluídos na base histórica.

---
