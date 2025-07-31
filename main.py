from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()