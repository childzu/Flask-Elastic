import os
from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flask_app.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    from . import cust
    app.register_blueprint(cust.bp)
    app.add_url_rule('/cust/', endpoint='index')

    from .api import customer
    app.register_blueprint(customer.bp)

    return app


# from flask import Flask, jsonify, request
# from elasticsearch import Elasticsearch

# app = Flask(__name__)
# es = Elasticsearch('127.0.0.1', port=9200)

# @app.route('/')
# def hello():
#     return 'Hello, World!'

# @app.route('/search', methods=['GET'])
# def search_request():
#     keyword = request.args.get('q')
#     res = es.search(
#         index="customer", 
#         doc_type="_doc",
#         body={
#             "query": {
#                 "multi_match" : {
#                     "query": keyword, 
#                     "fields": [
#                         "firstName", 
#                         "lastName"
#                     ] 
#                 }
#             }
#         }
#     )
#     return jsonify(res['hits']['hits'])
