# this would fetch real time updates from goverment websites and post it
from db.database import supabase
from fastapi import APIRouter

router = APIRouter()

@router.get("/official-updates")
def getOfficialUpdates():
    #we need to scrap from government website and then show 
    return {
        "updates":[
            {"source":"NDMA","update":"Red Alert in mumbai due to heavy rainfall."},
            {"source":"IMD","update":"Expect over 150mm rain in next 24 hours."}
        ]
    }