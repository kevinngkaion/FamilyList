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
import asyncio
from pprint import pprint

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
def read_root():
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
async def get_user_by_id(id: str):
    response = await fetch_one('user', id)
    if response:
        return response
    raise HTTPException(404, f"there is no user with this ID {id}")

@app.put("/user/{id}", response_model=User, tags=["user"])
async def put_user(id:str, data:UpdateUser):
    response = await update('user', id, data)
    if response:
        return response
    raise HTTPException(404, f"there is no user with this ID {id}")

@app.delete("/user/{id}", tags=["user"])
async def delete_user(id:str):
    response = await remove('user', id)
    if response:
        return "Succesfully deleted a user!"
    raise HTTPException(404, f"there is no user with this ID {id}")

@app.get("/group", tags=["group"])
async def get_groups():
    response = await fetch_all('group')
    return response

@app.get("/group/{id}", response_model=Group, tags=["group"])
async def get_group_by_id(id: str):
    response = await fetch_one('group', id)
    if response:
        return response
    raise HTTPException(404, f"there is no group with this ID {id}")

@app.post("/group", response_model=Group, tags=["group"])
async def create_group(group: CreateGroup):
    response = await create('group', group.dict())
    response = await fetch_one('group', response.inserted_id)
    if response:
        return response
    raise HTTPException(400, "Something went wrong / Bad request")

@app.put("/group/{id}", response_model=Group, tags=["group"])
async def put_group(group: CreateGroup):
    response = await update('group', id, data)
    if response:
        return response
    raise HTTPException(404, f"there is no group with this ID {id}")

@app.delete("/group/{id}", tags=["group"])
async def delete_group(id:str):
    response = await remove('group', id)
    if response:
        return "Succesfully deleted a group!"
    raise HTTPException(404, f"there is no group with this ID {id}")

def create_base_user(user):
    if user['_id'] and user['fname'] and user['lname']:
        return BaseUser(id=user['_id'], fname=user['fname'], lname=user['lname'])
    return None

async def convert_grouplist(grouplist):
    # This function will take a raw grouplist from the db and convert all the ids for the group and members into their appropriate objects.
    group_id = grouplist['group']
    group = await fetch_one('group', group_id)
    if group:
        #Get the ids of the group admin and members
        admin_id = group['admin']
        member_ids = group['members']
        
        #fetch_tasks is a list of the async tasks that need to be run.
        fetch_tasks = [fetch_one('user', member_id) for member_id in member_ids]
        
        #convert the admin to a base user in order to return meaningful information
        admin = create_base_user(await fetch_one('user', admin_id))
        
        #asyncio gather will wait for all the tasks in the fetch_tasks list to complete before assigning to members_list
        members_list = await asyncio.gather(*fetch_tasks)
        members = [create_base_user(member) for member in members_list]
        
        #set the group's info to be the meaningful Object Models
        group['admin'] = admin
        group['members'] = members
        grouplist['group'] = group
    else:
        raise HTTPException(404, f"The group who owns this list could not be found")
    return 

@app.get("/grouplist", tags=["group list"])
async def get_grouplists():
    grouplists = await fetch_all('grouplist')
    response = []
    for grouplist in grouplists:
        await convert_grouplist(grouplist)
        response.append(GroupList(**grouplist))
    return response

@app.get("/grouplist/{id}", response_model=GroupList, tags=["group list"])
async def get_grouplist_by_id(id: str):

    grouplist = await fetch_one('grouplist', id)
    if grouplist:
        await convert_grouplist(grouplist)
        response = grouplist
        return response
    raise HTTPException(404, f"there is no grouplist with this ID {id}")

@app.post("/grouplist", response_model=GroupList, tags=["group list"])
async def create_grouplist(grouplist: CreateGroupList):
    response = await create('grouplist', grouplist.dict())
    response = await fetch_one('grouplist', response.inserted_id)
    if response:
        return response
    raise HTTPException(400, "Something went wrong / Bad request")

@app.put("/grouplist/{id}", response_model=GroupList, tags=["group list"])
async def put_grouplist(id:str, grouplist: CreateGroupList):
    response = await update('grouplist', id, grouplist)
    if response:
        return response
    raise HTTPException(404, f"there is no grouplist with this ID {id}")
    return {"Hello": "World"}

@app.delete("/grouplist/{id}", tags=["group list"])
async def delete_grouplist(id:str):
    response = await remove('grouplist', id)
    if response:
        return "Succesfully deleted a grouplist!"
    raise HTTPException(404, f"there is no grouplist with this ID {id}")