import psycopg2, os

def get_shipments() -> list:
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get("DB_NAME"), #"cosmocargo",
            user=os.environ.get("DB_USER"), #"cosmocargo_service",
            password=os.environ.get("DB_PASSWORD"), #"cosmocargo",
            host=os.environ.get("DB_HOST"), #"localhost",
            port=os.environ.get("DB_PORT"), #"5432"
        )

        cur = conn.cursor()
        query = """
select  
    shipment_id,
    shipment_time,
    weight_kg,
    volume_m3,
    eta_min,
    ss.name as shipment_status,
    forecast_origin_wind_velocity_mph,
    forecast_origin_wind_direction,
    forecast_origin_precipitation_chance,
    fopk.name as forecast_origin_precipitation_kind,
    oss.name as origin_solar_system,
    op.name as origin_planet,
    oc.name as origin_country,
    origin_address,
    dss.name as destination_solar_system,
    dp.name as destination_planet,
    dc.name as destination_country,
    destination_address
from 
    cosmocargo.shipment s
        inner join cosmocargo.shipment_status ss 
            on s.shipment_status_id = ss.shipment_status_id
        inner join cosmocargo.precipitation_kind fopk 
            on s.forecast_origin_precipitation_kind_id = fopk.precipitation_kind_id
        inner join cosmocargo.solar_system oss 
            on s.origin_solar_system_id = oss.solar_system_id
        inner join cosmocargo.solar_system dss 
            on s.destination_solar_system_id = dss.solar_system_id
        inner join cosmocargo.planet op 
            on s.origin_planet_id = op.planet_id 
        inner join cosmocargo.planet dp 
            on s.destination_planet_id = dp.planet_id 
        inner join cosmocargo.country oc 
            on s.origin_country_id = oc.country_id
        inner join cosmocargo.country dc 
            on s.destination_country_id = dc.country_id        
order by 
    s.shipment_time desc, 
    s.shipment_id asc
"""

        cur.execute(query)
        rows = cur.fetchall()

        return rows

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return error
    
    finally:
        if cur: 
            cur.close()

def get_shipment(id: int) -> list:
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get("DB_NAME"), #"cosmocargo",
            user=os.environ.get("DB_USER"), #"cosmocargo_service",
            password=os.environ.get("DB_PASSWORD"), #"cosmocargo",
            host=os.environ.get("DB_HOST"), #"localhost",
            port=os.environ.get("DB_PORT"), #"5432"
        )

        cur = conn.cursor()
        query = """
select  
    shipment_id,
    shipment_time,
    weight_kg,
    volume_m3,
    eta_min,
    ss.name as shipment_status,
    forecast_origin_wind_velocity_mph,
    forecast_origin_wind_direction,
    forecast_origin_precipitation_chance,
    fopk.name as forecast_origin_precipitation_kind,
    oss.name as origin_solar_system,
    op.name as origin_planet,
    oc.name as origin_country,
    origin_address,
    dss.name as destination_solar_system,
    dp.name as destination_planet,
    dc.name as destination_country,
    destination_address
from 
    cosmocargo.shipment s
        inner join cosmocargo.shipment_status ss 
            on s.shipment_status_id = ss.shipment_status_id
        inner join cosmocargo.precipitation_kind fopk 
            on s.forecast_origin_precipitation_kind_id = fopk.precipitation_kind_id
        inner join cosmocargo.solar_system oss 
            on s.origin_solar_system_id = oss.solar_system_id
        inner join cosmocargo.solar_system dss 
            on s.destination_solar_system_id = dss.solar_system_id
        inner join cosmocargo.planet op 
            on s.origin_planet_id = op.planet_id 
        inner join cosmocargo.planet dp 
            on s.destination_planet_id = dp.planet_id 
        inner join cosmocargo.country oc 
            on s.origin_country_id = oc.country_id
        inner join cosmocargo.country dc 
            on s.destination_country_id = dc.country_id
where 
    s.shipment_id = %s
"""

        cur.execute(query, (id,))
        row = cur.fetchone()

        return row

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return error
    
    finally:
        if cur: 
            cur.close()

def update_shipment(id: int, f: list):
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get("DB_NAME"), #"cosmocargo",
            user=os.environ.get("DB_USER"), #"cosmocargo_service",
            password=os.environ.get("DB_PASSWORD"), #"cosmocargo",
            host=os.environ.get("DB_HOST"), #"localhost",
            port=os.environ.get("DB_PORT"), #"5432"
        )

        cur = conn.cursor()
        query = f"""
update 
    cosmocargo.shipment 
set 
    weight_kg = %s,
    volume_m3 = %s,
    eta_min = %s,
    shipment_status_id = %s,
    forecast_origin_wind_velocity_mph = %s,
    forecast_origin_wind_direction = %s,
    forecast_origin_precipitation_chance = %s,
    forecast_origin_precipitation_kind_id = %s,
    origin_solar_system_id = %s,
    origin_planet_id = %s,
    origin_country_id = %s,
    origin_address = %s,
    destination_solar_system_id = %s,
    destination_planet_id = %s,
    destination_country_id = %s,
    destination_address = %s
where 
    shipment_id = %s
"""

        cur.execute(query, (f["weight"], f["volume"], f["eta"], f["status"], f["fow_velocity"], f["fow_direction"], f["fop_chance"], f["fop_kind"], f["o_solar_system"], f["o_planet"], f["o_country"], f["o_address"], f["d_solar_system"], f["d_planet"], f["d_country"], f["d_address"], id))
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn:
            conn.rollback()
        return error
    
    finally:
        if cur: 
            cur.close()

def get_ref_data(table: str) -> list:
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get("DB_NAME"), #"cosmocargo",
            user=os.environ.get("DB_USER"), #"cosmocargo_service",
            password=os.environ.get("DB_PASSWORD"), #"cosmocargo",
            host=os.environ.get("DB_HOST"), #"localhost",
            port=os.environ.get("DB_PORT"), #"5432"
        )

        cur = conn.cursor()
        query = f"select {table}_id, name from cosmocargo.{table} where active = true order by 1 asc"

        cur.execute(query)
        rows = cur.fetchall()

        return rows

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return error
    
    finally:
        if cur: 
            cur.close()

