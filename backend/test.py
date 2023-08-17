from typing import Annotated, Any, Callable

from bson import ObjectId
from fastapi import FastAPI, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict, Field, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

from config import DB_CONNECTION_STRING
from model import Todo

# MongoDB driver
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(DB_CONNECTION_STRING)
database = client.TestDB
collection = database.test

# Based on https://docs.pydantic.dev/latest/usage/types/custom/#handling-third-party-types
class _ObjectIdPydanticAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
            cls,
            _source_type: Any,
            _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:

        def validate_from_str(id_: str) -> ObjectId:
            return ObjectId(id_)

        from_str_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_str_schema,
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance first before doing any further work
                    core_schema.is_instance_schema(ObjectId),
                    from_str_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: str(instance)
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
            cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        # Use the same schema that would be used for `str`
        return handler(core_schema.str_schema())


PydanticObjectId = Annotated[
    ObjectId, _ObjectIdPydanticAnnotation
]


class User(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias='_id')
    name: str
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Jane Doe",
            }
        }
        
class CreateUser(BaseModel):
    name: str

app = FastAPI()

@app.get("/")
async def get_root():
    todos = []
    cursor = collection.find({})
    async for document in cursor:
        todos.append(User(**document))
    return todos

@app.post("/user", response_model=User)
async def post_user(user:CreateUser):
    document = jsonable_encoder(user)
    print(document)
    new_student = await collection.insert_one(document)
    response = await collection.find_one({"_id": new_student.inserted_id})
    # response = await collection.insert_one(document)
    return response

@app.get("/user/{id}", response_model=User)
async def get_usr(id: str):
    response = await collection.find_one({"_id": ObjectId(id)})
    if response:
        return response
    raise HTTPException(404, f"there is no TODO item with this id {id}")


# Some usage examples

user1 = User(_id=ObjectId('64cca8a68efc81fc425aa864'), name='John Doe')
print(user1)
user2 = User(_id='64cca8a68efc81fc425aa864', name='John Doe')
assert user1 == user2  # Can use str and ObjectId interchangeably
