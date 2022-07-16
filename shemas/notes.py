from datetime import date

from pydantic import BaseModel


class NoteSchema(BaseModel):
    title: str
    tag: str | None
    date: date
