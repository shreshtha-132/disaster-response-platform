from db.database import supabase
from datetime import datetime, timedelta
import json

CACHE_TTL_SECONDS = 3600

async def get_from_cache(key:str):
    now = datetime.now().isoformat()
    response = supabase.table("cache").select("*").eq("key",key).single().execute()
    if response.data and response.data["expires_at"] > now:
        return response.data["value"]
    return None

async def set_in_cache(key:str,value:dict,ttl:int=CACHE_TTL_SECONDS):
    expires_at = (datetime.now() + timedelta(seconds=ttl)).isoformat()
    existing = supabase.table("cache").select("key").eq("key",key).single().execute()
    if existing.data:
        supabase.table("cache").update({"value":value,"expires_at":expires_at}).eq("key",key).execute()
    else:
        supabase.table("cache").insert({"key":key,"value":value, "expires_at":expires_at}).execute()
