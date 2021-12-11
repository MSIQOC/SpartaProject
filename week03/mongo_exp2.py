from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.sparta  #client.디비이름

toystory = db.movies.find_one({'title': '월-E'})

for movie in db.movies.find():
    if movie['point'] == toystory['point'] and toystory['title'] != '월-E':
        #print(movie['point'])
        movie['point'] = 0
        print(movie['point'])
        db.movies.update_one({'title': toystory['title']}, {"$set": {'point': 0}})

for movie in db.movies.find():
    if movie['point'] == toystory['point']:
        print(movie['point'], movie['title'])


#print(toystory['point'])