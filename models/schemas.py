from pydantic import BaseModel
from typing import List,Optional
from uuid import UUID

class GeoPoint(BaseModel):
    latitude:float
    longitude:float

class DisasterCreate(BaseModel):
    title:str
    location_name: Optional[str]
    description:str
    tags:List[str]
    owner_id:str

class DisasterUpdate(BaseModel):
    title: Optional[str]
    location_name: Optional[str]
    description:Optional[str]
    tags:Optional[List[str]]
    owner_id:Optional[str]


class ResourceCreate(BaseModel):
    # disaster_id uuid references disasters(id),
    # name text,
    # location_name text,
    # location geography(Point, 4326),
    # type text,
    disaster_id: UUID
    name: str
    location_name: str
    location: Optional[GeoPoint]
    type: Optional[str]


class ResourceUpdate(BaseModel):
    name: Optional[str]
    location_name: Optional[str]
    location: Optional[GeoPoint]
    type: Optional[str]



       