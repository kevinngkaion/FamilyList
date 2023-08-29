from config import DB_CONNECTION_STRING
from model import *
from bson import ObjectId
import asyncio

# MongoDB driver
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(DB_CONNECTION_STRING)
database = client.TodoList

async def fetch_one(collection, id):
    obj_id = ObjectId(id)
    document = await database[collection].find_one({"_id": obj_id})
    return document

async def fetch_base_user(user_id):
    user = await database['user'].find_one({"_id": user_id})
    if user:
        base_user = BaseUser(id=user['_id'], fname=user['fname'], lname=user['lname'])
        return base_user;
    return None

async def fetch_grouplist(id):
    obj_id = ObjectId(id)
    document = await database['grouplist'].find_one({"_id": obj_id})
    group_id = ObjectId(document['group'])
    group = await database['group'].find_one({"_id": group_id})
    admin_id = ObjectId(group['admin'])
    member_ids = [ObjectId(member_id) for member_id in group['members']]
    fetch_tasks = [fetch_base_user(member_id) for member_id in member_ids]
    group['admin'] = await fetch_base_user(admin_id)
    group['members'] = await asyncio.gather(*fetch_tasks)
    
    document['group'] = group
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