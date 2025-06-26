from fastapi import APIRouter,HTTPException
from db.database import supabase
from models.schemas import DisasterCreate,DisasterUpdate,GeoPoint
from datetime import datetime
from uuid import UUID
from . import geocode

router = APIRouter()

@router.get("/disasters")
def fetch_disasters():
    data = supabase.table("disasters").select("*").execute()
    return {"disasters": data.data}

@router.post("/disasters")
async def create_disaster(disaster:DisasterCreate):
    # disaster.title,disaster.tags,disaster.description,disaster.owner_id
    # title text,
    # location_name text,
    # location geography(Point, 4326),
    # description text,
    # tags text[],
    # owner_id text,
    # created_at timestamp default now(),
    # audit_trail jsonb
    now = datetime.now().isoformat()
    insert_data = dict(disaster)
    
    location_data = await geocode.getLocationAndCoordinates(disaster.description)

    insert_data["location_name"]=location_data["location_name"]
    latlon = location_data["location_coord"]
    insert_data["location"] = f"POINT({latlon.longitude} {latlon.latitude})"
    

    #now convert location_name to lan,lat       
    insert_data["created_at"] = now
    insert_data["audit_trail"]=[{
        "action":"create",
        "user_id":disaster.owner_id or "unknown",
        "timestamp":now
    }]

    response = supabase.table("disasters").insert(insert_data).execute()
    return {"message":"Disaster Created","data": response.data}
    


@router.get("/disasters/{disaster_id}")
def fetch_disaster(disaster_id:UUID):
    response = supabase.table("disasters").select("*").eq("id",str(disaster_id)).single().execute()
    if not response.data:
        raise HTTPException(status_code=404,detail="Disaster Not Found")
    return {"disaster":response.data}


@router.put("/disasters/{disaster_id}")
async def update_disaster(disaster:DisasterUpdate,disaster_id:UUID):
    existing = supabase.table("disasters").select("*").eq("id",str(disaster_id)).single().execute()
    if not existing.data:
        raise HTTPException(status_code=404,detail="Disaster Not Found")
    
    update_data = {}
    if disaster.title is not None:
        update_data["title"]=disaster.title
    if disaster.tags is not None:
        update_data["tags"]=disaster.tags
    if disaster.description is not None:
        update_data["description"]=disaster.description
        #update location (lat,lan) as well
        new_data = await geocode.getLocationAndCoordinates(disaster.description)
        latlon = new_data["location_coord"]
        update_data["location"] = f"POINT({latlon.longitude} {latlon.latitude})"
        update_data["location_name"] = new_data["location_name"]
    if disaster.owner_id is not None:
        update_data["owner_id"]=disaster.owner_id
    

    old_trail = existing.data.get("audit_trail", []) or []
    old_trail.append({
        "action":"update",
        "user_id":disaster.owner_id or "unknown",
        "timestamp":datetime.now().isoformat()
    })

    update_data["audit_trail"]=old_trail

    updated = supabase.table("disasters").update(update_data).eq("id", str(disaster_id)).execute()

    return {"updated":updated.data}




@router.delete("/disasters/{disaster_id}")
def delete_disaster(disaster_id:UUID):
    deleted = supabase.table("disasters").delete().eq("id",str(disaster_id)).execute()
    if not deleted.data:
        raise HTTPException(status_code=404,detail="Disaster Not Found")
    return {"deleted":deleted.data}


