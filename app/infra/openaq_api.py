# app/infra/openaq_api.py
import requests
from interfaces.sensor_repository import SensorRepository
from interfaces.measurement_repository import MeasurementRepository
from domain.models import Measurement
import numpy as np
from datetime import date, timedelta
from flask import jsonify
import pandas as pd
import pickle
from sqlalchemy import create_engine
from sklearn.preprocessing import OneHotEncoder
import os
from dotenv import load_dotenv

# Carregar as variáveis do arquivo .env
load_dotenv()
OpenAQApi_key = os.getenv("X_API_KEY")
weatherAPI_key = os.getenv("WEATHER_API_KEY")
import joblib

class OpenAQApi(SensorRepository, MeasurementRepository):
    BASE_URL = "https://api.openaq.org/v3"
    HEADERS = {"accept": "application/json", "X-API-Key": OpenAQApi_key}

    def get_pm25_sensors_from_chile(self):
        """ Obtém os sensores de PM2.5 no Chile """
        url = f"{self.BASE_URL}/locations"
        params = {"limit": 200, "page": 1, "order_by": "id", "sort_order": "asc", "iso": "CL"}
        response = requests.get(url, headers=self.HEADERS, params=params)
        data = response.json()

        sensors = []
        city_list = ['Santiago', 'Puerto Montt', 'Puerto Varas', 'Valparaíso', 'Viña del Mar']
        for location in data.get("results", []):
            if location.get("country", {}).get("code") == "CL" and location.get("locality") in city_list:
                for sensor in location.get("sensors", []):
                    if sensor.get("parameter", {}).get("name") == "pm25":
                        sensors.append({
                            "id": sensor["id"],
                            "city": location["locality"]
                        })
        return sensors

    def get_measurements(self, sensor_id: int, datetime_from: str, datetime_to: str, city: str):
        """ Obtém medições de um sensor específico """
        url = f"{self.BASE_URL}/sensors/{sensor_id}/measurements/daily"
        params = {"datetime_from": datetime_from, "datetime_to": datetime_to, "limit": 1000}
        response = requests.get(url, headers=self.HEADERS, params=params)

        if response.status_code != 200:
            return []

        data = response.json()
        measurements = []

        for result in data.get("results", []):
            measurements.append(
                Measurement(
                    sensor_id=sensor_id,
                    value=result["value"],
                    datetime_from=result["period"]["datetimeFrom"]["local"],
                    datetime_to=result["period"]["datetimeTo"]["local"],
                    city=city
                )
            )

        return measurements

