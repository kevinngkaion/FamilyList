from typing import Union

from fastapi import FastAPI, HTTPException, Depends, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId
from passlib.context import CryptContext

from model import UserLogin

from config import ALLOWED_ORIGINS

from auth.auth import router, get_current_active_user

from datetime import timedelta, datetime, timezone


import json

app = FastAPI()
app.include_router(router)

from database import *

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.get("/")
def read_root(user: User = Depends(get_current_active_user)):
    return {"Name": "Kevin Ngkaion"}

@app.get("/user", tags=["user"])
async def get_users(response:Response, request:Request):
    data = await fetch_all("user")
    # response = Response(content=data)
    response.set_cookie(key="token", value="TestToken", httponly=True, secure=False, samesite="None")
    response.set_cookie(key="name", value="Kevin", httponly=False, secure=False, samesite="None")
    print(request.cookies.get("token"))
    return data

@app.get("/user/{id}", response_model=User, tags=["user"])
async def get_user_by_id(id: str, user: User = Depends(get_current_active_user)):
    response = await fetch_one('user', id)
    if response:
        return response
    raise HTTPException(404, f"there is no user with this ID {id}")

@app.put("/user/{id}", response_model=User, tags=["user"])
async def put_user(id:str, data:UpdateUser, user: User = Depends(get_current_active_user)):
    response = await update('user', id, data)
    if response:
        return response
    raise HTTPException(404, f"there is no user with this ID {id}")

@app.delete("/user/{id}", tags=["user"])
async def delete_user(id:str, user: User = Depends(get_current_active_user)):
    response = await remove('user', id)
    if response:
        return "Succesfully deleted a user!"
    raise HTTPException(404, f"there is no user with this ID {id}")

@app.get("/group", tags=["group"])
async def get_groups(user: User = Depends(get_current_active_user)):
    response = await fetch_all('group')
    return response

@app.get("/group/{id}", response_model=Group, tags=["group"])
async def get_group_by_id(id: str, user: User = Depends(get_current_active_user)):
    response = await fetch_one('group', id)
    if response:
        return response
    raise HTTPException(404, f"there is no group with this ID {id}")

@app.post("/group", response_model=Group, tags=["group"])
async def create_group(group: CreateGroup, user: User = Depends(get_current_active_user)):
    response = await create('group', group.dict())
    response = await fetch_one('group', response.inserted_id)
    if response:
        return response
    raise HTTPException(400, "Something went wrong / Bad request")

@app.put("/group/{id}", response_model=Group, tags=["group"])
async def put_group(group: CreateGroup, user: User = Depends(get_current_active_user)):
    response = await update('group', id, data)
    if response:
        return response
    raise HTTPException(404, f"there is no group with this ID {id}")

@app.delete("/group/{id}", tags=["group"])
async def delete_group(id:str, user: User = Depends(get_current_active_user)):
    response = await remove('group', id)
    if response:
        return "Succesfully deleted a group!"
    raise HTTPException(404, f"there is no group with this ID {id}")

@app.get("/grouplist", tags=["group list"])
async def get_grouplists(user: User = Depends(get_current_active_user)):
    response = await fetch_all('grouplist')
    return response

@app.get("/grouplist/{id}", response_model=GroupList, tags=["group list"])
async def get_grouplist_by_id(id: str, user: User = Depends(get_current_active_user)):
    response = await fetch_one('grouplist', id)
    if response:
        return response
    raise HTTPException(404, f"there is no grouplist with this ID {id}")

@app.post("/grouplist", response_model=GroupList, tags=["group list"])
async def create_grouplist(grouplist: CreateGroupList, user: User = Depends(get_current_active_user)):
    response = await create('grouplist', grouplist.dict())
    response = await fetch_one('grouplist', response.inserted_id)
    if response:
        return response
    raise HTTPException(400, "Something went wrong / Bad request")

@app.put("/grouplist/{id}", response_model=GroupList, tags=["group list"])
async def put_grouplist(grouplist: CreateGroupList, user: User = Depends(get_current_active_user)):
    response = await update('grouplist', id, data)
    if response:
        return response
    raise HTTPException(404, f"there is no grouplist with this ID {id}")

@app.delete("/grouplist/{id}", tags=["group list"])
async def delete_grouplist(id:str, user: User = Depends(get_current_active_user)):
    response = await remove('grouplist', id)
    if response:
        return "Succesfully deleted a grouplist!"
    raise HTTPException(404, f"there is no grouplist with this ID {id}")