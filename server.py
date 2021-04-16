from flask import Flask, request, Response, jsonify
from flask_restful import Resource, Api
from bson.json_util import dumps

from models.restaurant import printSomething
import models.restaurant as mr

app = Flask(__name__)
api = Api(app)


class Restaurant(Resource):
    def post(self):
        json = request.get_json()
        print(json)
        if 'name' in json and 'email' in json and 'password' in json:
            name = json['name']
            email = json['email']
            password = json['password']
            r = mr.Restaurant(name, email, password)


            return jsonify(
                {'status': 'OK', 'message': 'Restaurant Created Successfully.', 'id': "Some ID Will Come here"})
        else:
            return jsonify({'status': 'Failed',
                            'message': 'Restaurant could not be created please include name, email and password fields in request body'})

    def get(self):
        json = request.get_json()

        if json:
            if 'email' in json and 'password' in json:
                res = mr.Restaurant().getAuthenticated(json['email'], json['password'])
                return jsonify({"login": "false"}) if res == None else jsonify(res)
        return jsonify(mr.Restaurant().getAll())


class Product(Resource):
    def post(self):
        json = request.get_json()
        json = json if json != None else {}
        if 'name' in json and 'price' and 'category' in json and 'restaurant' in json and 'variants' in json and 'image' in json:
            return mr.Product(json['restaurant'], json['category']).add(json['name'], json['price'], json['variants'],
                                                                        json['image'])
        return {"status": "Failed", "message": "Please provide 'name, price and category' fields"}

    def get(self):
        json = request.get_json()
        json = json if json != None else {}
        if 'category' in json:
            return list(mr.Product(json['restaurant'], json['category']).get())
        return {"status": "Failed", "message": "Please provide 'category' to get the products for"}

    def delete(self):
        json = request.get_json()
        json = json if json != None else {}
        if 'product' in json:
            mr.Product(json['restaurant'], json['category']).deleteOne(json['product'])
            return {"status": "OK", "message": "Product Deleted Successfully"}
        return {"status": "Failed", "message": "Unable to delete the product."}

    def patch(self):
        json = request.get_json()
        json = json if json != None else {}
        if 'product' in json:
            mr.Product(json['restaurant'], json['category']).activate(json['product'])
            return {"status": "OK", "message": "Product Updated Successfully"}
        return {"status": "Failed", "message": "Unable to Update the product."}


class Category(Resource):
    def post(self):
        json = request.get_json()
        json = json if json != None else {}
        if 'name' not in json and 'restaurant' not in json:
            return {'status': 'Failed', 'message': 'Please include the \'name\' and \'restaurant\' in the request'}
        else:
            res = mr.Category(json['restaurant']).add(json['name'])
            return res

    def get(self):
        json = request.get_json()
        json = json if json != None else {}
        if 'restaurant' in json:
            return list(mr.Category(json['restaurant']).getAll())
        return {'status': 'Failed', 'message': 'Please include the \'restaurant\' in the request'}

    def delete(self):
        json = request.get_json()
        json = json if json != None else {}
        if 'category_id' in json:
            mr.Product(json['restaurant'], json['category_id']).delete()
            return mr.Category(json['restaurant']).deleteOne(json['category_id'])
        else:
            return mr.Category(json['restaurant']).deleteAll()


class Table(Resource):
    def get(self):
        json = request.get_json()
        json = json if json != None else {}
        if 'restaurant' in json:
            return list(mr.Table(json['restaurant']).getAll())
        return jsonify({"message": "Will Start working on Tables soon"})
    def post(self):
        json = request.get_json()
        json = json if json != None else {}
        if 'restaurant' in json and 'floor_flag' in json:
            return mr.Table(json['restaurant']).addFloor()
        elif 'restaurant' in json and 'table' in json and 'floor' in json:
            return mr.Table(json['restaurant']).addTable(json['floor'], json.get('table',''))
        return {"status":"Failed"}

    def put(self):
        json = request.get_json()
        json = json if json != None else {}
        if 'restaurant' in json and 'table' in json and 'floor' in json and 'ticks' in json:
            return mr.Table(json['restaurant']).reserveTable(json['floor'], json['table'], json['ticks'])




# Restaurant -> ORDER_ID -> tray (products(product_name, category_name, price, qty) order_details(hst, subtotal, tip, total))
class Orders(Resource):
    def post(self):
        json = request.get_json()
        json = json if json != None else {}
        print(json)
        print("----")
        if 'restaurant' in json and 'products' in json and 'details' in json:
            restaurant = json['restaurant']
            products = json['products']  # this is an array of products

            result = map(lambda x: 'name' in x and 'price' in x and 'qty' in x and 'image' in x, products)
            print(result)
            if False in result:
                return {'message': 'Please include name, price, qty in all products'}
       
                

            details = json['details']
            order = mr.Order(restaurant).add(products,details)
            return {'message':'You are right '+str(order)}


        return {'message':'please include \'restaurant\' in /orders/ request'}
    def get(self):
        json = request.get_json()
        json = json if json != None else {}

        if 'restaurant' in json:
            restaurant = json['restaurant']

            order = mr.Order(restaurant).get()
            return jsonify(order)

        return {'message': 'please include \'restaurant\' in /orders/ request'}


api.add_resource(Restaurant, '/restaurant/')
api.add_resource(Product, '/product/')
api.add_resource(Category, '/category/')
api.add_resource(Orders, '/orders/')
api.add_resource(Table, '/table/')

if __name__ == '__main__':
    app.run()
