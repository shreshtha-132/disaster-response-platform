from google import genai
import httpx
import os
from services.cache import get_from_cache,set_in_cache

GEMINI_API_KEY = os.environ.get("GOOGLE_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

async def extract_location_with_gemini(description:str):
    key = f"loc:{description}"
    cached = await get_from_cache(key=key)
    if cached:
        return cached
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",contents=f"Extract only the location name from this sentence: '{description}'"
    )
    result = response.text.strip()
    await set_in_cache(key, result)
    return result
    

async def verify_image_with_gemini(image_url:str):
    key = f"img:{image_url}"
    cached = await get_from_cache(key=key)
    if cached:
        return cached
    
    prompt = f"Verify if the image at this URL depicts a real disaster or is fake: {image_url}"
    response = client.models.generate_content(model="gemini-2.5-flash",contents=prompt)
    
    result = response.text.strip()
    await set_in_cache(key, result)
    return result
    