import sys
from datetime import date

sys.path.append("..")

from fastapi import FastAPI, Depends, Query, HTTPException

from sqlalchemy.orm import Session

from db.models import Base
from db.database import engine
from shemas.item import Item, ItemTotalOutput
from api.services import (
    get_db,
    add_new_purchases,
    remove_purchase,
    get_purchases_with_total,
    validate_items_date,
    OrderField
)


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post('/add_purchase', status_code=201, response_model=list[Item])
def add_purchase(items: list[Item], db: Session = Depends(get_db)):
    """Добавление покупки"""
    validate_items_date(items)
    add_new_purchases(items, db)
    return items


@app.delete('/delete_purchase/{name}', status_code=200)
def delete_purchase(name: str, db: Session = Depends(get_db)):
    """Удаление покупки"""

    deleted_purhase = remove_purchase(name.title(), db)
    if not deleted_purhase:
        raise HTTPException(status_code=404, detail='Item not found')
        
    return None

@app.get('/get_purchases', response_model=list[ItemTotalOutput | None])
def get_purchases(date_start: date | None = Query(None), 
                    date_end: date | None = Query(None),
                    limit: int | None = Query(None, gt=0), 
                    db: Session = Depends(get_db),
                    order_field: OrderField | None = Query(None)):
    """Получение списка покупок"""
    purchases_list = get_purchases_with_total(
                                db, date_start, date_end, limit, order_field)
    return purchases_list

    #https://stackoverflow.com/questions/55873174/how-do-i-return-an-image-in-fastapi