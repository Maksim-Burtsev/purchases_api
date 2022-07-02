from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session

from schemas import Item
from database import engine, SessionLocal
from models import Base, Purchase

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()


@app.post('/add_purchase', status_code=201, response_model=Item)
def add_purchase(item: Item, db: Session = Depends(get_db)):

    purhase = Purchase(name=item.name, price=item.price, date=item.date)
    db.add(purhase)
    db.commit()

    return item
