from db.database import supabase
from datetime import datetime, timedelta
import json

CACHE_TTL_SECONDS = 3600

async def get_from_cache(key:str):
    response = supabase.table("cache").select("*").eq("key",key).execute()
    data_list = response.data
    if data_list and len(data_list)==1:
        data = data_list[0]
        expires_at = datetime.fromisoformat(data["expires_at"])
        if expires_at > datetime.now():
            try:
                return json.loads(data["value"])
            except (json.JSONDecodeError, TypeError):
                return data["value"]
            
        return None
    

async def set_in_cache(key:str,value:dict,ttl:int=CACHE_TTL_SECONDS):
    expires_at = (datetime.now() + timedelta(seconds=ttl)).isoformat()
    json_value = json.dumps(value)

    existing = supabase.table("cache").select("key").eq("key",key).execute()
    if existing.data:
        supabase.table("cache").update({"value":json_value,"expires_at":expires_at}).eq("key",key).execute()
    else:
        supabase.table("cache").insert({"key":key,"value":json_value, "expires_at":expires_at}).execute()
