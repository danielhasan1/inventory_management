from db import get_db
from options import Status
from base import BaseFeatures


class Location(BaseFeatures):
    def __init__(self, name: str):
        self.name = name
        self.id = None

    def register(self):
        with get_db() as db:
            if not self._is_name_exist(field="name", table="locations", value=self.name, db=db):
                self.id = self.generate_id(table="locations")
                db.execute(
                    '''insert into locations (name, id, status) values (?, ?, ?)''',
                    (self.name, str(self.id), Status.REGISTER.value),
                )
            else:
                raise ValueError(f"ERR: Location '{self.name}' already exists")

    def deregister(self):
        with get_db() as db:
            if self._is_name_exist(field="name", table="locations", value=self.name, db=db):
                has_inventory = db.execute(
                    "SELECT EXISTS(SELECT 1 FROM inventory WHERE location_id = ?)",
                    (self.id,)
                ).fetchone()[0]
                if has_inventory:
                    raise ValueError(f"ERR: Location '{self.name}' has inventories")
                db.execute('''update locations set status =? where name=?''', (Status.DEREGISTER.value, self.name,))
