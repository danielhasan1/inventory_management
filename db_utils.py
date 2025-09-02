from typing import Any, Optional
import sqlite3
import uuid
from db import get_db


class DBUtils:
    @staticmethod
    def exists_by_field(*, table: str, field: str, value: Any) -> bool:
        with get_db() as db:
            row = db.execute(
                f"SELECT EXISTS(SELECT 1 FROM {table} WHERE {field} = ?)",
                (value,)
            ).fetchone()
            return bool(row[0])

    @staticmethod
    def get_by_field(*, table: str, field: str, value: Any) -> Optional[dict]:
        """get row by field name if multiple exists it will return the first one in default ordering"""
        with get_db() as db:
            db.row_factory = sqlite3.Row
            row = db.execute(
                f"SELECT * FROM {table} WHERE {field} = ?",
                (value,)
            ).fetchone()
            return dict(row) if row else None

    @staticmethod
    def generate_unique_id(*, table: str) -> str:
        while True:
            new_id = str(uuid.uuid4())
            if not DBUtils.exists_by_field(table=table, field="id", value=new_id):
                return new_id

    @staticmethod
    def get_by_fields(*, table: str, fields: list, values: list) -> Optional[dict]:
        """get row by field name if multiple exists it will return the first one in default ordering"""
        with get_db() as db:
            db.row_factory = sqlite3.Row
            conditions = " AND ".join([f"{field}=?" for field in fields])
            query = f"SELECT * FROM {table} WHERE {conditions} LIMIT 1"
            row = db.execute(query, values).fetchone()
            return dict(row) if row else None