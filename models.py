from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from options import Status
from db_utils import DBUtils



@dataclass
class Location:
    name: str
    id: Optional[str] = None
    status: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def is_active(self) -> bool:
        return self.status == Status.REGISTER.value

    def has_inventory(self) -> bool:
        from repositories import LocationRepository
        return LocationRepository.has_inventory(self.id)


@dataclass
class Inventory:
    location_id: str
    item_id: str
    quantity: int
    location_id: Optional[str]
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
