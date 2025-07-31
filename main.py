from fastapi import FastAPI
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

@app.get("/{full_path:path}")
def catch_invalid_paths(full_path: str):
    with open("error.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=404, media_type="text/html")