from typing import Annotated
from bson import ObjectId
from pydantic import BaseModel, Field
from serializer import PydanticObjectId

class Todo(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias='_id')
    title: str
    description: str
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "title": "Task 1",
                "description": "Feed the dogs"
            }
        }
        
class CreateTodo(BaseModel):
    title: str
    description: str
        
        
    # # id: Annotated[ObjectId, ObjectIdPydanticAnnotation(alias="_id")]
    # title: str
    # description: str
    


# kevin = Todo(id="", title="Kevin", description="Name")
# print(kevin)
# class Model(BaseModel):
#     id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
#     name: str = "Kevin"

# kevin = Model(id='64b7abdecf2160b649ab6085')
# print(type(kevin.id))
# print(Model(id='64b7abdecf2160b649ab6085').model_dump_json())
# print(Model(id=ObjectId()))
# print(Model.model_json_schema())
# try:
#     print(Model(id='foobar'))  # will error
# except Exception as error:
#     print(error)
    