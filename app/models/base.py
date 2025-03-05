from typing import Optional, List
from sqlmodel import SQLModel, Field, Column, Integer, String, ForeignKey, Relationship
from ..common.utilities.string import to_camel


class BaseModel(SQLModel):
    """Base SQL model class."""

    id: Optional[int] = Field(
        sa_column=Column("Id", Integer, primary_key=True, autoincrement=True)
    )

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
