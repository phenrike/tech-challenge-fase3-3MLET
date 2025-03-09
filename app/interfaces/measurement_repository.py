# app/interfaces/measurement_repository.py
from abc import ABC, abstractmethod

class MeasurementRepository(ABC):
    @abstractmethod
    def get_measurements(self, sensor_id: int, datetime_from: str, datetime_to: str):
        pass
