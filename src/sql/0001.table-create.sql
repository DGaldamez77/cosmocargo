CREATE SCHEMA cosmocargo;
ALTER SCHEMA cosmocargo OWNER TO cosmocargo_admin;

GRANT USAGE ON SCHEMA cosmocargo TO cosmocargo_admin;
GRANT USAGE ON SCHEMA cosmocargo TO cosmocargo_service;
GRANT USAGE ON SCHEMA cosmocargo TO cosmocargo_readonly;
GRANT USAGE ON SCHEMA cosmocargo TO cosmocargo_readwrite;


CREATE FUNCTION cosmocargo.table_changed() RETURNS TRIGGER
    LANGUAGE plpgsql
AS
$$
BEGIN
    IF NEW.* IS DISTINCT FROM OLD.* THEN
        NEW.updated := current_timestamp;
        IF NEW.UPDATED_BY IS NULL THEN
            NEW.updated_by := current_user;
        END IF;
    END IF;
    RETURN NEW;
END;
$$;


CREATE TYPE cosmocargo.wind_direction AS ENUM ('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW');


CREATE TABLE cosmocargo.shipment_status
(
    shipment_status_id            SERIAL
        CONSTRAINT shipment_status_pk
            PRIMARY KEY,
    name                    VARCHAR NOT NULL,
    active                  BOOLEAN NOT NULL         DEFAULT TRUE,
    created                 TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    created_by              VARCHAR NOT NULL         DEFAULT CURRENT_USER,
    updated                 TIMESTAMP WITH TIME ZONE,
    updated_by              VARCHAR
);

ALTER TABLE cosmocargo.shipment_status
    owner to cosmocargo_admin;

CREATE UNIQUE INDEX shipment_status_shipment_statu_id_uindex 
    ON cosmocargo.shipment_status (shipment_status_id);

CREATE UNIQUE INDEX shipment_status_name_uindex 
    ON cosmocargo.shipment_status (name);

GRANT ALL ON cosmocargo.shipment_status TO cosmocargo_readwrite;
GRANT SELECT ON cosmocargo.shipment_status TO cosmocargo_readonly;

CREATE TRIGGER shipment_status_u
    BEFORE UPDATE
    ON cosmocargo.shipment_status
    FOR EACH ROW
EXECUTE PROCEDURE cosmocargo.table_changed();

GRANT ALL ON SEQUENCE cosmocargo.shipment_status_shipment_status_id_seq TO cosmocargo_readwrite;


CREATE TABLE cosmocargo.precipitation_kind
(
    precipitation_kind_id            SERIAL
        CONSTRAINT precipitation_kind_pk
            PRIMARY KEY,
    name                    VARCHAR NOT null,
    active                  BOOLEAN NOT NULL         DEFAULT TRUE,
    created                 TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    created_by              VARCHAR NOT NULL         DEFAULT CURRENT_USER,
    updated                 TIMESTAMP WITH TIME ZONE,
    updated_by              VARCHAR
);

ALTER TABLE cosmocargo.precipitation_kind
    owner to cosmocargo_admin;

CREATE UNIQUE INDEX precipitation_kind_shipment_statu_id_uindex 
    ON cosmocargo.precipitation_kind (precipitation_kind_id);

CREATE UNIQUE INDEX precipitation_kind_name_uindex 
    ON cosmocargo.precipitation_kind (name);

GRANT ALL ON cosmocargo.precipitation_kind TO cosmocargo_readwrite;
GRANT SELECT ON cosmocargo.precipitation_kind TO cosmocargo_readonly;

CREATE TRIGGER precipitation_kind_u
    BEFORE UPDATE
    ON cosmocargo.precipitation_kind
    FOR EACH ROW
EXECUTE PROCEDURE cosmocargo.table_changed();

GRANT ALL ON SEQUENCE cosmocargo.precipitation_kind_precipitation_kind_id_seq TO cosmocargo_readwrite;


CREATE TABLE cosmocargo.solar_system
(
    solar_system_id            SERIAL
        CONSTRAINT solar_system_pk
            PRIMARY KEY,
    name                    VARCHAR NOT null,
    active                  BOOLEAN NOT NULL         DEFAULT TRUE,
    created                 TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    created_by              VARCHAR NOT NULL         DEFAULT CURRENT_USER,
    updated                 TIMESTAMP WITH TIME ZONE,
    updated_by              VARCHAR
);

ALTER TABLE cosmocargo.solar_system
    owner to cosmocargo_admin;

CREATE UNIQUE INDEX solar_system_shipment_statu_id_uindex 
    ON cosmocargo.solar_system (solar_system_id);

CREATE UNIQUE INDEX solar_system_name_uindex 
    ON cosmocargo.solar_system (name);

GRANT ALL ON cosmocargo.solar_system TO cosmocargo_readwrite;
GRANT SELECT ON cosmocargo.solar_system TO cosmocargo_readonly;

CREATE TRIGGER solar_system_u
    BEFORE UPDATE
    ON cosmocargo.solar_system
    FOR EACH ROW
EXECUTE PROCEDURE cosmocargo.table_changed();

GRANT ALL ON SEQUENCE cosmocargo.solar_system_solar_system_id_seq TO cosmocargo_readwrite;


