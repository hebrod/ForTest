CREATE DATABASE "ForTest"
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

CREATE TABLE region_dim (
	id SERIAL PRIMARY KEY,
	region VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE datasource_dim (
	id SERIAL PRIMARY KEY,
	datasource VARCHAR(50) UNIQUE NOT NULL
);

CREATE EXTENSION postgis;

CREATE TABLE location_dim (
	id SERIAL PRIMARY KEY,
	location GEOGRAPHY(POINT, 4326) UNIQUE NOT NULL
);

CREATE TABLE time_dim (
	id SERIAL PRIMARY KEY,
	year INTEGER NOT NULL,
	month INTEGER NOT NULL,
	day INTEGER NOT NULL,
	hour INTEGER NOT NULL
);

CREATE TABLE facts (
	id SERIAL PRIMARY KEY,
	region INTEGER NOT NULL,
	datasource INTEGER NOT NULL,
	origin INTEGER NOT NULL,
	destination INTEGER NOT NULL,
	time INTEGER NOT NULL,
	events INTEGER NOT NULL,
	constraint fk_region 
    foreign key (region) 
    REFERENCES region_dim (id),
	constraint fk_datasource 
    foreign key (datasource) 
    REFERENCES datasource_dim (id),
	constraint fk_origin 
    foreign key (origin) 
    REFERENCES location_dim (id),
	constraint fk_destination 
    foreign key (destination) 
    REFERENCES location_dim (id),
	constraint fk_time 
    foreign key (time) 
    REFERENCES time_dim (id)
);