from pydantic import BaseModel
from typing import List,Optional
from uuid import UUID

class GeoPoint(BaseModel):
    latitude:float
    longitude:float

class DisasterCreate(BaseModel):
    title:str
    location_name: Optional[str]=None
    description:str
    tags:List[str]
    owner_id:str

class DisasterUpdate(BaseModel):
    title: Optional[str]=None
    location_name: Optional[str]=None
    description:Optional[str]=None
    tags:Optional[List[str]]=None
    owner_id:Optional[str]=None


class ResourceCreate(BaseModel):
    # disaster_id uuid references disasters(id),
    # name text,
    # location_name text,
    # location geography(Point, 4326),
    # type text,
    disaster_id: UUID
    name: str
    location_name: str
    location: Optional[GeoPoint]=None
    type: Optional[str]


class ResourceUpdate(BaseModel):
    name: Optional[str]=None
    location_name: Optional[str]=None
    location: Optional[GeoPoint]=None
    type: Optional[str]=None



       