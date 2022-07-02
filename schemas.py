from datetime import date


from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: int
    date: date
