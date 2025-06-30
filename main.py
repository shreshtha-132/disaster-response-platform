# from models import DisasterSchema,ReportSchema
# from db import insert_record
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

app = FastAPI()

from api import(
    disaster_router,
    social_media_router,
    updates_router,
    verify_image_router,
    resource_router
)
app.include_router(disaster_router)
# app.include_router(geocode_router)
app.include_router(social_media_router)
app.include_router(updates_router)
app.include_router(verify_image_router)
app.include_router(resource_router)

@app.get("/")
def root():
    return {"Hello Welcome to Home"}

