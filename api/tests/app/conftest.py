from uuid import uuid4

from pydantic import BaseModel


#################################################################
# Shared testing fixtures for all endpoint tests (since they all need to request from a mocked table):
#################################################################

class FakeTable:
    #################################
    # Some columns (e.g. "id" on Holding) are filterable on the real table but aren't
    # part of the pydantic model, same as real postgrest filters not needing to be
    # selected columns. _extra tracks those per row, keyed the same as _rows.
    #################################
    def __init__(self, model: type[BaseModel], extra_fields=lambda: {}, rows=()):
        self.model = model
        self.extra_fields = extra_fields
        self._rows: dict[str, BaseModel] = {}
        self._extra: dict[str, dict] = {}
        for row in rows:
            key = str(row.id)
            self._rows[key] = row
            self._extra[key] = {"id": row.id}

    def _value(self, key, row, column):
        if hasattr(row, column):
            return getattr(row, column)
        return self._extra.get(key, {}).get(column)

    def find(self, limit=None, gt=None, lt=None, **filters):
        items = list(self._rows.items())
        for column, value in filters.items():
            items = [(k, r) for k, r in items if str(self._value(k, r, column)) == str(value)]
        for column, value in (gt or {}).items():
            items = [(k, r) for k, r in items if self._value(k, r, column) > value]
        for column, value in (lt or {}).items():
            items = [(k, r) for k, r in items if self._value(k, r, column) < value]
        rows = [r for _, r in items]
        return rows[:limit] if limit else rows

    def get(self, **filters):
        rows = self.find(limit=1, **filters)
        return rows[0] if rows else None

    def insert(self, *rows):
        created = []
        for row in rows:
            fields = self.extra_fields()
            key = str(fields.get("id", uuid4()))
            entry = self.model(**row.model_dump(exclude=set(fields)), **fields)
            self._rows[key] = entry
            self._extra[key] = fields
            created.append(entry)
        return created

    def update(self, values: dict, **filters):
        if not filters:
            raise ValueError("update needs at least one filter")
        keys = [k for k, r in self._rows.items()
                if all(str(self._value(k, r, column)) == str(value) for column, value in filters.items())]
        updated = []
        for key in keys:
            new_row = self._rows[key].model_copy(update=values)
            self._rows[key] = new_row
            updated.append(new_row)
        return updated

    #################################
    # Mock the select_query().or_(...).limit(...) chain that e.g. get_current_season()
    # queries for requests that are more complex than what find() can provide.
    #################################
    def select_query(self):
        return self

    def or_(self, *_args, **_kwargs):
        return self

    def limit(self, *_args, **_kwargs):
        return self

    def run(self, _query):
        return list(self._rows.values())
