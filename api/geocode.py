# this would extract location with gemini convert to lat/lan
from db.database import supabase
from fastapi import APIRouter, HTTPException
import httpx
from models.schemas import GeoPoint
from services import gemini
from services.cache import get_from_cache, set_in_cache

async def getCoord(location_name:str):
    key = f"coord:{location_name}"
    cached = await get_from_cache(key=key)
    if cached:
        return GeoPoint(**cached)
    
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q":location_name,
        "format":"json",
        "limit":1
    }
    headers = {
        "User-Agent":"DisasterResponsePlatform/1.0"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        data = response.json()

    if data:
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        result = GeoPoint(latitude=lat, longitude=lon)
        await set_in_cache(key, dict(result))
        return result
        
    else:
        return None




async def getLocationAndCoordinates(description:str):
    key = f"locAndCoord{description}"
    cached = await get_from_cache(key=key)
    if cached:
        cached["location_coord"] = GeoPoint(**cached["location_coord"])
        return cached
    
    location_name = await gemini.extract_location_with_gemini(description=description)
    coordinates = await getCoord(location_name)
    result = {
        "location_name": location_name,
        "location_coord": coordinates
    }
    await set_in_cache(key, {
        "location_name": location_name,
        "location_coord": dict(coordinates)
    })
    return result

    
    

