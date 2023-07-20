from flask import Flask, jsonify, request
import sqlite3
import queries

app = Flask(__name__)

# Recent info Sensor_id
@app.route('/sensors/<int:sensor_id>', methods = ['GET'])
def get_sensor(sensor_id):
    print(f"sensor id: {sensor_id}")
    conn = sqlite3.connect('sensors.db', check_same_thread = False)
    cursor = conn.cursor()
    cursor.execute(queries.query_by_sensor_id, (sensor_id,))
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    conn.close()

    json_data = []
    for row in rows:
        json_data.append(dict(zip(columns, row)))

    print(json_data)
    return jsonify(json_data)


#Get all sensors recent values 
@app.route('/sensors', methods = ['GET', 'POST'])
def get_all_sensor():
    if request.method == 'GET':
        conn = sqlite3.connect('sensors.db', check_same_thread = False)
        cursor = conn.cursor()
        cursor.execute(queries.query_all_sensors)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        conn.close()

        json_data = []
        for row in rows:
            json_data.append(dict(zip(columns, row)))

        print(json_data)
        return jsonify(json_data)
    elif request.method == 'POST':
        
        data = request.get_json()
        
        conn = sqlite3.connect('sensors.db', check_same_thread = False)
        cursor = conn.cursor()

        sensor_name = data['name']
        sensor_type = data['type']
        sensor_office = data['office']
        sensor_building = data['building']
        sensor_room = data['room']
        sensor_units = data['units']

        #handle if exest sensore with the same name:
        cursor.execute("SELECT * FROM sensors WHERE name = ?", (sensor_name,))
        rows = cursor.fetchall()
        if(len(rows) != 0):
            return jsonify({"message": "Exist sensor with the same name"}), 409 
        

        cursor.execute(queries.query_insert_sensor, (sensor_name, sensor_type, sensor_office, sensor_building, sensor_room, sensor_units))
        conn.commit()
        conn.close()

        return jsonify({"message": "Sensor data successfully inserted."}), 200


#Get all sensors recent values from Office
@app.route('/sensors/<string:city>', methods = ['GET'])
def get_all_sensor_office(city):
    conn = sqlite3.connect('sensors.db', check_same_thread = False)
    cursor = conn.cursor()
    cursor.execute(queries.query_by_city, (city,))
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    conn.close()

    json_data = []
    for row in rows:
        json_data.append(dict(zip(columns, row)))

    print(json_data)
    return jsonify(json_data)


#Get all sensors recent values from Office and Building
@app.route('/sensors/<string:city>/<string:building>', methods = ['GET'])
def get_all_sensor_building(city, building):
    conn = sqlite3.connect('sensors.db', check_same_thread = False)
    cursor = conn.cursor()
    cursor.execute(queries.query_by_building, (city, building))
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    conn.close()

    json_data = []
    for row in rows:
        json_data.append(dict(zip(columns, row)))

    print(json_data)    

    return jsonify(json_data)


#Get all sensors recent values from Office and Building
@app.route('/sensors/<string:city>/<string:building>/<string:room>', methods = ['GET'])
def get_all_sensor_room(city, building, room):
    conn = sqlite3.connect('sensors.db', check_same_thread = False)
    cursor = conn.cursor()
    cursor.execute(queries.query_by_room, (city, building, room))
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    conn.close()

    json_data = []
    for row in rows:
        json_data.append(dict(zip(columns, row)))

    print(json_data)      

    return jsonify(json_data)

if __name__ == '__main__':
    app.run(debug = True)
