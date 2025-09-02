from typing import Optional
import sqlite3

import options
from db_utils import DBUtils
from models import Location, Inventory
from options import Status
from db import get_db


class LocationRepository:
    @staticmethod
    def create(location: Location) -> Location:
        row = DBUtils.get_by_field(table="locations", field="name", value=location.name)
        if row and row.get("status") == options.Status.REGISTER.value:
            raise ValueError(f"ERR: Location '{location.name}' already exists")

        if not row:
            location.id = DBUtils.generate_unique_id(table="locations")
        else:
            location.id = row["id"]
        location.status = Status.REGISTER.value

        with get_db() as db:
            db.execute(
                "INSERT OR REPLACE INTO locations (id, name, status) VALUES (?, ?, ?)",
                (location.id, location.name, location.status)
            )
        return location

    @staticmethod
    def get_by_name(name: str) -> Optional[Location]:
        data = DBUtils.get_by_field(table="locations", field="name", value=name)
        return Location(**data) if data else None

    @staticmethod
    def update_status(location: Location, status: int):
        with get_db() as db:
            db.execute(
                "UPDATE locations SET status = ? WHERE id = ?",
                (status, location.id)
            )

    @staticmethod
    def has_inventory(location_id) -> bool:
        return DBUtils.exists_by_field(table="inventory", field="location_id", value=location_id)


class InventoryRepository:
    @staticmethod
    def get_or_create(location_id: str, item_id: str) -> Inventory:
        data = DBUtils.get_by_fields(table="inventory", fields=["location_id", "item_id"], values=[location_id, item_id])
        if data and data['item_id'] == item_id:
            return Inventory(**data)

        # Create new inventory item
        inventory = Inventory(
            id=DBUtils.generate_unique_id(table="inventory"),
            location_id=location_id,
            item_id=item_id,
            quantity=0
        )
        return inventory

    @staticmethod
    def save(inventory: Inventory):
        with get_db() as db:
            db.execute(
                """INSERT OR REPLACE INTO inventory 
                   (id, location_id, item_id, quantity) VALUES (?, ?, ?, ?)""",
                (inventory.id, inventory.location_id, inventory.item_id, inventory.quantity)
            )

    @staticmethod
    def get_by_location(location_id: str) -> list[Inventory]:
        with get_db() as db:
            db.row_factory = sqlite3.Row
            rows = db.execute(
                "SELECT * FROM inventory WHERE location_id = ? ORDER BY created_at DESC",
                (location_id,)
            ).fetchall()
            return [Inventory(**dict(row)) for row in rows]


    @staticmethod
    def transfer_inventory(f_inventory: Inventory, to_inventory: Inventory) -> None:
        with get_db() as db:
            db.execute("UPDATE inventory SET quantity = ? WHERE id = ? AND location_id = ?",
                       (f_inventory.quantity, f_inventory.id, f_inventory.location_id))
            db.execute("INSERT OR REPLACE INTO inventory (id, location_id, item_id, quantity) VALUES (?, ?, ?, ?)",
                       (to_inventory.id, to_inventory.location_id, to_inventory.item_id, to_inventory.quantity))