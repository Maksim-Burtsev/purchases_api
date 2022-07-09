import sys
from datetime import date

sys.path.append("..")

from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.responses import FileResponse

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
    create_pie_chart,
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
                    order_field: OrderField | None = Query(None),
                    db: Session = Depends(get_db)):
    """Получение списка покупок"""
    purchases_list = get_purchases_with_total(
                                db, date_start, date_end, limit, order_field)
    return purchases_list

@app.get('/get_count_pie', status_code=200)
def get_count_pie(user_id: int, db: Session = Depends(get_db)):
    """Возвращает диаграмму на основе 10 самых частовстречающихся покупок"""

    filename = str(user_id)
    create_pie_chart(db, filename)

    return FileResponse(f'pie_images/{filename}.jpeg')

#TODO autodelete img after response