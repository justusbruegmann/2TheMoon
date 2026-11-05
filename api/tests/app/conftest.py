from uuid import uuid4

from pydantic import BaseModel


#################################################################
# Shared testing fixtures for all endpoint tests (since they all need to request from a mocked table):
#################################################################

class FakeTable:
    def __init__(self, model: type[BaseModel], extra_fields=lambda: {}, rows=()):
        self.model = model
        self.extra_fields = extra_fields
        self._rows: dict[str, BaseModel] = {str(row.id): row for row in rows}

    def find(self, limit=None, gt=None, lt=None, **filters):
        rows = list(self._rows.values())
        for column, value in filters.items():
            rows = [r for r in rows if str(getattr(r, column)) == str(value)]
        for column, value in (gt or {}).items():
            rows = [r for r in rows if getattr(r, column) > value]
        for column, value in (lt or {}).items():
            rows = [r for r in rows if getattr(r, column) < value]
        return rows[:limit] if limit else rows

    def get(self, **filters):
        return self._rows.get(str(filters["id"]))

    def insert(self, *rows):
        created = []
        for row in rows:
            fields = self.extra_fields()
            entry = self.model(**row.model_dump(exclude=set(fields)), **fields)
            self._rows[str(fields.get("id", uuid4()))] = entry
            created.append(entry)
        return created

    def update(self, values: dict, **filters):
        key = str(filters["id"])
        row = self._rows.get(key)
        if row is None:
            return []
        updated = row.model_copy(update=values)
        self._rows[key] = updated
        return [updated]

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
