from typing import Dict, List, Any
from datetime import datetime
import time

class ProgressManager:
    def __init__(self, total_cities: int):
        self.total_cities = total_cities
        self.processed_cities = 0
        self.start_time = time.time()
        self.errors = []
        self.measurements_inserted = 0
        self.weather_cities = {}

    def _calculate_progress(self) -> Dict[str, Any]:
        elapsed_time = time.time() - self.start_time
        return {
            "elapsed_time_seconds": round(elapsed_time, 2),
            "errors": self.errors,
            "measurements": {
                "progress_percentage": round((self.processed_cities / self.total_cities) * 100, 2) if self.total_cities > 0 else 0,
                "total_inserted": self.measurements_inserted,
                "processed_cities": self.processed_cities
            },
            "weather": {
                "progress_percentage": round((len(self.weather_cities) / self.total_cities) * 100, 2) if self.total_cities > 0 else 0,
                "cities": [
                    {
                        "city": city,
                        "total_inserted": data["total_inserted"]
                    }
                    for city, data in self.weather_cities.items()
                ]
            }
        }

    def update_progress(self, city: str, measurements_inserted: int = 0, weather_records_inserted: int = 0) -> Dict[str, Any]:
        if measurements_inserted > 0:
            self.processed_cities += 1
            self.measurements_inserted += measurements_inserted
        if weather_records_inserted > 0:
            self.weather_cities[city] = {
                "total_inserted": weather_records_inserted
            }
        return self._calculate_progress()

    def add_error(self, city: str, error_type: str, error_message: str) -> Dict[str, Any]:
        self.errors.append({
            "city": city,
            "type": error_type,
            "message": error_message
        })
        return self._calculate_progress()

    def get_final_result(self) -> Dict[str, Any]:
        return self._calculate_progress() 