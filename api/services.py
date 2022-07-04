from datetime import date
from typing import TypedDict

import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import func

from db.models import Purchase
from db.database import SessionLocal

from shemas.item import Item


class ItemDict(TypedDict):
    name: str
    total: int


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
    db_purhase = db.query(Purchase).filter(Purchase.name == name).first()
    print(db_purhase)
    if db_purhase:
        db.delete(db_purhase)
        db.commit()


def get_purchases_with_total(db: Session, date_start: date | None,
                             date_end: date | None) -> list[ItemDict]:
    """
    Возвращает список состоящий из имени покупки и общей суммы, потраченной на неё
    """

    if date_start and date_end:
        query = \
            db.query(Purchase.name,  func.sum(Purchase.price).label('total')) \
            .filter(Purchase.date >= date_start, Purchase.date <= date_end) \
            .group_by(Purchase.name) \
            .order_by(sqlalchemy.desc('total'))

    else:
        query = \
            db.query(Purchase.name,  func.sum(Purchase.price).label('total')) \
            .group_by(Purchase.name) \
            .order_by(sqlalchemy.desc('total'))

    result = [ItemDict(name=item.name, total=item.total) for item in query]

    return result
