-- DROP SCHEMA public;

DROP SCHEMA IF EXISTS public CASCADE;

CREATE SCHEMA public AUTHORIZATION pg_database_owner;

-- DROP SEQUENCE public.tbl_measurements_id_measurements_seq;

CREATE SEQUENCE public.tbl_measurements_id_measurements_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

CREATE TABLE public.tbl_measurements (
	id integer NOT NULL DEFAULT nextval('public.tbl_measurements_id_measurements_seq'),
	id_sensor integer NOT NULL,
	ds_city varchar(250) NOT NULL,
	dt_date_from timestamp NOT NULL,
	dt_date_to timestamp NOT NULL,
	qt_pm25 numeric(10, 2) NOT NULL,
    CONSTRAINT pk_tbl_measurements PRIMARY KEY (id)
);

CREATE SEQUENCE public.tbl_weather_history_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

CREATE TABLE public.tbl_weather_history (
	id integer NOT NULL DEFAULT nextval('public.tbl_weather_history_id_seq'),
	ds_city varchar(250) NOT NULL,
	dt_date date NOT NULL,
	qt_avg_humidity numeric(10, 2) NOT NULL,
	qt_avg_temp_c numeric(10, 2) NOT NULL,
	qt_avg_vis_km numeric(10, 2) NOT NULL,
	qt_max_wind_kph numeric(10, 2) NOT NULL,
	qt_total_precip_mm numeric(10, 2) NOT NULL,
	qt_pressure_mb numeric(10, 2) NOT NULL,
    CONSTRAINT pk_tbl_weather_history PRIMARY KEY (id)
);