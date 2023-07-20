from flask import Flask, jsonify, request
import sqlite3
import queries

app = Flask(__name__)

def execute_query(query, params=()):
    with sqlite3.connect('sensors.db', check_same_thread = False) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return {"message": "Internal server error"}, 500


def make_response(data):
    if isinstance(data, tuple):  
        return jsonify(data[0]), data[1] # Error
    else:
        return jsonify(data)


@app.route('/sensors/<int:sensor_id>', methods = ['GET'])
def get_sensor(sensor_id):
    data = execute_query(queries.query_by_sensor_id, (sensor_id,))
    return make_response(data)


#Get all sensors recent values from Office
@app.route('/sensors/<string:city>', methods = ['GET'])
def get_all_sensor_office(city):
    data = execute_query(queries.query_by_city, (city,))
    return make_response(data)


#Get all sensors recent values from Office and Building
@app.route('/sensors/<string:city>/<string:building>', methods = ['GET'])
def get_all_sensor_building(city, building):
    data = execute_query(queries.query_by_building, (city, building))
    return make_response(data)


#Get all sensors recent values from Office and Building
@app.route('/sensors/<string:city>/<string:building>/<string:room>', methods = ['GET'])
def get_all_sensor_room(city, building, room):
    data = execute_query(queries.query_by_room, (city, building, room))
    return make_response(data)


#Get all sensors recent values 
@app.route('/sensors', methods = ['GET', 'POST'])
def get_all_sensor():
    if request.method == 'GET':
        data = execute_query(queries.query_all_sensors)
        return make_response(data)
        
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


if __name__ == '__main__':
    app.run(debug = True)
