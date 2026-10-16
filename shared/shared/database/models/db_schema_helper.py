from typing import Generic, TypeVar
from pydantic import BaseModel



T = TypeVar("T", bound=BaseModel)


class TableRef(Generic[T]):
    def __init__(self, name: str, model: type[T]):
        self.name = name
        self.model = model

        # Map db aliases to correctly validate column names in the way that the database expects them
        self._db_to_field: dict[str, str] = {}
        for field_name, info in model.model_fields.items():
            db_name = info.alias or field_name
            self._db_to_field[db_name] = field_name

        # Translate python field names to db column names
        self._field_to_db: dict[str, str] = {f: d for d, f in self._db_to_field.items()}

        # All db column names as one comma separated string for select statements
        self.columns = ",".join(self._db_to_field)


    # Column name validator
    def col(self, field: str) -> str:
        if field in self._db_to_field:
            return field
        if field in self._field_to_db:
            return self._field_to_db[field]
        raise ValueError(f"Invalid column name '{field}' in table '{self.name}'")


    def cols(self, *fields: str) -> str:
        return ",".join(self.col(c) for c in fields)


    # Result parser
    def parse(self, rows: list[dict]) -> list[T]:
        return [self.model.model_validate(r) for r in rows]



###############################################
# Instantiate schemas for all db tables here
###############################################

from shared.database.models.fastapi.schema_public_latest import TestingTable



TESTING_TABLE = TableRef("testing_table", TestingTable)
