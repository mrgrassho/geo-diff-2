from os import environ
from os.path import join, dirname, isfile
from flask import Flask, request, send_file, abort, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from json import JSONEncoder
from bson import ObjectId

class JSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return JSONEncoder.default(self, o)


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__, static_url_path='/static')
app.config["MONGO_URI"] = environ.get("MONGO_URI")
app.config["DIR_TILES"] = environ.get("DIR_TILES")
app.json_encoder = JSONEncoder
mongo = PyMongo(app)
cors = CORS(app)


@app.route('/<filter_name>/<date>/<z>/<y>/<x>', methods=['GET', 'POST'])
def tiles(filter_name, date, z, y, x):
    api_token = request.args.get('key', type=str)
    auth_user = mongo.db.users.find_one({"api_token": api_token})
    if (auth_user is not None):
        filename = join(app.config["DIR_TILES"], filter_name, date, z, y, f"{x}")
        if isfile(filename):
            return send_file(filename)
    abort(404)


@app.route('/filters', methods=['GET', 'POST'])
def filters():
    api_token = request.headers.get('Authorization')
    auth_user = mongo.db.users.find_one({"api_token": api_token})
    if (auth_user is not None):
        app.logger.info('%s succesfully login', auth_user['name'])    
        filters = mongo.db.filters.find({})
        return jsonify([i for i in filters])
    else:
        abort(404)


@app.route('/dates', methods=['GET', 'POST'])
def dates():
    api_token = request.headers.get('Authorization')
    filter_name = request.args.get('filter', type=str)
    auth_user = mongo.db.users.find_one({"api_token": api_token})
    if (auth_user is not None):
        app.logger.info('%s succesfully login', auth_user['name'])
        if (filter_name is not None):
            dates = mongo.db.geo_index.find({'filterName': filter_name})
        else:
            dates = mongo.db.geo_index.find({})
        return jsonify([date for date in dates])
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8080)