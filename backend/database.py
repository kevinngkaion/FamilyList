from config import DB_CONNECTION_STRING
from model import *
from bson import ObjectId
import asyncio
from pprint import pprint

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
        # if collection == "user":
        #     document = User(**document)
        # elif collection == "grouplist":
        #     document = GroupList(**document)
        # elif collection == "group":
        #     document = Group(**document)
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

async def update_list(id, data):
    collection = database['grouplist']
    obj_id = ObjectId(id)
    filter_criteria = {"_id": obj_id}
    array_filters = None
    if isinstance(data, CreateGroupList):
        updated_items = []
        for item in data.items:
            updated_items.append(dict(item))
        data.items = updated_items
        update_operation = {"$set": dict(data)}
    elif isinstance(data, Item):
        count_filter_criteria = {"_id": obj_id,
                       "items": {
                           "$elemMatch": {"name": data.name}
                       }}
        item_exists = await collection.count_documents(filter=count_filter_criteria)
        if not item_exists:
            grouplist = await collection.find_one({"_id": obj_id})
            grouplist['items'].append(dict(data))
            update_operation = {"$set": dict(grouplist)}
            await collection.update_one(filter_criteria, update_operation)
            document = await collection.find_one(filter_criteria)
            return document
        else:
            update_operation = {"$set": {"items.$[elem]": dict(data)}}
    elif isinstance(data, ListNameUpdate):
        update_operation = {"$set": {"name": data.name}}
    pprint(await collection.update_one(filter_criteria, update_operation, array_filters=array_filters))
    document = await collection.find_one({"_id": obj_id})
    return document
    