CREATE TABLE cosmocargo.planet
(
    planet_id            SERIAL
        CONSTRAINT planet_pk
            PRIMARY KEY,
    name                    VARCHAR NOT null,
    active                  BOOLEAN NOT NULL         DEFAULT TRUE,
    created                 TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    created_by              VARCHAR NOT NULL         DEFAULT CURRENT_USER,
    updated                 TIMESTAMP WITH TIME ZONE,
    updated_by              VARCHAR
);

ALTER TABLE cosmocargo.planet
    owner to cosmocargo_admin;

CREATE UNIQUE INDEX planet_shipment_statu_id_uindex 
    ON cosmocargo.planet (planet_id);

CREATE UNIQUE INDEX planet_name_uindex 
    ON cosmocargo.planet (name);

GRANT ALL ON cosmocargo.planet TO cosmocargo_readwrite;
GRANT SELECT ON cosmocargo.planet TO cosmocargo_readonly;

CREATE TRIGGER planet_u
    BEFORE UPDATE
    ON cosmocargo.planet
    FOR EACH ROW
EXECUTE PROCEDURE cosmocargo.table_changed();

GRANT ALL ON SEQUENCE cosmocargo.planet_planet_id_seq TO cosmocargo_readwrite;


CREATE TABLE cosmocargo.country
(
    country_id            SERIAL
        CONSTRAINT country_pk
            PRIMARY KEY,
    name                    VARCHAR NOT null,
    active                  BOOLEAN NOT NULL         DEFAULT TRUE,
    created                 TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    created_by              VARCHAR NOT NULL         DEFAULT CURRENT_USER,
    updated                 TIMESTAMP WITH TIME ZONE,
    updated_by              VARCHAR
);

ALTER TABLE cosmocargo.country
    owner to cosmocargo_admin;

CREATE UNIQUE INDEX country_shipment_statu_id_uindex 
    ON cosmocargo.country (country_id);

CREATE UNIQUE INDEX country_name_uindex 
    ON cosmocargo.country (name);

GRANT ALL ON cosmocargo.country TO cosmocargo_readwrite;
GRANT SELECT ON cosmocargo.country TO cosmocargo_readonly;

CREATE TRIGGER country_u
    BEFORE UPDATE
    ON cosmocargo.country
    FOR EACH ROW
EXECUTE PROCEDURE cosmocargo.table_changed();

GRANT ALL ON SEQUENCE cosmocargo.country_country_id_seq TO cosmocargo_readwrite;


CREATE TABLE cosmocargo.shipment
(
    shipment_id            SERIAL
        CONSTRAINT topic_pk
            PRIMARY KEY,
    shipment_time           TIMESTAMP  WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    weight_kg               NUMERIC(10, 2) NOT NULL DEFAULT 0,
    volume_m3               NUMERIC(10, 3) NOT NULL DEFAULT 0,
    eta_min                 INT NOT NULL DEFAULT 0,
    shipment_status_id                INT
        CONSTRAINT shipment_status_shipment_status_id_fk
            REFERENCES cosmocargo.shipment_status,
    forecast_origin_wind_velocity_mph NUMERIC(10, 2) NOT NULL DEFAULT 0,
    forecast_origin_wind_direction cosmocargo.wind_direction NOT NULL DEFAULT 'N',
    forecast_origin_precipitation_chance NUMERIC(10, 2) NOT NULL DEFAULT 0,
    forecast_origin_precipitation_kind_id INT
        CONSTRAINT precipitation_kind_precipitation_kind_id_fk
            REFERENCES cosmocargo.precipitation_kind,
    origin_solar_system_id INT
        CONSTRAINT solar_system_solar_system_id_fk
            REFERENCES cosmocargo.solar_system,
    origin_planet_id INT
        CONSTRAINT planet_planet_id_fk
            REFERENCES cosmocargo.planet,
    origin_country_id INT
        CONSTRAINT country_country_id_fk
            REFERENCES cosmocargo.country,
    origin_address VARCHAR NOT NULL,
    destination_solar_system_id INT
        CONSTRAINT solar_system_solar_system_id_fk_2
            REFERENCES cosmocargo.solar_system,
    destination_planet_id INT
        CONSTRAINT planet_planet_id_fk_2
            REFERENCES cosmocargo.planet,
    destination_country_id INT
        CONSTRAINT country_country_id_fk_2
            REFERENCES cosmocargo.country,
    destination_address VARCHAR NOT NULL,
    shipment_hash VARCHAR NOT NULL,
    active                  BOOLEAN NOT NULL         DEFAULT TRUE,
    created                 TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    created_by              VARCHAR NOT NULL         DEFAULT CURRENT_USER,
    updated                 TIMESTAMP WITH TIME ZONE,
    updated_by              VARCHAR
);

ALTER TABLE cosmocargo.shipment
    owner to cosmocargo_admin;

CREATE UNIQUE INDEX shipment_shipment_id_uindex 
    ON cosmocargo.shipment (shipment_id);

CREATE UNIQUE INDEX shipment_hash_uindex 
    ON cosmocargo.shipment (shipment_hash);

GRANT ALL ON cosmocargo.shipment TO cosmocargo_readwrite;
GRANT SELECT ON cosmocargo.shipment TO cosmocargo_readonly;

CREATE TRIGGER shipment_u
    BEFORE UPDATE
    ON cosmocargo.shipment
    FOR EACH ROW
EXECUTE PROCEDURE cosmocargo.table_changed();

GRANT ALL ON SEQUENCE cosmocargo.shipment_shipment_id_seq TO cosmocargo_readwrite;


GRANT cosmocargo_readwrite TO cosmocargo_service;