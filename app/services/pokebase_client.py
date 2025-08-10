import asyncio
from typing import List

import httpx

from app.services.schemas import Berry, NamedAPIResource, NamedAPIResourceList


class PokebaseClient:
    ENDPOINT: str = ""
    API_VERSION: str = "v2"

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.path = f"{self.base_url}/{self.API_VERSION}/{self.ENDPOINT}"


class NamedAssetAPIResource[AssetDetailT](PokebaseClient):
    DETAIL_CLASS: type[AssetDetailT]

    def __init__(self, base_url: str):
        super().__init__(base_url)
        self.client = httpx.AsyncClient()

    async def get_list(self) -> List[NamedAPIResource]:
        next_url = self.path
        all_resources = []

        while next_url:
            resource_list = await self.get_page(next_url)
            all_resources.extend(resource_list.results)
            next_url = resource_list.next

        return [NamedAPIResource(**item) for item in all_resources]

    async def get_page(self, url: str) -> NamedAPIResourceList:
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()

    async def get_all_details(self) -> List[AssetDetailT]:
        all_resources = await self.get_list()
        detail_tasks = [self.get_detail(resource.url) for resource in all_resources]
        return await asyncio.gather(*detail_tasks)

    async def get_detail(self, url: str) -> AssetDetailT:
        response = await self.client.get(url)
        response.raise_for_status()
        return self.DETAIL_CLASS(**response.json())


class BerryClient(NamedAssetAPIResource[Berry]):
    ENDPOINT = "berry"
    DETAIL_CLASS = Berry
