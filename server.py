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
        if 'name' in json and 'email' in json and 'password' in json :
            name = json['name']
            email = json['email']
            password = json['password']
            r = mr.Restaurant(name, email, password)
            
            return jsonify({'status':'OK', 'message':'Restaurant Created Successfully.', 'id': "Some ID Will Come here"})
        else:
            return jsonify({'status':'Failed', 'message':'Restaurant could not be created please include name, email and password fields in request body'})

    def get(self):
        json = request.get_json()
        
        if json:
            if 'email' in json and 'password' in json:
                res = mr.Restaurant().getAuthenticated(json['email'], json['password'])
                return jsonify({"login":"false"}) if res == None else jsonify(res)
        return mr.Restaurant().getAll()


class Product(Resource):
    def post(self):
        json = request.get_json()
        if 'email' in json and 'product' not in json:
            res = mr.Restaurant().addCategory(json['email'], json['category'])
            return jsonify({"status":"OK","message":"Product created successfully"})
        elif 'email' in json and 'product' in json:
            res = mr.Restaurant().addProduct(json['email'], json['category'],json['product'])
            return jsonify({"status":"OK","message":"Product created successfully"})
        return jsonify({"status":"Failed", "message":"Product cannot be added."})
    
    def get(self):
        res = mr.Restaurant().getCategories('kishore@smooth.tech')
        return jsonify(res[0]["categories"])
    
api.add_resource(Restaurant, '/restaurant/')
api.add_resource(Product, '/product/')

if __name__ == '__main__':
    app.run()
