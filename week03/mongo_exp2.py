from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.sparta

target_movie = db.movies.find_one({'title': '월-E'})
target_star = target_movie['point']
allofthem = list(db.movies.find({'point': 0}))
for a in allofthem:
    print(a)

# db.movies.updateMany({'point': target_star, 'title': {'$ne': '월-E'}}, {'$set': {'point': 0}})
#
# for a in allofthem:
#     print(a)