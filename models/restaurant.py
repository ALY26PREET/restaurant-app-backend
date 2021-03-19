from . import restaurants
from bson.objectid import ObjectId
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
            "name":restaurantName, 
            "email":email, 
            "password":password,
            "floors":2,
            "hours":{
                "sunday":[0000, 2359],
                "monday":[0000, 2359],
                "tuesday":[0000, 2359],
                "wednesday":[0000, 2359],
                "thursday":[0000, 2359],
                "friday":[0000, 2359],
                "saturday":[0000, 2359],
            }, 
            "categories":{
                "Default":[]
            }   


        }

        restaurants.insert_one(itemsToAdd)


    def getAll(self):
        l = [x for x in restaurants.find({}, { "_id":0 })]
        return l

    def getAuthenticated(self, email, password):
        all = restaurants.find_one({
            "email":email,
            "password":password
        }, {"_id":0 })
       
        return all

    def getOne(self, email):
        val = restaurants.find_one({
            "email":email
        }, {"_id":0})

        return val
    def addCategory(self,email, category):
        restaurants.update_one({"email":email}, {"$set":{"categories."+category:[]}})
        return "DONE"
    def addProduct(self, email, category, product):
        print(email, category, product)
        product['id'] = str(ObjectId())
        restaurants.update_one({"email":email}, {"$push":{"categories."+category : product }})
        return "DONE"

    def getCategories(self, email):
        return restaurants.find({"email":email}, {"_id":0, "categories":1})

    def addTable(self, email, floorNum, tableID):
        pass



#THIS IS A COMMENT AND IS MADE BY RITESH. 

