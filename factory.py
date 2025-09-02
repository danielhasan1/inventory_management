from location_service import LocationService
from inventory_service import InventoryService


class WarehouseFactory:
    location_service = LocationService()
    inventory_service = InventoryService()

    @classmethod
    def get_location_service(cls) -> LocationService:
        return cls.location_service

    @classmethod
    def get_inventory_service(cls) -> InventoryService:
        return cls.inventory_service