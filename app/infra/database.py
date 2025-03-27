import os
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        self.cur = self.conn.cursor()

    def check_measurement_exists(self, id_sensor: int, dt_date_from: datetime, dt_date_to: datetime):
        query = """
            SELECT COUNT(*) FROM public.tbl_measurements 
            WHERE id_sensor = %s 
            AND dt_date_from = %s 
            AND dt_date_to = %s
        """
        self.cur.execute(query, (id_sensor, dt_date_from, dt_date_to))
        return self.cur.fetchone()[0] > 0

    def check_weather_history_exists(self, ds_city: str, dt_date: datetime):
        query = """
            SELECT COUNT(*) FROM public.tbl_weather_history 
            WHERE ds_city = %s 
            AND dt_date = %s
        """
        self.cur.execute(query, (ds_city, dt_date))
        return self.cur.fetchone()[0] > 0

    def insert_measurement(self, id_sensor: int, ds_city: str, dt_date_from: datetime, dt_date_to: datetime, qt_pm25: float):
        if not self.check_measurement_exists(id_sensor, dt_date_from, dt_date_to):
            query = """
                INSERT INTO public.tbl_measurements 
                (id_sensor, ds_city, dt_date_from, dt_date_to, qt_pm25)
                VALUES (%s, %s, %s, %s, %s)
            """
            self.cur.execute(query, (id_sensor, ds_city, dt_date_from, dt_date_to, qt_pm25))

    def insert_weather_history(self, ds_city: str, dt_date: datetime, qt_avg_humidity: float, 
                             qt_avg_temp_c: float, qt_avg_vis_km: float, qt_max_wind_kph: float,
                             qt_total_precip_mm: float, qt_pressure_mb: float):
        if not self.check_weather_history_exists(ds_city, dt_date):
            query = """
                INSERT INTO public.tbl_weather_history 
                (ds_city, dt_date, qt_avg_humidity, qt_avg_temp_c, qt_avg_vis_km, 
                 qt_max_wind_kph, qt_total_precip_mm, qt_pressure_mb)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cur.execute(query, (ds_city, dt_date, qt_avg_humidity, qt_avg_temp_c, 
                                   qt_avg_vis_km, qt_max_wind_kph, qt_total_precip_mm, 
                                   qt_pressure_mb))

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def __del__(self):
        if hasattr(self, 'cur'):
            self.cur.close()
        if hasattr(self, 'conn'):
            self.conn.close() 