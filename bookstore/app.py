"""
SFU CMPT 756 Term-Project BookStore application
"""

# Standard library modules
import csv
import logging
import os
import sys
import uuid
import requests

# Installed packages
from flask import Blueprint
from flask import Flask
from flask import request
from flask import Response
from prometheus_flask_exporter import PrometheusMetrics

import simplejson as json

# The path to the file (CSV format) containing the sample data
DB_PATH = '/data/book.csv'

db = {
    "name": "http://cmpt756db:30002/api/v1/datastore",
    "endpoint": [
        "read",
        "write",
        "delete",
        "update",
        "readall"
    ]
}

# The application

app = Flask(__name__)

bp = Blueprint('app', __name__)

database = {}

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Book process')

def load_db():
    global database
    with open(DB_PATH, 'r') as inp:
        rdr = csv.reader(inp)
        next(rdr)  # Skip header line
        for author, booktitle, id in rdr:
            database[id] = (author, booktitle)

@bp.route('/', methods=['GET'])
def list_all():
    global database
    url = db['name'] + '/' + db['endpoint'][4]
    response = requests.post(
        url,
        json={"objtype": "book"})
    return (response.json())


@bp.route('/<book_id>', methods=['GET'])
def get_book(book_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(
            json.dumps({"error": "missing auth"}),
            status=401,
            mimetype='application/json')
    payload = {"objtype": "book", "objkey": book_id}
    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(url, params=payload)
    return (response.json())


@bp.route('/', methods=['POST'])
def create_book():
    global database
    try:
        content = request.get_json()
        Author = content['Author']
        BookTitle = content['BookTitle']
    except Exception:
        return app.make_response(
            ({"Message": "Error reading arguments"}, 400)
            )
    book_id = str(uuid.uuid4())
    url = db['name'] + '/' + db['endpoint'][1]
    response = requests.post(
        url,
        json={"objtype": "book",
              "Author": Author,
              "BookTitle": BookTitle,
              "book_id": book_id})
    return (response.json())


@bp.route('/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    url = db['name'] + '/' + db['endpoint'][2]

    response = requests.delete(url,
                               params={"objtype": "book", "objkey": book_id})
    return (response.json())


@bp.route('/<book_id>', methods=['PUT'])
def update(book_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}), status=401,
                        mimetype='application/json')
    try:
        content = request.get_json()
        author = content['Author']
        book_title = content['BookTitle']
    except Exception:
        return json.dumps({"message": "error reading arguments"})
    url = db['name'] + '/' + db['endpoint'][3]
    response = requests.put(
        url,
        params={"objtype": "book", "objkey": book_id},
        json={"Author": author, "BookTitle": book_title})
    return (response.json())


@bp.route('/shutdown', methods=['GET'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return {}

@bp.route('/health')
@metrics.do_not_track()
def health():
    return Response("", status=200, mimetype="application/json")


@bp.route('/readiness')
@metrics.do_not_track()
def readiness():
    return Response("", status=200, mimetype="application/json")

@bp.route('/booktest')
def booktest():
    return 'BOOK TEST RESPONSE'


app.register_blueprint(bp, url_prefix='/api/v1/book/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("missing port arg 1")
        sys.exit(-1)

    # load_db()
    p = int(sys.argv[1])
    app.run(host='0.0.0.0', port=p, threaded=True)
