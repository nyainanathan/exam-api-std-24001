import _pydatetime
import base64
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


@app.get("/ping/auth")
def send_pong(request : Request):

    auth_header = request.headers.get("Authorization")
    auth_header_encoded_str = auth_header.replace("Basic ", "")

    required_credential = "user:secret"
    required_credential_bytes = required_credential.encode("utf-8")
    required_credential_encoded = base64.b64encode(required_credential_bytes)
    required_credential_encoded_str = required_credential_encoded.decode("utf-8")

    if auth_header_encoded_str == required_credential_encoded_str:
        return Response(content=f"pong" ,status_code=200,  media_type="text/plain")
    return Response(content="wrong credentials", status_code=403, media_type="text/plain")

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


def serialize_posts():
    serialized_posts = []
    for post in post_list:
        serialized_posts.append(post.model_dump())
    return serialized_posts

@app.put("/posts")
def edit_posts(updated_posts : List[PostPayload]):
    if len(updated_posts) == 0:
        return JSONResponse(content={"error message" :"there is no tasks to be updated"}, status_code=400)
    else:
        for updated_post in updated_posts:
            is_present = False
            post_index = 0
            for present_post in post_list:
                if updated_post.title == present_post.title:
                    is_present = True
                    post_index = post_list.index(present_post)
            if is_present:
                post_list.pop(post_index)
                post_list.insert(post_index, updated_post)
            else:
                post_list.append(updated_post)
    return JSONResponse(content={"Updated set of tasks" : serialize_posts()}, status_code=200)

@app.get("/{full_path:path}")
def catch_invalid_paths(full_path: str):
    with open("error.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=404, media_type="text/html")
