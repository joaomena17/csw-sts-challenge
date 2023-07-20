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
@app.route('/sensors/', methods = ['GET'])
def get_all_sensor():
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

#Get all sensors recent values from Office and Room
@app.route('/sensors/<string:city>/<string:room>', methods = ['GET'])
def get_all_sensor_room(city, room):
    conn = sqlite3.connect('sensors.db', check_same_thread = False)
    cursor = conn.cursor()
    cursor.execute(queries.query_by_room, (city, room))
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
