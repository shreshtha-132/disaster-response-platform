from fastapi import APIRouter,HTTPException
from models.schemas import ResourceCreate,ResourceUpdate,GeoPoint
from db.database import supabase
from uuid import UUID
from datetime import datetime
from . import geocode

router = APIRouter()

@router.post("/resources")
async def add_resource(resource: ResourceCreate):
    data = {
    "disaster_id": str(resource.disaster_id),  # ✅ Fix here
    "name": resource.name,
    "location_name": resource.location_name,
    "location": None,  # filled below
    "type": resource.type
    }
    existing = supabase.table("disasters").select("id").eq("id", str(resource.disaster_id)).single().execute()
    if not existing.data:
        raise HTTPException(status_code=404,detail="Disaster Not Found")

    #add a check here to check even if disaster_id is present or not from the disasters table
    coordinates = await geocode.getCoord(resource.location_name)
    data["location"]= f"POINT({coordinates.longitude} {coordinates.latitude})"
    data["created_at"] = datetime.now().isoformat()
    response = supabase.table("resources").insert(data).execute()
    return {"message":"Resource Created","data":response.data}


#get resources with help of disaster id
@router.get("/resources/{disaster_id}/resources")
def get_resources_by_disaster_id(disaster_id:UUID):
    # this endpont would fetch all the resources using the disaster id
    check_disaster = supabase.table("disasters").select("id").eq("id", str(disaster_id)).maybe_single().execute()
    if not check_disaster.data:
        raise HTTPException(status_code=404, detail="Disaster not found")
    
    response = supabase.table("resources").select("*").eq("disaster_id",str(disaster_id)).execute()
    return {"Resources":response.data}

#get resource with the help of location_name
#gets the location name converts into geopoint, finds the disaster id of disaster at that geopoint
@router.get("/resources/{location_name}/resources")
async def get_resources_by_name(location_name:str):
    latlon = await geocode.getCoord(location_name=location_name)
    if not latlon:
        raise HTTPException(status_code=404,detail="Invalid Location Name")
    
    #finding disasters
    point_wkt = f"POINT({latlon.longitude} {latlon.latitude})"
    radius_meters = 5000

    disasters_reponse = supabase.rpc("find_disasters_near_location",
    {"location":point_wkt,"radius_meters":radius_meters}).execute()

    if disasters_reponse.error:
        raise HTTPException(status_code=500,detail="Error fetching disasters")
    
    disaster_ids = [d["id"] for d in disasters_reponse.data]
    if not disaster_ids:
        return {"resources":[]} 
    
    #fetch all resources for this ids

    response = supabase.table("resources").select("*").in_("disaster_id",disaster_ids).execute()
    if not response.data:
        raise HTTPException(status_code=500,detail="Error Fetching resources")
    return {"Resources":response.data}




