import sqlite3
import uuid

from db import get_db


class BaseFeatures:

    def generate_id(self, table: str) -> uuid.UUID:
        with get_db() as db:
            while 1:
                rando_id = uuid.uuid4()
                if not self._is_id_exist(table=table, uid=rando_id, db=db):
                    return rando_id

    @staticmethod
    def _is_id_exist(*, table: str, uid: uuid.UUID, db: sqlite3.Cursor) -> bool:
            row = db.execute(f"select exists(select 1 from {table} where id=?) ", (str(uid),)).fetchone()
            if row[0] == 0:
                return False
            return True

    @staticmethod
    def _is_name_exist(*, field: str, table: str, value: str | int,  db: sqlite3.Cursor) -> bool:
        row = db.execute(f"select exists(select 1 from {table} where {field}=?) ", (value,)).fetchone()
        if row[0] == 0:
            return False
        return True

    def get_by_field(self, *, table: str, field: str):
        pass

