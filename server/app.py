#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():

    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    response = make_response(
        bakeries_serialized,
        200
    )
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()
    bakery_serialized = bakery.to_dict()

    response = make_response(
        bakery_serialized,
        200
    )
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    
    response = make_response(
        baked_goods_by_price_serialized,
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()

    response = make_response(
        most_expensive_serialized,
        200
    )
    return response

@app.route('/baked_goods', methods=['GET', 'POST'])
def create_baked_good():
    if request.method == 'POST':
        # Retrieve data from the request form
        name = request.form.get('name')
        price = request.form.get('price')
        bakery_id = request.form.get('bakery_id')  # Assuming you have a field for bakery_id in the form

        # Create a new BakedGood object and add it to the database
        baked_good = BakedGood(name=name, price=price, bakery_id=bakery_id)
        db.session.add(baked_good)
        db.session.commit()

        # Create a custom response with the newly created baked good's data as JSON
        baked_good_data = {
            "id": baked_good.id,
            "name": baked_good.name,
            "price": baked_good.price,
            "bakery_id": baked_good.bakery_id
        }

        response = make_response(jsonify(baked_good_data), 201)  # 201 Created status code
        return response

    # Handle GET requests to retrieve baked goods (you can customize this part as needed)
    baked_goods = BakedGood.query.all()
    baked_goods_list = [{"id": baked_good.id, "name": baked_good.name, "price": baked_good.price} for baked_good in baked_goods]

    response = make_response(jsonify(baked_goods_list))
    return response



@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get(id)

    if bakery is None:
        return jsonify({"message": "Bakery not found"}), 404  # Custom status code for "Not Found"

    if request.method == 'PATCH':
        # Retrieve data from the request form
        new_name = request.form.get('name')

        # Update the bakery's name in the database
        bakery.name = new_name
        db.session.commit()

        # Return the updated bakery's data as JSON
        bakery_data = {
            "id": bakery.id,
            "name": bakery.name,
            "created_at": bakery.created_at,
            "updated_at": bakery.updated_at
        }

        response = make_response(jsonify(bakery_data))
        return response

    # Handle GET requests to retrieve bakery data (you can customize this part as needed)
    bakery_data = {
        "id": bakery.id,
        "name": bakery.name,
        "created_at": bakery.created_at,
        "updated_at": bakery.updated_at
    }

    response = make_response(jsonify(bakery_data))
    return response


@app.route('/baked_goods/<int:id>', methods=['GET', 'DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)

    if baked_good is None:
        return jsonify({"message": "Baked good not found"}), 404  # Custom status code for "Not Found"

    if request.method == 'DELETE':
        # Delete the baked good from the database
        db.session.delete(baked_good)
        db.session.commit()

        # Return a JSON message confirming the deletion
        response_data = {"message": f"Baked good with ID {id} has been deleted."}
        response = make_response(jsonify(response_data))
        return response

    # Handle GET requests to retrieve baked good data (you can customize this part as needed)
    baked_good_data = {
        "id": baked_good.id,
        "name": baked_good.name,
        "price": baked_good.price,
        "created_at": baked_good.created_at,
        "updated_at": baked_good.updated_at,
        "bakery_id": baked_good.bakery_id
    }

    response = make_response(jsonify(baked_good_data))
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
