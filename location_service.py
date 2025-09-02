from repositories import LocationRepository
from models import Location
from options import Status


class LocationService:
    @staticmethod
    def register_location(*args) -> str:
        # TODO: CHECK PARAMS VALIDATION FOR EACH METHOD
        try:
            name = args[0]
            location = Location(name=name)
            LocationRepository.create(location)
            return "OK"
        except ValueError as e:
            return str(e)

    @staticmethod
    def deregister_location(*args) -> str:
        # TODO: CHECK PARAMS VALIDATION FOR EACH METHOD
        name = args[0]
        location = LocationRepository.get_by_name(name)
        if not location:
            return f"ERR: Location '{name}' does not exist"

        if not location.is_active():
            return f"ERR: Location '{name}' does not exist"

        if location.has_inventory():
            return f"ERR: Location '{name}' has inventories"

        LocationRepository.update_status(location, Status.DEREGISTER.value)
        return "OK"