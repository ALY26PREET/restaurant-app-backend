from pymongo import MongoClient
client = MongoClient()
db = client['restaurantbackenddb']
restaurants = db['restaurant']
products = db['products']
categories = db['categories']
orders = db['orders']
tables = db['tables']

