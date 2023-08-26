from config import DB_CONNECTION_STRING
from model import *
from bson import ObjectId

# MongoDB driver
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(DB_CONNECTION_STRING)
database = client.TodoList

async def fetch_one(collection, id):
    obj_id = ObjectId(id)
    document = await database[collection].find_one({"_id": obj_id})
    return document

async def fetch_user(username):
    document = await database['user'].find_one({"username": username})
    return document

async def fetch_all(collection):
    documents = []
    cursor = database[collection].find({})
    async for document in cursor:
        if collection == "user":
            document = User(**document)
        elif collection == "grouplist":
            document = GroupList(**document)
        elif collection == "group":
            document = Group(**document)
        documents.append(document)
    return documents

async def create(collection, document):
    result = await database[collection].insert_one(document)
    return result

async def update(collection, id, data):
    obj_id = ObjectId(id)
    items = data.items
    updated_items = []
    for item in items:
        updated_items.append(dict(item))
    data.items = updated_items
    print(data)
    await database[collection].update_one({"_id":obj_id}, {"$set": dict(data)})
    document = await database[collection].find_one({"_id":obj_id})
    return document

async def remove(collection, id):
    obj_id = ObjectId(id)
    response = await database[collection].delete_one({"_id":obj_id})
    return True