import sys
sys.path.append("..")

from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session

from db.models import Base
from db.database import engine
from shemas.item import Item
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
