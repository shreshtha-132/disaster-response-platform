# this would get the image and verify it using gemini API for fake or real
from db.database import supabase
from fastapi import APIRouter, Query
from services import gemini

router = APIRouter()

@router.get("/verify-image")
async def verify_image(image_url: str = Query(..., description="Image URL to verify")):
    result = await gemini.verify_image_with_gemini(image_url=image_url)
    return {"verification_result":result}