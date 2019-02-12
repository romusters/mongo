from pymongo import MongoClient
import json
from bson.objectid import ObjectId
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

class mongo():
	def __init__(self):
		self.client = MongoClient()
		self.client = MongoClient('localhost', 27017)
		self.client = MongoClient('mongodb://localhost:27017/')
		self.db = self.client.database

	def check_user(self, user):
		if user not in self.db.collection_names():
			logger.info("populating user")
			self.populate_user(user)

	def addagreement(self, id, user, agreement):
		self.check_user(user)
		self.db[user].update({'_id': ObjectId(id)}, {'$set' : {'agreement' : str(agreement)}})


	def addlabel(self, id, user, label):
		self.check_user(user)
		self.db[user].update({'_id': ObjectId(id)}, {'$set' : {'label' : str(label)}})

	def populate_user(self, user):
		self.db.create_collection(user)
		for tweet in self.db['tweets'].find():
			self.db[user].insert(tweet)

	def get_tweet(self, user):
		data = self.db[user].find({'label': {'$exists': False}})[0]
		return data['tweets'], str(data['_id'])




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
