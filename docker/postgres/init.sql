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
	id_sensor numeric(4) NOT NULL,
	ds_city varchar(250) NOT NULL,
	dt_date date NOT NULL,
	qt_pm25 numeric(3, 2) NULL,
    qt_avg_humidity numeric(2, 2) NULL,
    qt_avg_temp_c numeric(2, 2) NULL,
    qt_max_wind_kph numeric(3, 2) NULL,
    qt_total_precip_mm numeric(4, 2) NULL,
	pressure numeric(4, 1) NULL,
	visibility numeric(2) NULL,
    CONSTRAINT pk_tbl_measurements PRIMARY KEY (id)
);