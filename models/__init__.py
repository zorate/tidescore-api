from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGODB_URI)
db = client[Config.DATABASE_NAME]

# Collections
users_collection = db['users']
lenders_collection = db['lenders']
scores_collection = db['scores']
consents_collection = db['consents']
transactions_collection = db['transactions']
employment_collection = db['employment']
guarantors_collection = db['guarantors']
api_requests_collection = db['api_requests']