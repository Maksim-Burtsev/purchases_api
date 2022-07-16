from datetime import date

from pydantic import BaseModel


class Note(BaseModel):
    title: str
    tag: str | None
    date: date
