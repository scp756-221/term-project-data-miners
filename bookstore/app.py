"""
SFU CMPT 756 Term-Project BookStore application
"""

# Standard library modules
import csv
import logging
import os
import sys
import uuid

# Installed packages
from flask import Blueprint
from flask import Flask
from flask import request


# The path to the file (CSV format) containing the sample data
DB_PATH = '/data/book.csv'

# The application

app = Flask(__name__)

bp = Blueprint('app', __name__)

database = {}


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
    response = {
        "Count": len(database),
        "Items":
            [{'Author': value[0], 'BookTitle': value[1], 'book_id': id}
             for id, value in database.items()]
    }
    return response


@bp.route('/<book_id>', methods=['GET'])
def get_book(book_id):
    global database
    if book_id in database:
        value = database[book_id]
        response = {
            "Count": 1,
            "Items":
                [{'Author': value[0],
                  'BookTitle': value[1],
                  'book_id': book_id}]
        }
    else:
        response = {
            "Count": 0,
            "Items": []
        }
        return app.make_response((response, 404))
    return response


@bp.route('/', methods=['POST'])
def create_book():
    global database
    try:
        content = request.get_json()
        # print(f">>>>>>>>>>>>>>>>content:{content}")
        Author = content['Author']
        BookTitle = content['BookTitle']
    except Exception:
        return app.make_response(
            ({"Message": "Error reading arguments"}, 400)
            )
    book_id = str(uuid.uuid4())
    database[book_id] = (Author, BookTitle)
    response = {
        "book_id": book_id
    }
    return response


@bp.route('/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    global database
    if book_id in database:
        del database[book_id]
    else:
        response = {
            "Count": 0,
            "Items": []
        }
        return app.make_response((response, 404))
    return {}

@bp.route('/shutdown', methods=['GET'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return {}


app.register_blueprint(bp, url_prefix='/api/v1/book/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("missing port arg 1")
        sys.exit(-1)

    load_db()
    p = int(sys.argv[1])
    app.run(host='0.0.0.0', port=p, threaded=True)
