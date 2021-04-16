from . import restaurants
from . import products
from . import categories
from . import orders
from . import tables
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
        ids = str(ObjectId())
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
            "id": ids

        }

        floors = [{
            "restaurant":ids,
            "floorName":floorName,
            "tables":[],
            "permanent":False
        },{
            "restaurant":ids,
            "floorName":floorName,
            "tables":[],
            "permanent":False
        }]

        tables.insert_many(floors)

        
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
            orders.insert_one({self.restaurant:[]})
    def get(self):
        l = [x for x in orders.find({self.restaurant:{"$exists":True}}, {"_id": 0})]
        print(l)
        return l[0][self.restaurant]

    def add(self, products, details):
        order_id = str(ObjectId())
        if orders.find({self.restaurant: {"$exists":True}}).limit(1).count() == 1:
            order = {
                'id':order_id,
                'products':products, #this will be an array of objects
                'details':details #this will be an object with 3 fields
            }
            res = orders.update({self.restaurant:{"$exists":True}}, {"$push":{self.restaurant:order}})
            print(res)
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



class Table:
    def __init__(self, restaurant):
        self.restaurant = restaurant
    def addFloor(self,floorName=None):
        floorName = floorName if floorName != None else ""
        floor = {
            "restaurant":self.restaurant,
            "floorName":floorName,
            "tables":[],
            "permanent":False,
            "id":str(ObjectId())
        }
        restaurants.update_one({"id":self.restaurant}, {"$set":{"floors":restaurants.find({"id":self.restaurant})[0]["floors"]+1}})
        tables.insert_one(floor)
        return {"status":"OK","message":"New floor has been added to this restaurant."}
    
    def addTable(self, floor, table):
        tableT = {
            "table":str(ObjectId()),
            "name":table['name'],
            "location":table['location'],
            "bookedTill":None
            
        }

        tables.update_one({"id":floor}, {"$push":{"tables":tableT}})
        return {"status":"OK", "message":"table has been added to floor"}


    def reserveTable(self, floor, table, ticks):
        tables.update_one({'id':floor, 'restaurant':self.restaurant, "tables.table":table}, {"$set":{"tables.$.bookedTill":ticks}})
        return {"status":"OK", "message":"table has been added to floor"}

    def getAll(self):
        return tables.find({"restaurant":self.restaurant}, {"_id":0})



# THIS IS A COMMENT AND IS MADE BY RITESH.

