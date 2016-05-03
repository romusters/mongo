def test():
	from pymongo import MongoClient
	import json
	client = MongoClient()
	client = MongoClient('localhost', 27017)
	client = MongoClient('mongodb://localhost:27017/')

	db = client.database
	db_tweets = db.tweets
	print(db.collection_names())
	print db["usrC"]
	clear(db_tweets)
	clear(db["userA"])

	tweets = ["tweet 1", "tweet 2"]
	for tweet in tweets:
		db_tweets.insert_one({"tweets": tweet})

	users = ["userA", "userB"]

	dict = {}
	for user in users:
		check_user(db, user)

		for tweet in db_tweets.find():
			print tweet
			db[user].insert_one(tweet)

	from bson.objectid import ObjectId
	id = '5728b5fbc3dc0b18eb931bb6'
	db["userA"].update({'_id': ObjectId(id)}, {'$set' : {'labels' : "anton"}})

	for e in db["userA"].find():
		print e

def add_user(db, user):
	db[user]

def check_user(db, user):
	if user not in db.collection_names():
		add_user()

def main():
	from pymongo import MongoClient
	import json
	client = MongoClient()
	client = MongoClient('localhost', 27017)
	client = MongoClient('mongodb://localhost:27017/')

	db = client.test_database
	collection = db.test_collection


	database = db.labels
	clear(database)
	users = ['robert', 'anton']
	for u in users:
		insert_user(database, u)

	id = 1
	new_label = 'a'

	cp_labels = None
	for e in database.find({'user':'robert'}):
		cp_labels = e['labels']
		print cp_labels
		doc = [id, new_label]
		cp_labels.append(doc)
		print cp_labels

	database.update({'user': 'robert'}, {'$set' : {'labels' : str(cp_labels)}})
	for e in database.find({'user':'robert'}):
		print e['labels']
	# print collection.find_one()
	# from bson.objectid import ObjectId
	# id = '57277d4ac3dc0b23dae93729'
	# document = collection.find_one({'_id': ObjectId(str(id))})
	# print document
	# collection.update({'_id': ObjectId(str(id))}, {'$set' : {'test' : 'test'}})
	# document = collection.find_one({'_id': ObjectId(str(id))})
	# print document

def clear(db):
	db.delete_many({})

def insert_user(database, user):
	database.insert({ "user" : user, "labels" : []})

def insert(db):
	from bson.json_util import loads
	j = loads('[{"foo": [1, 2]}, {"bar": {"hello": "world"}}, {"code": {"$scope": {}, "$code": "function x() { return 1; }"}}, {"bin": {"$type": "00", "$binary": "AQIDBA=="}}]')
	for line in j:
		db.test_collection.insert(line)


if __name__ == '__main__':
	#main()
	test()