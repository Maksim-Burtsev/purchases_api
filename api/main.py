import sys
from datetime import date

import sqlalchemy
sys.path.append("..")

from fastapi import FastAPI, Depends, Body

from sqlalchemy.orm import Session
from sqlalchemy import func

from db.models import Base, Purchase
from db.database import engine
from shemas.item import Item, ItemTotalOutput
from api.services import get_db, add_new_purchase, remove_purchase


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

    #TODO in get_query(date_start and date_end)
    if date_start and date_end:
        query = db.query(Purchase.name,  func.sum(Purchase.price).label('total')).filter(Purchase.date>=date_start, Purchase.date<=date_end).group_by(Purchase.name).order_by(sqlalchemy.desc('total'))

    else:
        query = db.query(Purchase.name,  func.sum(Purchase.price).label('total')).group_by(Purchase.name).order_by(sqlalchemy.desc('total'))

    result = [{'name':item.name, 'total':item.total} for item in query]
    
    return result