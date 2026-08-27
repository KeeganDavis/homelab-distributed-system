from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Event(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: UUID
    event_type: str = Field(min_length=1, max_length=100)
    created_at: datetime
    payload: dict[str, Any]

    @field_validator("event_type")
    @classmethod
    def event_type_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("event_type must not be blank")

        return value

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("created_at must include timezone information")

        return value
