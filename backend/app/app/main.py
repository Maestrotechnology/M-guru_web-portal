from fastapi import FastAPI, Request, status
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
import asyncio
import sys
sys.path.append('../')

from app.api.api import api_router
from app.core.config import settings
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
import threading
# from app.api.endpoints.mqtt_api import run
# from app.api.endpoints import mqtt_api
# from app.api.endpoints.mqtt_api import run_mqtt_in_thread
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(docs_url=settings.API_DOC_PATH,
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# app.mount("/static", StaticFiles(directory="static"), name="static")
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(),
                 }),
    )
# import logging


# logging.basicConfig(level=logging.DEBUG)

# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     logging.debug(f"Request: {request.method} {request.url}")
#     response = await call_next(request)
#     logging.debug(f"Response: {response.status_code}")
#     return response

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     errors = []
#     for error in exc.errors():
#         errors.append({"loc": error["loc"], "msg": error["msg"], "type": error["type"]})
#     logging.error(f"Validation errors: {errors}")
#     return JSONResponse(status_code=422, content={"detail": "Validation error", "errors": errors})

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
app.include_router(api_router, prefix=settings.API_V1_STR)