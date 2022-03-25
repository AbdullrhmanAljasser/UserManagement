from pymongo import MongoClient
import pymongo

_username = "userdatabase"
_password = "XJRVReNMPCXbvIWA"
_cluster = "usermanagement"
_database = "usermanagement"


# MongoDB Database
CONNECTION_STRING = f"mongodb+srv://{_username}:{_password}@{_cluster}.eob5c.mongodb.net/{_database}?retryWrites=true&w=majority"

db_client = MongoClient(CONNECTION_STRING)