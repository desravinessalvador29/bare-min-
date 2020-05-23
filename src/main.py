"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import datetime
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db
from models import Product, Order

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



@app.route('/product', methods=['POST', 'GET'])
def handle_product():
 
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'name' not in body:
            raise APIException('You need to specify the name', status_code=400)
        if 'price' not in body:
            raise APIException('You need to specify the price', status_code=400)
        if 'description' not in body:
            raise APIException('You need to specify the description', status_code=400)

        product1 = Product(name=body['name'], price=body['price'], description=body['description'])
        db.session.add(product1)
        db.session.commit()
        return "ok", 200


    if request.method == 'GET':
        all_product = Product.query.all()
        all_product = list(map(lambda x: x.serialize(), all_product))
        return jsonify(all_product), 200

    return "Invalid Method", 404


@app.route('/product/<int:product_id>', methods=['PUT', 'GET', 'DELETE'])
def get_single_product(product_id):

    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        product1 = Product.query.get(product_id)
        if product1 is None:
            raise APIException('Product not found', status_code=404)

        if "name" in body:
            product1.name = body["name"]
        if "price" in body:
            product1.price = body["price"]
        if "description" in body:
            product1.description = body["description"]
        db.session.commit()

        return jsonify(product1.serialize()), 200

    if request.method == 'GET':
        product1 = Product.query.get(product_id)
        if product1 is None:
            raise APIException('Product not found', status_code=404)
        return jsonify(product1.serialize()), 200

    if request.method == 'DELETE':
        product1 = Product.query.get(product_id)
        if product1 is None:
            raise APIException('Product not found', status_code=404)
        db.session.delete(product1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404


@app.route('/order', methods=['POST', 'GET'])
def handle_order():
 
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'first_name' not in body:
            raise APIException('You need to specify the first name', status_code=400)
        if 'last_name' not in body:
            raise APIException('You need to specify the last name', status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)
        if 'phone' not in body:
            raise APIException('You need to specify the phone', status_code=400)
        if 'address' not in body:
            raise APIException('You need to specify the address', status_code=400)
        if 'city' not in body:
            raise APIException('You need to specify the city', status_code=400)
        if 'state' not in body:
            raise APIException('You need to specify the state', status_code=400)
        if 'country' not in body:
            raise APIException('You need to specify the country', status_code=400)
        if 'zip_code' not in body:
            raise APIException('You need to specify the zip code', status_code=400)
        if 'card_number' not in body:
            raise APIException('You need to specify the card number', status_code=400)
        if 'card_expiration_date' not in body:
            raise APIException('You need to specify the card expiration date', status_code=400)
        if 'card_cvv' not in body:
            raise APIException('You need to specify the card cvv', status_code=400)

        order1 = Order(first_name=body['first_name'], last_name=body['last_name'], email=body['email'], phone=body['phone'], address=body['address'], city=body['city'], state=body['state'], country=body['country'], zip_code=body['zip_code'], card_number=body['card_number'], card_expiration_date=body['card_expiration_date'], card_cvv=body['card_cvv'])
        db.session.add(order1)
        db.session.commit()
        return "ok", 200

    if request.method == 'GET':
        all_orders = Order.query.all()
        all_orders = list(map(lambda x: x.serialize(), all_orders))
        return jsonify(all_orders), 200

    return "Invalid Method", 404


@app.route('/order/<int:order_id>', methods=['GET', 'DELETE'])
def get_single_order(order_id):


    if request.method == 'GET':
        order1 = Order.query.get(order_id)
        if order1 is None:
            raise APIException('Order not found', status_code=404)
        return jsonify(order1.serialize()), 200

    if request.method == 'DELETE':
        order1 = Order.query.get(order_id)
        if order1 is None:
            raise APIException('Order not found', status_code=404)
        db.session.delete(order1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
