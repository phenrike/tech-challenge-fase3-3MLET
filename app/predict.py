from flask import Flask, request, jsonify
import pickle
import numpy as np
import requests

app = Flask(__name__)

# Carregar o modelo treinado
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Endpoint para prever o índice PM2.5
@app.route("/predict-pm25", methods=["GET"])
def predict_pm25():
    try:
        city = request.args.get("city")
        date = request.args.get("date")

        if not city or not date:
            return jsonify({"error": "Parâmetros 'city' e 'date' são obrigatórios"}), 400

        # Consultar a API de previsão do tempo
        weather_api_url = "https://api.weatherapi.com/v1/forecast.json"
        weather_api_key = "3a32179cc75946e2acd01006252103"  # Substitua pela sua chave da WeatherAPI
        params = {
            "key": weather_api_key,
            "q": city,
            "dt": date
        }

        response = requests.get(weather_api_url, params=params)

        if response.status_code != 200:
            return jsonify({"error": f"Erro ao consultar a WeatherAPI: {response.status_code}"}), 500

        data = response.json()

        # Verificar se os dados climáticos estão disponíveis
        if "forecast" not in data or "forecastday" not in data["forecast"] or len(data["forecast"]["forecastday"]) == 0:
            return jsonify({"error": "Dados climáticos não disponíveis para a data fornecida"}), 500

        # Extrair os dados climáticos necessários
        forecast = data["forecast"]["forecastday"][0]["day"]
        temperature = forecast.get("avgtemp_c")
        humidity = forecast.get("avghumidity")
        wind_speed = forecast.get("maxwind_kph")

        if temperature is None or humidity is None or wind_speed is None:
            return jsonify({"error": "Dados climáticos incompletos"}), 500

        # Fazer a previsão do índice PM2.5
        features = np.array([[temperature, humidity, wind_speed]])
        predicted_pm25 = model.predict(features)[0]

        return jsonify({
            "city": city,
            "date": date,
            "predicted_pm25": predicted_pm25,
            "weather_data": {
                "temperature": temperature,
                "humidity": humidity,
                "wind_speed": wind_speed
            }
        })

    except Exception as e:
        # Log do erro no terminal
        print(f"Erro no servidor: {e}")
        return jsonify({"error": "Ocorreu um erro interno no servidor"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)