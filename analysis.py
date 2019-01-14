import pymongo
import json


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["test"]
mycol = mydb["reply"]
print(mycol.find_one())
for x in mycol.find({},{ "_id": 0, "name": 1, "member": 1 }):

