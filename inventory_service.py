from db import get_db
from repositories import LocationRepository, InventoryRepository


class InventoryService:

    @staticmethod
    def increment_inventory(location_name: str, item_id: str, quantity: int) -> str:
        # TODO: CHECK PARAMS VALIDATION FOR EACH METHOD
        location = LocationRepository.get_by_name(location_name)
        if not location or not location.is_active():
            return f"ERR: Location '{location_name}' does not exist"

        inventory = InventoryRepository.get_or_create(location.id, item_id)
        inventory.quantity += int(quantity)
        InventoryRepository.save(inventory)
        return "OK"

    @staticmethod
    def decrement_inventory(location_name: str, item_id: str, quantity: int) -> str:
        # TODO: CHECK PARAMS VALIDATION FOR EACH METHOD
        location = LocationRepository.get_by_name(location_name)
        if not location or not location.is_active():
            return f"ERR: Location '{location_name}' does not exist"

        inventory = InventoryRepository.get_or_create(location.id, item_id)
        if inventory.quantity < int(quantity):
            return f"ERR: Insufficient quantity of item {item_id} in location {location_name} (has {inventory.quantity})"

        inventory.quantity -= int(quantity)
        InventoryRepository.save(inventory)
        return "OK"

    @staticmethod
    def transfer_inventory(*args) -> str:
        # TODO: CHECK PARAMS VALIDATION FOR EACH METHOD
        try:
            from_location, to_location, item_id, quantity = args
        except ValueError:
            return (f"ERR: Inventory Transfer requires from_location, to_location, item_id, quantity in ordered fashion")
        f_location = LocationRepository.get_by_name(from_location)
        t_location = LocationRepository.get_by_name(to_location)
        if not f_location or not f_location.is_active():
            return f"ERR: Location '{from_location}' does not exist"
        if not t_location or not t_location.is_active():
            return f"ERR: Location '{to_location}' does not exist"
        f_inventory = InventoryRepository.get_or_create(f_location.id, item_id)
        to_inventory = InventoryRepository.get_or_create(t_location.id, item_id)
        if f_inventory.quantity < int(quantity):
            return f"ERR: Insufficient quantity of item {item_id} in location {from_location} (has {f_inventory.quantity})"
        f_inventory.quantity -= int(quantity)
        to_inventory.quantity += int(quantity)
        InventoryRepository.transfer_inventory(f_inventory, to_inventory)
        return "OK"

    @staticmethod
    def observer_inventory(location_name: str) -> str:
        # TODO: CHECK PARAMS VALIDATION FOR EACH METHOD
        location = LocationRepository.get_by_name(location_name)

        if not location or not location.is_active():
            return f"ERR: Location '{location_name}' does not exist"

        inventories = InventoryRepository.get_by_location(location.id)

        if not inventories or all(inventory.quantity == 0 for inventory in inventories):
            return f"EMPTY"
        res = []
        for inventory in inventories:
            if inventory.quantity == 0:
                continue
            # kinda wanted to preserve cli main '>' format so patching here
            if not res:
                # first line so dont prepend >
                res.append(f"ITEM {inventory.item_id} {str(inventory.quantity)}\n")
            else:
                res.append(f"> ITEM {inventory.item_id} {str(inventory.quantity)}\n")
        return "".join(res)
