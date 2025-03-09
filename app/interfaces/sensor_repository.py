from abc import ABC, abstractmethod

class SensorRepository(ABC):
    @abstractmethod
    def get_pm25_sensors_from_chile(self):
        pass