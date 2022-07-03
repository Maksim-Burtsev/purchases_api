import sys
sys.path.append("..")

from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session

from db.models import Base, Purchase
from db.database import engine, SessionLocal
from shemas.item import Item


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()


def add_new_purchase(item: Item, db: Session) -> Purchase:

    db_purhase = Purchase(name=item.name.title(),
                          price=item.price,
                          date=item.date)
    db.add(db_purhase)
    db.commit()
    db.refresh(db_purhase)
    return db_purhase


def remove_purchase(name: str, db: Session):
    db_purhase = db.query(Purchase).filter(Purchase.name == name.title()).first()
    print(db_purhase)
    if db_purhase:
        db.delete(db_purhase)
        db.commit()


@app.post('/add_purchase', status_code=201, response_model=Item)
def add_purchase(item: Item, db: Session = Depends(get_db)):

    add_new_purchase(item, db)
    return item


@app.delete('/delete_purchase/{name}', status_code=200)
def delete_purchase(name: str, db: Session = Depends(get_db)):
    remove_purchase(name, db)
    return None
