from datetime import date
from typing import TypedDict
from enum import Enum

import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import func

from db.models import Purchase
from db.database import SessionLocal

from shemas.item import Item


class ItemDict(TypedDict):
    name: str
    total: int
    count: int


class OrderField(str, Enum):
    NAME = 'name'
    TOTAL = 'total'
    COUNT = 'count'
    DESC_NAME = '-name'
    DESC_TOTAL = '-total'
    DESC_COUNT = '-count'


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


def remove_purchase(name: str, db: Session) -> Purchase:
    """
    Удаляет первую покупку с указанным именем из базы данных
    """
    db_purhase = db.query(Purchase).filter(Purchase.name == name).first()
    if db_purhase:
        db.delete(db_purhase)
        db.commit()
    return db_purhase


def get_purchases_with_total(db: Session, date_start: date | None,
                             date_end: date | None, limit: int | None,
                             order_field: OrderField | None) -> list[ItemDict]:
    """
    Возвращает список состоящий из имени покупки общей суммы (которая на неё потрачена) и сколько раз она была сделана
    """
    order = get_order(order_field)

    query = db.query(Purchase.name,
                     func.sum(Purchase.price).label('total'),
                     func.count(Purchase.name).label('count'))

    if date_start and date_end:
        query = query.filter(Purchase.date >= date_start,
                             Purchase.date <= date_end)

    query = query.group_by(Purchase.name)\
                 .order_by(order)[:limit]

    result = [ItemDict(name=item.name, total=item.total,
                       count=item.count) for item in query]
    return result


def get_order(order_field):
    """
    Возвращает asc/desc объект sqlalchemy, который используется для order_by
    """
    if order_field:
        if order_field[0] == '-':
            return sqlalchemy.desc(order_field[1:])
        return sqlalchemy.asc(order_field)
    return sqlalchemy.desc('total')
