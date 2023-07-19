from flask import Flask, request, jsonify,Response
from flask_cors import CORS
from pymongo import MongoClient
from bson import json_util
from bson import ObjectId
from bson.errors import InvalidId
import json

from dotenv import load_dotenv

import os
load_dotenv()

# client = MongoClient(os.getenv('MONGO_URI'))

# db = client['zesty_zomato']
# collection = db['menu-data']
# get all the dish data
# import json
# from flask import Response

# @app.route('/menu', methods=['GET'])
# def get_menu():
#     documents = list(collection.find())
#     json_documents = json.dumps(documents, default=json_util.default)
#     return Response(json_documents, mimetype='application/json')





def create_app():
    app = Flask(__name__)
    CORS(app)

    client = MongoClient(os.getenv('MONGO_URI'))

    db = client['zesty_zomato']
    collection = db['menu-data']
    # check if mongoDB connected
    try:
        # Access a collection to check the connection
        count = collection.count_documents({})
        print(f"MongoDB connected. Collection count: {count}")
    except ConnectionError as e:
        print(f"Failed to connect to MongoDB. Error: {str(e)}")


    @app.route('/menu', methods=['GET'])
    def get_menu():
        cursor_documents = collection.find()
        json_documents = []
        for document in cursor_documents:
            document['_id'] = str(document['_id'])
            json_documents.append(document)
        return jsonify(json_documents),200


    

    # add dish
    @app.route('/menu/add', methods=['POST'])
    def add_dish():
        dish = request.json
        # Validate dish data
        if 'dish_name' not in dish or 'price' not in dish or 'availability' not in dish or 'stock' not in dish or 'image' not in dish:
            return jsonify({"msg": "Please prived all fields!"}), 400

        # Insert the dish data into the MongoDB collection
        inserted_dish = collection.insert_one(dish)
        return jsonify({'msg':"dish added!"}),201


    # update dish availabilty
    @app.route("/menu/update/<string:id>", methods=['PUT'])
    def update_availability(id):
        # check if id is valid ObjectId
        if not is_valid_object_id(id):
            return ({'msg':'Invalid ObjectId!'}),400

        # check if document is present with this id
        document_present = collection.find_one({"_id":ObjectId(id)})
        if not document_present:
            return ({'msg':"No document found!"}),404

        updated_dish = request.json
        updated_dish['_id'] = ObjectId(id)
        collection.update_one({'_id': ObjectId(id)}, {'$set': updated_dish})
        response = {'msg': 'Dish updated successfully'}
        return jsonify(response)


    # delete one of the dish
    @app.route('/menu/delete/<id>', methods=['DELETE'])
    def delete_dish(id):
        if not is_valid_object_id(id):
            return jsonify({'msg':'Invalid ObjectId!'}),400

        # check if document is present with this id
        document_present = collection.find_one({"_id":ObjectId(id)})
        if not document_present:
            return jsonify({'msg':"No document found!"}),404

        collection.delete_one({'_id': ObjectId(id)})
        response = {'msg': 'Dish deleted successfully'}
        return jsonify(response)





    # ORDER'S Routes starts here.....
    orders_collection = db['orders']

    # get all orders route
    @app.route("/orders",methods=['GET'])
    def get_orders():
        documents = orders_collection.find()
        json_documents =[]
        for document in documents:
            document['_id'] = str(document['_id'])
            json_documents.append(document)
        return jsonify(json_documents),200

    # add order route
    @app.route("/orders/add/<string:id>",methods=['POST'])
    def add_order(id):
        order_datails = request.json
        obj = {**order_datails,'status':'recieved'}
        customer_name = request.json.get('customer_name',None)
        quantity = request.json.get('quantity', 0)
        if customer_name is None:
            return jsonify({'msg':"Customer name is missing!"}),400
        if quantity == 0:
            return jsonify({'msg':'Quantity is missing!'}),400
        orders_collection.insert_one(obj)
        return jsonify({'msg':"order added!"}),201


    # update the status of a order route (valid for admins)
    @app.route("/orders/update/<string:id>",methods=['PUT'])
    def change_status(id):
        if 'status' not in request.json:
            return {'msg':'Please enter a status of the order!'},400
        status = request.json['status'].lower()
        if status not in ['received', 'preparing','ready for pickup','delivered']:
            return {'msg':'Please enter valid status!'},400
        is_order_present = orders_collection.find_one({'_id':ObjectId(id)})
        if not is_order_present:
            return jsonify({'msg':"No order found!"}),404
        response = orders_collection.update_one({'_id':ObjectId(id)},{'$set':{'status':request.json['status']}})
        return jsonify({'msg':'Order updated successfully!'}),200



    # filter based on status 
    @app.route("/orders/<string:status>",methods=['GET'])
    def filter_order(status):
        if status not in ['received', 'preparing','ready for pickup','delivered','pending']:
            return {'msg':'Please enter valid status!'},400
        filtered_curser_orders= orders_collection.find({'status': status})
        # converting mongodb ObjectId() into simple string.
        filtered_json_orders = []
        for order in filtered_curser_orders:
            order['_id'] = str(order['_id'])
            filtered_json_orders.append(order)
        return jsonify(filtered_json_orders), 200

    return app


