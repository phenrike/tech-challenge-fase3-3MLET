# app/application/services.py
from infra.openaq_api import OpenAQApi, WeatherAPI
from infra.database import Database
from datetime import datetime, timedelta
from typing import List, Dict, Any
from .progress_manager import ProgressManager
import unicodedata

def remove_accents(text: str) -> str:
    """Remove acentos de uma string"""
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')

class SensorService:
    def __init__(self, repository: OpenAQApi):
        self.repository = repository

    def get_pm25_sensors(self):
        return self.repository.get_pm25_sensors_from_chile()

class MeasurementService:
    def __init__(self, repository: OpenAQApi):
        self.repository = repository

    def get_measurements_for_all_sensors(self, datetime_from: str, datetime_to: str):
        sensor_service = SensorService(self.repository)
        sensors = sensor_service.get_pm25_sensors()

        if not sensors:
            return []

        measurements = []
        for sensor in sensors:
            measurements.extend(self.repository.get_measurements(sensor["id"], datetime_from, datetime_to, sensor["city"]))

        return measurements

class HistoryService:
    def __init__(self, repository: WeatherAPI):
        self.repository = repository

    def get_city_history(self, city: str, date: str):
        return self.repository.get_history(city, date)
    
class FutureService:
    def __init__(self, repository: WeatherAPI):
        self.repository = repository

    def get_city_future(self, city: str, date: str):
        return self.repository.get_future(city, date)

class OrchestratorService:
    def __init__(self, measurement_service: MeasurementService, history_service: HistoryService, database: Database):
        self.measurement_service = measurement_service
        self.history_service = history_service
        self.database = database
        self._progress = None

    def process_city_measurements(self, measurements: List[Any], city: str) -> Dict[str, int]:
        """Processa as medições de uma cidade específica"""
        city_measurements = [m for m in measurements if m.city == city]
        inserted_count = 0

        for measurement in city_measurements:
            try:
                self.database.insert_measurement(
                    id_sensor=measurement.sensor_id,
                    ds_city=measurement.city,
                    dt_date_from=datetime.strptime(measurement.datetime_from, "%Y-%m-%dT%H:%M:%S%z"),
                    dt_date_to=datetime.strptime(measurement.datetime_to, "%Y-%m-%dT%H:%M:%S%z"),
                    qt_pm25=measurement.value
                )
                inserted_count += 1
            except Exception as e:
                print(f"Erro ao inserir medição para cidade {city}: {str(e)}")
                self.database.rollback()
                raise

        return {"measurements_inserted": inserted_count}

    def process_city_weather(self, city: str, datetime_from: str, datetime_to: str) -> Dict[str, int]:
        """Processa o histórico do clima de uma cidade específica para cada dia do intervalo"""
        try:
            # Converte as strings de data para objetos datetime
            start_date = datetime.strptime(datetime_from.split('T')[0], "%Y-%m-%d")
            end_date = datetime.strptime(datetime_to.split('T')[0], "%Y-%m-%d")
            
            total_inserted = 0
            current_date = start_date
            days_processed = 0
            total_days = (end_date - start_date).days + 1
            
            # Remove acentos do nome da cidade
            city_without_accents = remove_accents(city)
            print(f"\nProcessando dados climáticos para {city} (sem acentos: {city_without_accents})")
            
            while current_date <= end_date:
                date_str = current_date.strftime("%Y-%m-%d")
                print(f"\nProcessando dados climáticos para {city} na data: {date_str}")
                
                weather_data = self.history_service.get_city_history(city_without_accents, date_str)
                if not weather_data:
                    print(f"Nenhum dado climático encontrado para a cidade {city} na data {date_str}")
                    current_date += timedelta(days=1)
                    days_processed += 1
                    continue

                for weather in weather_data:
                    try:
                        self.database.insert_weather_history(
                            ds_city=weather["city"],
                            dt_date=datetime.strptime(weather["date"], "%Y-%m-%d"),
                            qt_avg_humidity=weather["avg_humidity"],
                            qt_avg_temp_c=weather["avg_temp_c"],
                            qt_avg_vis_km=weather["avg_vis_km"],
                            qt_max_wind_kph=weather["max_wind_kph"],
                            qt_total_precip_mm=weather["total_precip_mm"],
                            qt_pressure_mb=weather["pressure_mb"]
                        )
                        total_inserted += 1
                    except Exception as e:
                        print(f"Erro ao inserir histórico do clima para cidade {city}: {str(e)}")
                        self.database.rollback()
                        raise

                current_date += timedelta(days=1)
                days_processed += 1

            return {
                "weather_history_inserted": total_inserted, 
                "no_data": False,
                "days_processed": days_processed,
                "total_days": total_days
            }
        except Exception as e:
            print(f"Erro ao processar histórico do clima para cidade {city}: {str(e)}")
            self.database.rollback()
            raise

    def get_progress(self) -> Dict[str, Any]:
        """Retorna o progresso atual do processamento"""
        if self._progress is None:
            return {"status": "not_started"}
        return self._progress

    def process_and_save_data(self, datetime_from: str, datetime_to: str):
        """Processa e salva dados por cidade, fazendo commit após cada cidade"""
        try:
            print("\n=== INICIANDO PROCESSAMENTO DE DADOS ===")
            
            # ETAPA 1: Processamento das medições
            print("\n=== ETAPA 1: Processando medições dos sensores ===")
            measurements = self.measurement_service.get_measurements_for_all_sensors(datetime_from, datetime_to)
            cities = list(set(m.city for m in measurements))
            
            # Inicializa o gerenciador de progresso
            progress_manager = ProgressManager(len(cities))
            self._progress = progress_manager._calculate_progress()
            
            # Processa medições por cidade
            for city in cities:
                try:
                    print(f"\nProcessando medições para cidade: {city}")
                    measurement_result = self.process_city_measurements(measurements, city)
                    self.database.commit()
                    print(f"Medições inseridas para {city}: {measurement_result['measurements_inserted']}")
                    
                    # Atualiza progresso
                    self._progress = progress_manager.update_progress(
                        city=city,
                        measurements_inserted=measurement_result["measurements_inserted"]
                    )
                    
                except Exception as e:
                    print(f"Erro ao processar medições para cidade {city}: {str(e)}")
                    self.database.rollback()
                    self._progress = progress_manager.add_error(
                        city=city,
                        error_type="measurement_error",
                        error_message=str(e)
                    )

            # ETAPA 2: Processamento do histórico do clima
            print("\n=== ETAPA 2: Processando histórico do clima ===")
            
            for city in cities:
                try:
                    print(f"\nProcessando histórico do clima para cidade: {city}")
                    weather_result = self.process_city_weather(city, datetime_from, datetime_to)
                    self.database.commit()
                    print(f"Registros climáticos inseridos para {city}: {weather_result['weather_history_inserted']}")
                    
                    # Atualiza progresso
                    self._progress = progress_manager.update_progress(
                        city=city,
                        weather_records_inserted=weather_result["weather_history_inserted"]
                    )
                    
                except Exception as e:
                    print(f"Erro ao processar histórico do clima para cidade {city}: {str(e)}")
                    self.database.rollback()
                    self._progress = progress_manager.add_error(
                        city=city,
                        error_type="weather_error",
                        error_message=str(e)
                    )

            print("\n=== PROCESSAMENTO CONCLUÍDO ===")
            return progress_manager.get_final_result()

        except Exception as e:
            print(f"\nErro geral no processamento: {str(e)}")
            self.database.rollback()
            raise