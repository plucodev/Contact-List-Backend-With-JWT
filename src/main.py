"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Person, Contact
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/person', methods=['POST', 'GET'])
def handle_person():
    """
    Create person and retrieve all persons
    """

    # POST request
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)

        user1 = Person(name=body['name'], email=body['email'], address=body['address'], phone=body['phone'])
        db.session.add(user1)
        db.session.commit()
        return "ok", 200

    # GET request
    if request.method == 'GET':
        all_people = Person.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))
        return jsonify(all_people), 200

    return "Invalid Method", 404
@app.route('/contact', methods=['POST', 'GET'])
def handle_contact():
    """
    Create person and retrieve all persons
    """

    # POST request
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)

        user1 = Contact(name=body['name'], email=body['email'], address=body['address'], phone=body['phone'])
        db.session.add(user1)
        db.session.commit()
        return "ok", 200

    # GET request
    if request.method == 'GET':
        all_people = Contact.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))
        return jsonify(all_people), 200

    return "Invalid Method", 404

@app.route('/person/<int:person_id>', methods=['PUT', 'GET', 'DELETE'])
def get_single_person(person_id):
    """
    Single person
    """

    # PUT request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        user1 = Person.query.get(person_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)

        if "name" in body:
            user1.name = body["name"]
        if "email" in body:
            user1.email = body["email"]
        if "address" in body:
            user1.address = body["address"]
        if "phone" in body:
            user1.phone = body["phone"]
        db.session.commit()

        return jsonify(user1.serialize()), 200

    # GET request
    if request.method == 'GET':
        user1 = Person.query.get(person_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)
        return jsonify(user1.serialize()), 200

    # DELETE request
    if request.method == 'DELETE':
        user1 = Person.query.get(person_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)
        db.session.delete(user1)
        return "ok", 200

    return "Invalid Method", 404


@app.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "hello": "world"
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is exercuted
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
