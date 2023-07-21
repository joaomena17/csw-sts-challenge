from flask import Flask, jsonify, request
import sqlite3
import queries
import gpt_integration as gpt

app = Flask(__name__)

def execute_query(query, params=()):
    with sqlite3.connect('sensors.db', check_same_thread = False) as conn:
        cursor = conn.cursor()
        try:
            if query.lstrip().upper().startswith('SELECT'):
                cursor.execute(query, params)
                rows = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, row)) for row in rows]
            else: # Delete Insert Update  
                return {"message": "Not allowed to modify the database"}, 403
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


#Get info by netural language query 
@app.route('/nlquery', methods = ['POST'])
def get_nlquery():
    data = request.get_json()

    if 'text' not in data:
        return jsonify({"message": "'text' field is required"}), 400
    
    text = data['text']
    query = gpt.generate_sql_query(text)

    data = execute_query(query)
    return make_response(data)


#Get all sensors recent values 
@app.route('/sensors', methods = ['GET', 'POST'])
def get_all_sensor():
    if request.method == 'GET':
        data = execute_query(queries.query_all_sensors)
        return make_response(data)
        
    elif request.method == 'POST':
        data = request.get_json()
        fields = ['name', 'type', 'office', 'building', 'room', 'units']

        missing_fields = [field for field in fields if field not in data or len(data[field]) == 0]
        print(missing_fields)
        if len(missing_fields) > 0:
            return jsonify({"message": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        with sqlite3.connect('sensors.db', check_same_thread = False) as conn:
            cursor = conn.cursor()

            cursor.execute(queries.query_by_name, (data['name'],))
            rows = cursor.fetchall()
            if rows:
                return jsonify({"message": "Exist sensor with the same name"}), 409 

            cursor.execute(queries.query_insert_sensor, (data['name'], data['type'], data['office'], data['building'], data['room'], data['units']))
            conn.commit()

        return jsonify({"message": "Added new sensor successfully"}), 200


if __name__ == '__main__':
    app.run(debug = True)
