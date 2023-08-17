from config import DB_CONNECTION_STRING
from model import Todo, CreateTodo

# MongoDB driver
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(DB_CONNECTION_STRING)
database = client.TodoList
collection = database.todo

async def fetch_one_todo(id):
    from bson import ObjectId
    obj_id = ObjectId(id)
    document = await collection.find_one({"_id": obj_id})
    return document

async def fetch_all_todos():
    todos = []
    cursor = collection.find({})
    async for document in cursor:
        todos.append(Todo(**document))
    return todos

async def create_todo(todo):
    document = todo
    result = await collection.insert_one(document)
    return result

async def update_todo(title, desc):
    await collection.update_one({"title":title}, {"$set":{"description":desc}})
    document = await collection.find_one({"title":title})
    return document

async def remove_todo(title):
    await collection.delete_one({"title":title})
    return True