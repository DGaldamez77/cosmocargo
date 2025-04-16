import psycopg2, datetime, os
from util import hash

def add_shipment(conn: psycopg2.extensions.connection, shipment: dict):
    try:
        cur = conn.cursor()

        shipment_hash = hash.create_sha256_hash(str(shipment))                 

        query = """INSERT INTO cosmocargo.shipment (shipment_time, weight_kg, volume_m3, eta_min, shipment_status_id, 
        forecast_origin_wind_velocity_mph, forecast_origin_wind_direction, forecast_origin_precipitation_chance, 
        forecast_origin_precipitation_kind_id, origin_solar_system_id, origin_planet_id, origin_country_id, origin_address, 
        destination_solar_system_id, destination_planet_id, destination_country_id, destination_address, shipment_hash) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        datetime_object = datetime.datetime.fromtimestamp(shipment["time"])
        shipment_time = datetime_object.strftime("%Y-%m-%d %H:%M:%S")

        cur.execute(query, (shipment_time, shipment["weightKg"], shipment["volumeM3"], shipment["etaMin"], shipment["shipment_status_id"], 
                            shipment["forecastOriginWindVelocityMph"], shipment["forecastOriginWindDirection"], shipment["forecastOriginPrecipitationChance"],
                            shipment["forecast_orogin_precipitation_kind_id"], shipment["origin_solar_system_id"], shipment["origin_planet_id"], shipment["origin_country_id"], 
                            shipment["originAddress"], shipment["destination_solar_system_id"], shipment["destination_planet_id"], shipment["destination_country_id"], 
                            shipment["destinationAddress"], shipment_hash))

        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error inserting shipment: ", error)
        if conn: 
            conn.rollback()
        return error
    
    finally:
        if cur: 
            cur.close()

def get_or_create(conn: psycopg2.extensions.connection, table_name: str, value: str):
    try:
        cur = conn.cursor()

        # check first if row exists
        query = f"SELECT {table_name}_id FROM cosmocargo.{table_name} WHERE name = '{value}'" 
        cur.execute(query)

        row = cur.fetchone()
        if row != None:
            return row[0]

        # does not exist... add it to table and return its ID        
        query = f"INSERT INTO cosmocargo.{table_name} (name) VALUES (%s) RETURNING {table_name}_id"
        cur.execute(query, (value,))

        # retrieve ID
        row = cur.fetchone()
        if row != None:
            return row[0]
        
        conn.commit()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error inserting {table_name}: ", error)
        if conn: 
            conn.rollback()
        return error
    
    finally:
        if cur: 
            cur.close()

def write_to_db(shipments: list):
    conn = psycopg2.connect(
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT"),
    )

    metrics = {
        "success": 0,
        "fail": 0
    }

    for shipment in shipments:
        print(shipment)
        shipment["shipment_status_id"] = get_or_create(conn, "shipment_status", shipment["status"])    
        shipment["forecast_orogin_precipitation_kind_id"] = get_or_create(conn, "precipitation_kind", shipment["forecastOriginPrecipitationKind"])
        shipment["origin_solar_system_id"] = get_or_create(conn, "solar_system", shipment["originSolarSystem"])    
        shipment["origin_planet_id"] = get_or_create(conn, "planet", shipment["originPlanet"])
        shipment["origin_country_id"] = get_or_create(conn, "country", shipment["originCountry"])
        shipment["destination_solar_system_id"] = get_or_create(conn, "solar_system", shipment["destinationSolarSystem"])    
        shipment["destination_planet_id"] = get_or_create(conn, "planet", shipment["destinationPlanet"])
        shipment["destination_country_id"] = get_or_create(conn, "country", shipment["destinationCountry"])

        err = add_shipment(conn, shipment)   
        if err != None:
            metrics["fail"] += 1
            print("write failed ", shipment)
        else:
            metrics["success"] += 1

    print(f"\n=============================================")
    print(f"processing completed.")
    print(f"Total processed {len(shipments)}, success {metrics['success']}, fail {metrics['fail']}")
    print(f"=============================================")
