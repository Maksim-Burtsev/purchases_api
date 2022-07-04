import sys
from datetime import date

sys.path.append("..")

from fastapi import FastAPI, Depends, Body

from sqlalchemy.orm import Session

from db.models import Base
from db.database import engine
from shemas.item import Item, ItemTotalOutput
from api.services import (
    get_db,
    add_new_purchase,
    remove_purchase,
    get_purchases_with_total,
)


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post('/add_purchase', status_code=201, response_model=Item)
def add_purchase(item: Item, db: Session = Depends(get_db)):
    """Добавление покупки"""
    
    add_new_purchase(item, db)
    return item


@app.delete('/delete_purchase/{name}', status_code=200)
def delete_purchase(name: str, db: Session = Depends(get_db)):
    """Удаление покупки"""

    remove_purchase(name.title(), db)
    return None

@app.post('/get_purchases', response_model=list[ItemTotalOutput | None])
def get_purchases(date_start: date | None = Body(None), 
                    date_end: date | None = Body(None), 
                    db: Session = Depends(get_db)):
    """Получение списка покупок"""
    
    purchases_list = get_purchases_with_total(db, date_start, date_end)
    return purchases_list