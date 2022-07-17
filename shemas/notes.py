from datetime import date

from pydantic import BaseModel, Field


class NoteSchema(BaseModel):
    title: str
    tag: str | None = Field(None)
    date: date
