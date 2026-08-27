from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProcessedEvent(BaseModel):
    """In-memory representation of an event after worker processing."""

    model_config = ConfigDict(extra="forbid")

    event_id: UUID
    event_type: str = Field(min_length=1, max_length=100)
    created_at: datetime
    payload: dict[str, Any]
    status: Literal["processed"] = "processed"
