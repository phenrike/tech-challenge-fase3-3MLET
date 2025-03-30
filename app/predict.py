from flask import Flask, request, jsonify
import joblib
import numpy as np
import requests

app = Flask(__name__)

# Carregar o modelo treinado
model = joblib.load("best_rf_model.pk")

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
        visibility = forecast.get("avgvis_km")
        pressure = forecast.get("pressure_mb")
        precipitation = forecast.get("totalprecip_mm")

        # Verificar e registrar parâmetros ausentes
        missing_params = {}
        if temperature is None:
            missing_params["temperature"] = "Ausente"
            temperature = 0  # Valor padrão
        if humidity is None:
            missing_params["humidity"] = "Ausente"
            humidity = 0  # Valor padrão
        if wind_speed is None:
            missing_params["wind_speed"] = "Ausente"
            wind_speed = 0  # Valor padrão
        if visibility is None:
            missing_params["visibility"] = "Ausente"
            visibility = 0  # Valor padrão
        if pressure is None:
            missing_params["pressure"] = "Ausente"
            pressure = 0  # Valor padrão
        if precipitation is None:
            missing_params["precipitation"] = "Ausente"
            precipitation = 0  # Valor padrão

        # Log dos parâmetros ausentes
        if missing_params:
            print(f"Parâmetros ausentes: {missing_params}")

        # Fazer a previsão do índice PM2.5
        features = np.array([[temperature, humidity, wind_speed, visibility, pressure, precipitation]])
        predicted_pm25 = int(model.predict(features)[0])

        return jsonify({
            "city": city,
            "date": date,
            "predicted_pm25": predicted_pm25,
            "weather_data": {
                "temperature": temperature,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "visibility": visibility,
                "pressure": pressure,
                "precipitation": precipitation
            },
            "missing_parameters": missing_params
        })

    except Exception as e:
        # Log do erro no terminal
        print(f"Erro no servidor: {e}")
        return jsonify({"error": "Ocorreu um erro interno no servidor"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)