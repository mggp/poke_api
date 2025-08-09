from typing import List
from app.services.schemas import Berry


class PokebaseClient:
    def __init__(self, base_url: str):
        self.base_url = base_url


class BerryClient(PokebaseClient):
    def get_all_details(self) -> List[Berry]:
        # TODO: Implement the actual API call to fetch berry details.
        return [
            Berry(
                id=1,
                name="cheri",
                growth_time=3,
                max_harvest=5,
                natural_gift_power=50,
                size=20,
                smoothness=10,
                soil_dryness=5,
            ),
        ]
        