from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

@app.get("/ping")
def send_pong():
    return Response(content="pong" ,status_code=200,  media_type="text/plain")

