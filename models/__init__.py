from pymongo import MongoClient
client = MongoClient()
db = client['restaurantbackenddb']

restaurants = db['restaurant']