# checking valid id
def is_valid_object_id(id):
    try:
        ObjectId(id)
        return True
    except InvalidId:
        return False



# # add dish
# @app.route('/menu/add', methods=['POST'])
# def add_dish():
#     dish = request.json
#      # Validate dish data
#     if 'dish_name' not in dish or 'price' not in dish or 'availability' not in dish or 'stock' not in dish or 'image' not in dish:
#         return jsonify({"msg": "Please prived all fields!"}), 400

#     # Insert the dish data into the MongoDB collection
#     inserted_dish = collection.insert_one(dish)
#     return jsonify({'msg':"dish added"}),201


# # update dish availabilty
# @app.route("/menu/update/<id>", methods=['PUT'])
# def update_availability(id):
#     print("id is :",id)
#     updated_dish = request.json
#     updated_dish['_id'] = ObjectId(id)
#     collection.update_one({'_id': ObjectId(id)}, {'$set': updated_dish})
#     response = {'message': 'Dish updated successfully'}
#     return jsonify(response)


# # delete one of the dish
# @app.route('/menu/delete/<id>', methods=['DELETE'])
# def delete_dish(id):
#     collection.delete_one({'_id': ObjectId(id)})
#     response = {'message': 'Dish deleted successfully'}
#     return jsonify(response)





# # ORDER'S Routes starts here.....
# orders_collection = db['orders']

# # get all orders route
# @app.route("/orders",methods=['GET'])
# def orders():
#     documents = list(orders_collection.find())
#     json_documents = json.dumps(documents, default=json_util.default)
#     return Response(json_documents, mimetype='application/json')

# # add order route
# @app.route("/orders/add/<string:id>",methods=['POST'])
# def add_order(id):
#     order_datails = request.json
#     obj = {**order_datails,'status':'recieved'}
#     customer_name = request.json.get('customer_name',None)
#     quantity = request.json.get('quantity', 0)
#     if customer_name is None:
#         return jsonify({'msg':"Customer name is missing!"}),400
#     if quantity == 0:
#         return jsonify({'msg':'Quantity is missing!'}),400
#     orders_collection.insert_one(obj)
#     return jsonify({'msg':"order added!"}),201


# # update the status of a order route (valid for admins)
# @app.route("/orders/update/<string:id>",methods=['PUT'])
# def change_status(id):
#     if 'status' not in request.json:
#         return {'msg':'Please enter a status of the order!'},400
#     status = request.json['status'].lower()
#     if status not in ['received', 'preparing','ready for pickup','delivered']:
#         return {'msg':'Please enter valid status!'},400
#     is_order_present = orders_collection.find_one({'_id':ObjectId(id)})
#     if not is_order_present:
#         return jsonify({'msg':"No order found!"}),404
#     response = orders_collection.update_one({'_id':ObjectId(id)},{'$set':{'status':request.json['status']}})
#     return jsonify({'msg':'Order updated successfully!'}),200



# # filter based on status 
# @app.route("/orders/<string:status>",methods=['GET'])
# def filter_order(status):
#     if status not in ['received', 'preparing','ready for pickup','delivered','pending']:
#         return {'msg':'Please enter valid status!'},400
#     filtered_curser_orders= orders_collection.find({'status': status})
#     # converting mongodb ObjectId() into simple string.
#     filtered_json_orders = []
#     for order in filtered_curser_orders:
#         order['_id'] = str(order['_id'])
#         filtered_json_orders.append(order)
#     return jsonify(filtered_json_orders), 200



app = create_app()

if __name__ == "__main__":
    app.run(port=4000, debug=True)
