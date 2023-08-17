from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId

from config import ALLOWED_ORIGINS

app = FastAPI()

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

@app.get("/api/grocery")
async def get_groceries():
    response = await fetch_all_todos()
    return response

@app.get("/api/grocery{id}", response_model=Todo)
async def get_grocery_by_id(id: str):
    response = await fetch_one_todo(id)
    if response:
        return response
    raise HTTPException(404, f"there is no TODO item with this title {title}")

@app.post("/api/grocery", response_model=Todo)
async def post_grocery(grocery:CreateTodo):
    response = await create_todo(grocery.dict())
    response = await fetch_one_todo(response.inserted_id)
    if response:
        return response
    raise HTTPException(400, "Something went wrong / Bad request")
    
    
# TODO
@app.put("/api/grocery{title}", response_model=Todo)
async def put_grocery(title:str, data:str):
    response = await update_todo(title, desc)
    if response:
        return response
    raise HTTPException(404, f"there is no TODO item with this title {title}")

# TODO
@app.delete("/api/grocery{title}")
async def delete_grocery(title):
    response = await remove_todo(title)
    if response:
        return "Succesfully deleted todo item!"
    raise HTTPException(404, f"there is no TODO item with this title {title}")