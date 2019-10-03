#!/usr/bin/env python3
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
import jinja2 as j2

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = True

app.config['MONGO_DBNAME'] = "timeplan"
app.config['MONGO_URI'] = "mongodb+srv://timeplan:vanskeligpassord@cluster0-qhhx4.mongodb.net/admin?retryWrites=true&w=majority"
timeplaner = PyMongo(app).db.timeplaner

j2_env = j2.Environment(loader=j2.FileSystemLoader('templates'), trim_blocks=True)

@app.route('/', methods=['GET'])
def index():
    template = j2_env.get_template('timeplan.jinja2')
    rendered_template = template.render()
    return rendered_template

'''@app.route('/api/timeplan', methods=['GET', 'POST', 'PUT', 'DELETE'])
def timeplanApi():
    if request.method == 'POST':

    elif request.method == 'PUT':

    elif request.method == 'DELETE':

    else:'''


@app.route('/api/timeplaner', methods=['GET'])
def getTimeplaner():
    resp = {}
    for timeplan in timeplaner.find():
        resp[timeplan['navn']] = timeplan['_id']
    resp.status_code = 200
    return resp

@app.route('/api/timeplan', methods=['GET'])
def getTimeplan():
    resp = jsonify(timeplaner.find_one({ '_id': request.json['_id'] }))
    resp.status_code = 200
    return resp

@app.errorhandler(404)
def err404route(error=None):
    template = j2_env.get_template('err.jinja2', err="404 Not Found")
    rendered_template = template.render()
    return rendered_template

