from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flask_app.auth import login_required
from flask_app.db import get_db
from elasticsearch import Elasticsearch

es = Elasticsearch('127.0.0.1', port=9200)
bp = Blueprint('cust', __name__, url_prefix='/cust')

@bp.route('/')
def index():
    res = es.search(
        index="customer", 
        doc_type="_doc",
        body={
            "query": {
                "match_all" : {}
            }
        }
    )
    customers = []
    for hit in res['hits']['hits']:
        beer = hit['_source']
        customers.append(beer)
    return render_template('customer/index.html', customers=customers)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        age = request.form['age']
        email = request.form['email']
        error = None

        if not firstName:
            error = 'First name is required.'
        
        if not lastName:
            error = 'Last name is required.'

        if not email:
            error = 'Email is required'

        if error is not None:
            flash(error)
        else:
            body = {
                'firstName': firstName,
                'lastName': lastName,
                'age': age,
                'email': email
            }
            result = es.index(index='customer', doc_type='_doc', body=body)
            return render_template('customer/detail.html', result = result)
    
    return render_template('customer/create.html')
