from decimal import Decimal
from uuid import UUID, uuid4

import pytest

from app.domain.holding import holdings_patch_one, holdings_post_one
from app.util.response import DomainError
from shared.database.models import Holding, HoldingUpdate
from ..conftest import FakeTable

VALID_PAYLOAD = {
    "portfolio_id": str(uuid4()),
    "asset_id": str(uuid4()),
    "quantity": "1.5",
}


class FakeDatabase:
    def __init__(self):
        self.holdings = FakeTable(Holding, lambda: {"id": uuid4()})


###################
# Unit Tests
#
# holdings_post_one and holdings_patch_one are not mapped to a routing endpoint (yet),
# so they are tested directly here instead of through the API in tests/app/routers.
###################

def test_post_one_creates_holding():
    db = FakeDatabase()

    created = holdings_post_one(db, Holding(**VALID_PAYLOAD))

    assert created.quantity == Decimal("1.5")


def test_patch_one_updates_existing_holding():
    db = FakeDatabase()
    db.holdings.insert(Holding(**VALID_PAYLOAD))
    holding_id = UUID(next(iter(db.holdings._rows)))

    updated = holdings_patch_one(db, holding_id, HoldingUpdate(quantity=Decimal("5")))

    assert updated.quantity == Decimal("5")


def test_patch_one_no_fields_raises_400():
    db = FakeDatabase()

    with pytest.raises(DomainError) as exc_info:
        holdings_patch_one(db, uuid4(), HoldingUpdate())

    assert exc_info.value.status_code == 400


def test_patch_one_unknown_id_raises_404():
    db = FakeDatabase()

    with pytest.raises(DomainError) as exc_info:
        holdings_patch_one(db, uuid4(), HoldingUpdate(quantity=Decimal("5")))

    assert exc_info.value.status_code == 404
