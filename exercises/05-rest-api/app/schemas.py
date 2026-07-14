from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PostIn(BaseModel):
    user_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1)
    status: Literal["draft", "published"]


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    body: str | None = Field(default=None, min_length=1)
    status: Literal["draft", "published"] | None = None


class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    body: str
    status: str
    created_at: datetime