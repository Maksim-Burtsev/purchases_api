from sqlalchemy.orm import Session

from db.models import Purchase
from db.database import SessionLocal

from shemas.item import Item


def get_db():
    """
    Создаёт сессию для работы с бд
    """
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()


def add_new_purchase(item: Item, db: Session) -> Purchase:
    """
    Добавляет покупку в базу данных
    """
    db_purhase = Purchase(name=item.name.title(),
                          price=item.price,
                          date=item.date)
    db.add(db_purhase)
    db.commit()
    db.refresh(db_purhase)
    return db_purhase


def remove_purchase(name: str, db: Session):
    """
    Удаляет первую покупку с указанным именем из базы данных
    """
    db_purhase = db.query(Purchase).filter(Purchase.name==name).first()
    print(db_purhase)
    if db_purhase:
        db.delete(db_purhase)
        db.commit()