from app.config import get_settings
from app.router import router
from fastapi import FastAPI

version = get_settings().psgc_version
app = FastAPI(
    title="PSGC",
    description=f"Data Server of the PSGC Version {version}. Implemented using FastAPI and SQLite.",
    
)

# # Root
# @app.get("/")
# def root():
#     return { "message": "Welcome to the PSGC Rest API" }

app.include_router(router, prefix="/psgc")
