query_by_sensor_id = """
                    SELECT office, building, room, name, type, value
                    FROM 
                    (
                        SELECT *
                        FROM sensors s
                        WHERE id = ?
                    ) AS s
                    JOIN
                        sensor_values AS val 
                    ON s.id = val.sensor
                    ORDER BY timestamp DESC
                    LIMIT 1;
                    """

query_all_sensors = """
                    SELECT office, building, room, name, type, recent_value AS value
                    FROM 
                        sensors AS s
                    JOIN
                    (    
                        SELECT sensor, MAX(timestamp) AS recent_time, value as recent_value
                        FROM sensor_values
                        GROUP BY sensor
                    )AS val
                    ON s.id = val.sensor
                    """

query_by_city = """
                SELECT office, building, room, name, type, recent_value AS value
                FROM 
                (
                    SELECT * 
                    FROM sensors
                    WHERE office = ?
                ) AS s
                JOIN
                (    
                    SELECT sensor, MAX(timestamp) AS recent_time, value as recent_value
                    FROM sensor_values
                    GROUP BY sensor
                ) AS val 
                ON s.id = val.sensor
                """

query_by_building = """
                    SELECT office, building, room, name, type, recent_value AS value
                    FROM 
                    (
                        SELECT * 
                        FROM sensors
                        WHERE office = ? AND building = ?
                    ) AS s
                    JOIN
                    (    
                        SELECT sensor, MAX(timestamp) AS recent_time, value as recent_value
                        FROM sensor_values
                        GROUP BY sensor
                    ) AS val 
                    ON s.id = val.sensor
                    """

query_by_room = """
                SELECT s.office, s.building, s.room, s.name, s.type, sv.value AS recent_value
                FROM 
                (
                    SELECT * 
                    FROM sensors
                    WHERE office = ? AND building = ? AND room = ?
                ) AS s
                JOIN
                (
                    SELECT sensor, MAX(timestamp) AS max_timestamp, value as recent_value
                    FROM sensor_values
                    GROUP BY sensor
                ) AS max_val
                ON s.id = max_val.sensor
                JOIN
                    sensor_values AS sv
                ON sv.sensor = max_val.sensor AND sv.timestamp = max_val.max_timestamp
                """

query_insert_sensor = """
                        INSERT INTO sensors (name, type, office, building, room, units) 
                        VALUES (?, ?, ?, ?, ?, ?)
                      """

query_by_name = """
                SELECT * FROM sensors WHERE name = ?
                """
