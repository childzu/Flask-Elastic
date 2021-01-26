from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask.json import jsonify
from elasticsearch import Elasticsearch

es = Elasticsearch('127.0.0.1', port=9200)
bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/search')
def search():
    keyword = request.args.get('q')

    body = {
        "query": {
            "multi_match": {
                "query": keyword,
                "fields": ["firstName", "lastName", "email"]
            }
        }
    }

    res = es.search(index="customer", doc_type="_doc", body=body)
    customers = []
    for hit in res['hits']['hits']:
        beer = hit['_source']
        customers.append(beer)

    return jsonify(customers)