from . import restaurants
from . import products
from . import categories
from . import orders
from bson.objectid import ObjectId
from bson.json_util import dumps
import json


def printSomething():
    for x in restaurants.find({}):
        print(x)


class Restaurant:
    def __init__(self, restaurantName=None, email=None, password=None):
        if restaurantName != None:
            self.name = restaurantName
            self.email = email
            self.password = password
            self.add(restaurantName, email, password)
        else:
            pass

    def add(self, restaurantName, email, password):
        itemsToAdd = {
            "name": restaurantName,
            "email": email,
            "password": password,
            "floors": 2,
            "hours": {
                "sunday": [0000, 2359],
                "monday": [0000, 2359],
                "tuesday": [0000, 2359],
                "wednesday": [0000, 2359],
                "thursday": [0000, 2359],
                "friday": [0000, 2359],
                "saturday": [0000, 2359],
            },
            "id": str(ObjectId())

        }

        restaurants.insert_one(itemsToAdd)

    def getAll(self):
        l = [x for x in restaurants.find({}, {"_id": 0})]
        return l

    def getAuthenticated(self, email, password):
        all = restaurants.find_one({
            "email": email,
            "password": password,
        }, {"_id": 0})

        return all

    def getOne(self, email):
        val = restaurants.find_one({
            "email": email
        }, {"_id": 0})

        return val


class Order:
    def __init__(self, restaurant):
        self.restaurant = restaurant
        if orders.find({self.restaurant: {"$exists": True}}).limit(1).count() == 0:
            orders.insert_one({

            })
    def get(self):
        l = [x for x in orders.find({self.restaurant:{"$exists":True}}, {"_id": 0})]
        return l[0][self.restaurant]

    def add(self, products, details):
        order_id = str(ObjectId())
        if orders.find({self.restaurant: {"$exists":True}}).limit(1).count() == 1:
            order = {
                'id':order_id,
                'products':products, #this will be an array of objects
                'details':details #this will be an object with 3 fields
            }
            id = orders.find({self.restaurant:{"$exists":True}})[0]["_id"]

            t = orders.update({"_id": id}, {"$push":order})
            print(t)
            return True
        return False

class Product:
    def __init__(self, restaurant, category):
        self.restaurant = restaurant
        self.category = category
        pass

    def add(self, name, price, variants, image):
        product = {
            'name': name,
            'price': price,
            'category': self.category,
            'restaurant': self.restaurant,
            'variants': variants,
            'is_active': 'true',
            'image': image,
            'id': str(ObjectId())
        }
        products.insert_one(product)
        return {"status": "OK", "message": "New Product has been added Successfully"}

    def getAll(self):
        return products.find({}, {'_id': 0})

    def get(self):
        return products.find({"restaurant": self.restaurant, "category": self.category}, {'_id': 0})

    def delete(self):
        return products.delete_many({"restaurant": self.restaurant, "category": self.category})

    def deleteOne(self, product):
        print("Entered -----------------")
        return products.delete_one({"id": product})


class Category:
    def __init__(self, restaurant):
        self.restaurant = restaurant
        pass

    def add(self, name):
        category = {
            'restaurant': self.restaurant,
            'category': name,
            'id': str(ObjectId())
        }
        categories.insert_one(category)
        return {'status': 'OK', 'message': 'Category has been successfully added'}

    def getAll(self):
        return categories.find({'restaurant': self.restaurant}, {'_id': 0})

    def getAllFromRestaurant(self, restaurant):
        return categories.find({'restaurant': restaurant}, {'_id': 0})

    def deleteOne(self, id):
        categories.delete_one({"id": id, 'restaurant': self.restaurant})
        return {'status': 'OK', 'message': 'Category has been successfully deleted'}

    def deleteAll(self):
        categories.delete_many({})
        return {'status': 'OK', 'message': 'All categories has been successfully deleted'}

# THIS IS A COMMENT AND IS MADE BY RITESH.

