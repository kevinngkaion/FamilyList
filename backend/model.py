from typing import Annotated, List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from serializer import PydanticObjectId

class User(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias='_id')
    username: str
    email: EmailStr
    fname: str
    lname: str
    is_active: bool = True

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "johndoe@gmail.com",
                "fname": "John",
                "lname": "Doe",
                "is_active": "true"
            }
        }
        
class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    fname: str
    lname: str
    is_active: bool = True
    
class UpdateUser(BaseModel):
    username: str
    email: EmailStr
    fname: str
    lname: str
    is_active: bool = True
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: str or None = None
    
class UserInDB(User):
    hashed_password: str
    
class Group(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias='_id')
    name: str
    admin: PydanticObjectId
    users: List[PydanticObjectId]
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Wu Tang Clan",
                "admin": "id#1",
                "users": [
                    'id#1',
                    'id#2'
                ]
            }
        }
        
class CreateGroup(BaseModel):
    name: str
    admin: PydanticObjectId
    users: List[PydanticObjectId]
    
class Item(BaseModel):
    name: str
    description: Optional[str]
    quantity: int = 1
    is_purchased: bool = False
    
class GroupList(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias='_id')
    name: str
    group: PydanticObjectId
    items: List[Item]
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Wu Tang Clan",
                "admin": "id#1",
                "users": [
                    'id#1',
                    'id#2'
                ]
            }
        }
        
class CreateGroupList(BaseModel):
    name: str
    group: PydanticObjectId
    items: List[Item]
    
class UserLogin(BaseModel):
    username: str
    password: str
    class Config:
        json_schema_extra = {
            "Login Demo": {
                "username": "johndoe",
                "password": "letmein123"
            }
        }