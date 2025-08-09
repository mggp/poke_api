from typing import List

from pydantic import BaseModel


class NamedAPIResource(BaseModel):
    name: str
    url: str


class NamedAPIResourceList(BaseModel):
    count: int
    next: str = None
    previous: str = None
    results: List[NamedAPIResource]


class BerryFlavorMap(BaseModel):
    potency: int
    flavor: NamedAPIResource


class Berry(BaseModel):
    id: int
    name: str
    growth_time: int
    max_harvest: int
    natural_gift_power: int
    size: int
    smoothness: int
    soil_dryness: int
    firmness: NamedAPIResource
    flavors: List[BerryFlavorMap]
    item: NamedAPIResource
    natural_gift_type: NamedAPIResource
