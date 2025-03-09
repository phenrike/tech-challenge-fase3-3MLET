# 🌎 API de Sensores de Qualidade do Ar (OpenAQ)

## 📌 Sobre o Projeto
Esta API fornece dados sobre sensores de qualidade do ar no Chile, focando no poluente **PM2.5**. A API consome informações da **OpenAQ API** e permite consultar sensores disponíveis e suas medições dentro de um intervalo de datas.

## 🚀 Funcionalidades
- **Listar sensores de PM2.5 no Chile** (`GET /sensors/pm25/chile`)
- **Obter medições de todos os sensores** (`GET /sensor-data?datetime_from=YYYY-MM-DD&datetime_to=YYYY-MM-DD`)

---

## 🛠 Tecnologias Utilizadas
- **Python 3**
- **Flask** (para criação da API)
- **Requests** (para consumir a API OpenAQ)
- **Clean Architecture** (separação em camadas)

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
├── infra/         # Implementação de APIs externas
│   ├── openaq_api.py       # Consumo da API OpenAQ
│
├── application/            # Regras de negócio
│   ├── services.py         # Serviços para sensores e medições
│
├── presentation/           # Camada de apresentação (controllers)
│   ├── controllers.py      # Rotas da API
│
├── main.py                 # Inicialização do Flask
└── README.md
```

---

## 🏗 Como Configurar e Rodar a API

### 1️⃣ Clonar o repositório
```sh
git clone https://github.com/phenrike/tech-challenge-fase3-3MLET.git
cd tech-challenge-fase3-3MLET
```

### 2️⃣ Criar e ativar ambiente virtual
```sh
python3 -m venv venv
source venv/bin/activate  # (Linux/Mac)
venv\Scripts\activate     # (Windows)
```

### 3️⃣ Instalar dependências
```sh
pip install -r requirements.txt
```

### 4️⃣ Definir chave de API do OpenAQ
Crie um arquivo **.env** na raiz do projeto e adicione:
```sh
X_API_KEY=sua_api_key_aqui
```

### 5️⃣ Rodar a API
```sh
python app/main.py
```

A API estará rodando em **http://127.0.0.1:5000** 🚀

---

## 🔥 Como Usar os Endpoints

### 📍 **Listar sensores de PM2.5 no Chile**
```sh
GET http://127.0.0.1:5000/sensors/pm25/chile
```
📌 **Resposta:**
```json
{
  "pm25_sensors": [1044, 2045, 3067]
}
```

### 📍 **Obter medições de todos os sensores**
```sh
GET http://127.0.0.1:5000/sensor-data?datetime_from=2024-01-01&datetime_to=2024-01-31
```
📌 **Resposta:**
```json
[
  {
    "sensor_id": 1044,
    "value": 29.1,
    "datetimeFrom_local": "2024-01-01T00:00:00-03:00",
    "datetimeTo_local": "2024-01-02T00:00:00-03:00"
  }
]
```