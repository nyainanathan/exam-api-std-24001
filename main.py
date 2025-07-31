import _pydatetime
from _pydatetime import datetime
from fastapi import FastAPI
from pydantic_core.core_schema import DatetimeSchema
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

@app.get("/ping")
def send_pong():
    return Response(content="pong" ,status_code=200,  media_type="text/plain")

@app.get("/home")
def welcome_home():
    with open("welcome.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=200, media_type="text/html")


class PostPayload(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: str

post_list : List[PostPayload] = []

@app.post("/posts")
def create_posts(new_posts: List[PostPayload]):
    resp = []
    post_list.extend(new_posts)
    for post in post_list:
        resp.append(post.model_dump())
    return JSONResponse(content={"posts" : resp} , status_code=201)

@app.get("/posts")
def show_posts():
    all_posts = []
    for post in post_list:
        all_posts.append(post.model_dump())
    return  JSONResponse(content={"all the posts" : all_posts}, status_code=200)


@app.get("/{full_path:path}")
def catch_invalid_paths(full_path: str):
    with open("error.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=404, media_type="text/html")
