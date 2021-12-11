from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.sparta  #client.디비이름


wizards = db.wizards.find({}, {'_id': False})

for wizard in wizards:
    print(wizard)


