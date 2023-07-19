from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/sensors/<sensor_id>', methods = ['GET'])
def get_sensor():
    sensor_id = request.args.get('id')
    # TODO
    return jsonify(sensor_id)

"""
@app.route('/sensors/<sensor_id>', methods = ['GET'])
def get_sensor(sensor_id):
    return jsonify(sensor_id)
"""

if __name__ == '__main__':
    app.run()