class WeatherAPI():
    BASE_URL = "http://api.weatherapi.com/v1/"
    def get_history(self, city: str, date_str: str):
        """Obtém dados históricos de um determinado dia e uma cidade específica"""
        url = f"{self.BASE_URL}/history.json"
        data_obj = date.fromisoformat(date_str)
        today = date.today()
        interval = (today - data_obj).days
        data_list = []
        
        # Verifica se a data está dentro do limite permitido (1 ano)
        if interval > 365:
            print(f"Aviso: A data {date_str} está muito distante. A API só permite consultas até 1 ano atrás.")
            # Ajusta a data para exatamente um ano atrás
            data_obj = today - timedelta(days=365)
            print(f"Usando data ajustada: {data_obj}")
            
        params = {"key": weatherAPI_key, "q": city, "dt": data_obj.strftime("%Y-%m-%d")}
        response = requests.get(url, params=params)
        data = response.json()
        
        if response.status_code != 200:
            if "error" in data:
                error_code = data["error"].get("code")
                error_message = data["error"].get("message")
                print(f"Erro na API Weather: Código {error_code} - {error_message}")
                if error_code == 1008:
                    print("Limite da API atingido. Apenas dados de até 1 ano atrás são permitidos.")
                return []
            return []
            
        try:
            city = data["location"]["name"]
            date_var = data["forecast"]["forecastday"][0]["date"]
            avg_humidity = data["forecast"]["forecastday"][0]["day"]["avghumidity"]
            avg_temp_c = data["forecast"]["forecastday"][0]["day"]["avgtemp_c"]
            avg_vis_km = data["forecast"]["forecastday"][0]["day"]["avgvis_km"]
            max_wind_kph = data["forecast"]["forecastday"][0]["day"]["maxwind_kph"]
            total_precip_mm = data["forecast"]["forecastday"][0]["day"]["totalprecip_mm"]
            hours = data["forecast"]["forecastday"][0]["hour"]
            pressure_mb = float(np.mean([hour["pressure_mb"] for hour in hours]))
            
            return [{
                "city": city,
                "date": date_var,
                "avg_humidity": avg_humidity,
                "avg_temp_c": avg_temp_c,
                "avg_vis_km": avg_vis_km,
                "max_wind_kph": max_wind_kph,
                "total_precip_mm": total_precip_mm,
                "pressure_mb": pressure_mb
            }]
        except Exception as e:
            print(f"Erro ao processar dados para {city} em {data_obj}: {str(e)}")
            return []

    def get_future(self, city: str, date_str: str):
        """Obtém dados da previsão do tempo de um determinado dia e uma cidade específica"""
        
        params = {"key": weatherAPI_key, "q": city, "dt": date_str}
        # check date interval to decide if the url will be future or forecast
        data_obj = date.fromisoformat(date_str)
        today = date.today()
        interval = (data_obj - today).days
        if interval <= 14:
            # forecast
            url = f"{self.BASE_URL}/forecast.json"
            params["aqi"] = "no"
            params["alerts"] = "no"
        else:
            # future
            url = f"{self.BASE_URL}/future.json"
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return []

        data = response.json()
        print(data)
        city = data["location"]["name"]
        date_var = data["forecast"]["forecastday"][0]["date"]
        avg_humidity = data["forecast"]["forecastday"][0]["day"]["avghumidity"]
        avg_temp_c = data["forecast"]["forecastday"][0]["day"]["avgtemp_c"]
        avg_vis_km = data["forecast"]["forecastday"][0]["day"]["avgvis_km"]
        max_wind_kph = data["forecast"]["forecastday"][0]["day"]["maxwind_kph"]
        total_precip_mm = data["forecast"]["forecastday"][0]["day"]["totalprecip_mm"]
        # extracting hour list
        hours = data["forecast"]["forecastday"][0]["hour"]
        # taking pressure_mb values and taking its mean
        pressure_mb = np.mean([hour["pressure_mb"] for hour in hours])
        #"http://127.0.0.1:5000/weather-future?city=Santiago&date=2025-04-20"
        return {
        "city": city,
        "date": date_var,
        "avg_humidity": avg_humidity,
        "avg_temp_c": avg_temp_c,
        "avg_vis_km": avg_vis_km,
        "max_wind_kph": max_wind_kph,
        "total_precip_mm": total_precip_mm,
        "pressure_mb": pressure_mb
        }
    
    def forecast_pm25(self, city: str, date_str: str):
        """Obtém a previsão do pm 2.5 na cidade e data escolhidas"""
        # load the saved model
        model = joblib.load("app/model.pkl")

        # load the most recent historical data - same logic as the notebook
        # configure postgres connection 
        USER = "postgres"
        PASSWORD = "password"
        HOST = "db" 
        PORT = "5432" 
        DB_NAME = "db_measurements"
        # connection string
        conn_str = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
        # create connection engine
        engine = create_engine(conn_str)
        # test connection and load data into a dataframe
        query = "SELECT * FROM tbl_weather_history"
        df_weather_history = pd.read_sql(query, engine)
        query = "SELECT * FROM tbl_measurements"
        df_measurements = pd.read_sql(query, engine)
        # date transformations
        df_weather_history['dt_date'] = df_weather_history['dt_date'].apply(lambda x: x.isoformat() if pd.notnull(x) else None)
        df_measurements['dt_date'] = df_measurements['dt_date_from'].apply(lambda x: x.date().isoformat() if pd.notnull(x) else None)
        # merge both dataframes
        df = pd.merge(df_weather_history, df_measurements, on=['ds_city', 'dt_date'], how='inner')
        # drop columns
        df.drop(columns=['id_x', 'id_y', 'id_sensor', 'dt_date_from', 'dt_date_to'], inplace=True)
        # mean pm2.5 column
        df = df.groupby(['ds_city', 'dt_date']).mean().reset_index()
         # Converter dt_date para datetime
        df['dt_date'] = pd.to_datetime(df['dt_date'])
        
        # Adicionar features de data
        df["ano"] = df["dt_date"].dt.year
        df["mes"] = df["dt_date"].dt.month
        df["dia"] = df["dt_date"].dt.day
        
        # Ordenar por cidade e data
        df = df.sort_values(['ds_city', 'dt_date'])
        
        # Criar médias móveis para diferentes períodos
        df['qt_pm25_ma3'] = df.groupby('ds_city')['qt_pm25'].transform(lambda x: x.rolling(window=3, min_periods=1).mean())
        df['qt_pm25_ma7'] = df.groupby('ds_city')['qt_pm25'].transform(lambda x: x.rolling(window=7, min_periods=1).mean())
        df['qt_pm25_ma14'] = df.groupby('ds_city')['qt_pm25'].transform(lambda x: x.rolling(window=14, min_periods=1).mean())
        df['qt_pm25_ema'] = df.groupby('ds_city')['qt_pm25'].transform(lambda x: x.ewm(span=7, adjust=False).mean())
        df['qt_pm25_std7'] = df.groupby('ds_city')['qt_pm25'].transform(lambda x: x.rolling(window=7, min_periods=1).std().fillna(0))
        df['qt_pm25_trend'] = df['qt_pm25_ma7'] - df['qt_pm25_ma3']
        
        # Features de sazonalidade
        df['dia_semana'] = df['dt_date'].dt.dayofweek
        df['mes_ano'] = df['dt_date'].dt.month
        df['estacao'] = df['dt_date'].dt.month % 12 // 3 + 1
        
        # Features de interação
        df['temp_umidade'] = df['qt_avg_temp_c'] * df['qt_avg_humidity']
        df['pressao_umidade'] = df['qt_pressure_mb'] * df['qt_avg_humidity']
        df['vento_umidade'] = df['qt_max_wind_kph'] * df['qt_avg_humidity']
        
        # instanciating one hot encoder class
        encoder = OneHotEncoder()
        encoded_data = encoder.fit_transform(df[['ds_city']]).toarray()
        df_encoded = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(['ds_city']))
        # concatenate new data codifying the data
        df_encoded = pd.concat([df, df_encoded], axis=1)
        df = df_encoded
        # filter data based on the chosen city
        df = df.query(f'ds_city == "{city}"')
        df.drop(columns=['ds_city'], inplace = True)
        # drop previous date column and order by date
        df = df.sort_values(by=['ano', 'mes', 'dia'])
        last_date = pd.to_datetime(df['dt_date'].iloc[-1])
        df.drop(columns=['dt_date'], inplace=True)
        
        # create a dataframe to store future predictions
        df_prev = df.copy()
        
        # get features from the dataframe
        features = [
            'qt_avg_humidity', 'qt_avg_temp_c', 'qt_avg_vis_km', 
            'qt_max_wind_kph', 'qt_total_precip_mm', 'qt_pressure_mb',
            'qt_pm25_ma3', 'qt_pm25_ma7', 'qt_pm25_ma14',
            'qt_pm25_ema', 'qt_pm25_std7', 'qt_pm25_trend',
            'dia_semana', 'mes_ano', 'estacao',
            'temp_umidade', 'pressao_umidade', 'vento_umidade'#,
            #'ano', 'mes', 'dia'
        ] + [col for col in df.columns if col.startswith('ds_city_')]
        
        # iterate over days for prediction        
        while last_date < pd.to_datetime(date_str):
            # update last_date
            last_date = pd.to_datetime(last_date)
            last_date += pd.Timedelta(days=1)
            # get preview from API
            weather_data = self.get_future(city, last_date.strftime('%Y-%m-%d'))
            new_entry = df_prev.iloc[-1:].copy()
            # format json data to create a new entry for the history dataframe
            new_entry['qt_avg_humidity'] = weather_data['avg_humidity']
            new_entry['qt_avg_temp_c'] = weather_data['avg_temp_c']
            new_entry['qt_avg_vis_km'] = weather_data['avg_vis_km']
            new_entry['qt_max_wind_kph'] = weather_data['max_wind_kph']
            new_entry['qt_total_precip_mm'] = weather_data['total_precip_mm']
            new_entry['qt_pressure_mb'] = weather_data['pressure_mb']

            # atualizar data
            new_entry['ano'] = last_date.year
            new_entry['mes'] = last_date.month
            new_entry['dia'] = last_date.day
            new_entry['dia_semana'] = last_date.dayofweek
            new_entry['mes_ano'] = last_date.month
            new_entry['estacao'] = last_date.month % 12 // 3 + 1
            
            # atualizar features de interação
            new_entry['temp_umidade'] = new_entry['qt_avg_temp_c'] * new_entry['qt_avg_humidity']
            new_entry['pressao_umidade'] = new_entry['qt_pressure_mb'] * new_entry['qt_avg_humidity']
            new_entry['vento_umidade'] = new_entry['qt_max_wind_kph'] * new_entry['qt_avg_humidity']
            
            # garantir que colunas ds_city estejam corretas
            for column in new_entry.columns:
                if column.startswith('ds_city_'):
                    if column == f'ds_city_{city}':
                        new_entry[column] = 1
                    else:
                        new_entry[column] = 0
            
            # fazer previsão
            new_entry['qt_pm25'] = model.predict(new_entry[features])
            
            # atualizar médias móveis para a próxima iteração
            df_prev = pd.concat([df_prev, new_entry], ignore_index=True)
            
            # Recalcular médias móveis após adicionar nova entrada
            last_rows = df_prev.tail(14).copy()  # Pegamos as últimas 14 linhas para garantir cálculos corretos
            new_entry['qt_pm25_ma3'] = last_rows['qt_pm25'].tail(3).mean()
            new_entry['qt_pm25_ma7'] = last_rows['qt_pm25'].tail(7).mean()
            new_entry['qt_pm25_ma14'] = last_rows['qt_pm25'].tail(14).mean()
            new_entry['qt_pm25_ema'] = last_rows['qt_pm25'].ewm(span=7, adjust=False).mean().iloc[-1]
            new_entry['qt_pm25_std7'] = last_rows['qt_pm25'].tail(7).std() if len(last_rows) >= 7 else 0
            new_entry['qt_pm25_trend'] = new_entry['qt_pm25_ma7'] - new_entry['qt_pm25_ma3']
            
            # Atualizar a última entrada com os valores recalculados
            df_prev.iloc[-1] = new_entry

        return df_prev.tail(1).to_json(orient='records', index=False)