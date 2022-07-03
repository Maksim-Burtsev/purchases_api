from datetime import date

from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str
    price: int = Field(..., gt=0)
    date: date 