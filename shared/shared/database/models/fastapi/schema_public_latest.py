import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

# CUSTOM CLASSES
# Note: These are custom model classes for defining common features among
# Pydantic Base Schema.


class CustomModel(BaseModel):
    """Base model class with common features."""



class CustomModelInsert(CustomModel):
    """Base model for insert operations with common features."""



class CustomModelUpdate(CustomModel):
    """Base model for update operations with common features."""



# BASE CLASSES
# Note: These are the base Row models that include all fields.


class TestingTableBaseSchema(CustomModel):
    """TestingTable Base Schema."""

    # Primary Keys
    id: int

    # Columns
    created_at: datetime.datetime
    field_bool: bool | None = Field(default=None, alias="bool")
    number: Decimal | None = Field(default=None)
    text: str | None = Field(default=None)
    timestamptz: datetime.datetime | None = Field(default=None)


# INSERT CLASSES
# Note: These models are used for insert operations. Auto-generated fields
# (like IDs and timestamps) are optional.


class TestingTableInsert(CustomModelInsert):
    """TestingTable Insert Schema."""

    # Primary Keys

    # Field properties:
    # created_at: has default value
    # field_bool: nullable
    # number: nullable
    # text: nullable
    # timestamptz: nullable

    # Optional fields
    created_at: datetime.datetime | None = Field(default=None)
    field_bool: bool | None = Field(default=None, alias="bool")
    number: Decimal | None = Field(default=None)
    text: str | None = Field(default=None)
    timestamptz: datetime.datetime | None = Field(default=None)


# UPDATE CLASSES
# Note: These models are used for update operations. All fields are optional.


class TestingTableUpdate(CustomModelUpdate):
    """TestingTable Update Schema."""

    # Primary Keys

    # Field properties:
    # created_at: has default value
    # field_bool: nullable
    # number: nullable
    # text: nullable
    # timestamptz: nullable

    # Optional fields
    created_at: datetime.datetime | None = Field(default=None)
    field_bool: bool | None = Field(default=None, alias="bool")
    number: Decimal | None = Field(default=None)
    text: str | None = Field(default=None)
    timestamptz: datetime.datetime | None = Field(default=None)


# OPERATIONAL CLASSES


class TestingTable(TestingTableBaseSchema):
    """TestingTable Schema for Pydantic.

    Inherits from TestingTableBaseSchema. Add any customization here.
    """

