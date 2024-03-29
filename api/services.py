import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


from datetime import date, datetime
from typing import TypedDict
from enum import Enum

from fastapi import HTTPException

import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import func

from db.models import Purchase, Note
from db.database import SessionLocal

from shemas.item import Item
from shemas.notes import NoteSchema


class ItemDict(TypedDict):
    name: str
    total: int
    count: int


class NoteDict(TypedDict):
    title: str
    tag: str
    date: date


class OrderField(str, Enum):
    NAME = "name"
    TOTAL = "total"
    COUNT = "count"
    DESC_NAME = "-name"
    DESC_TOTAL = "-total"
    DESC_COUNT = "-count"


def get_db():
    """
    Создаёт сессию для работы с бд
    """
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()


def add_new_purchases(items: list[Item], db: Session) -> None:
    """
    Добавляет покупки в базу данных
    """
    purchases_list = [
        Purchase(name=item.name.title(), price=item.price, date=item.date)
        for item in items
    ]
    db.add_all(purchases_list)
    db.commit()


def remove_purchase(name: str, db: Session) -> Purchase:
    """
    Удаляет первую покупку с указанным именем из базы данных
    """
    db_purhase = db.query(Purchase).filter(Purchase.name == name).first()
    if db_purhase:
        db.delete(db_purhase)
        db.commit()
    return db_purhase


def get_purchases_with_total(
    db: Session,
    date_start: date | None,
    date_end: date | None,
    limit: int | None,
    order_field: OrderField | None,
) -> list[ItemDict]:
    """
    Возвращает список состоящий из имени покупки общей суммы (которая на неё потрачена) и сколько раз она была сделана
    """
    order = get_order(order_field)

    query = db.query(
        Purchase.name,
        func.sum(Purchase.price).label("total"),
        func.count(Purchase.name).label("count"),
    )

    if date_start:
        query = query.filter(Purchase.date >= date_start)

    if date_end:
        query = query.filter(Purchase.date <= date_end)

    query = query.group_by(Purchase.name).order_by(order)[:limit]

    result = [
        ItemDict(name=item.name, total=item.total, count=item.count) for item in query
    ]
    return result


def get_order(order_field):
    """
    Возвращает asc/desc объект sqlalchemy, который используется для order_by
    """
    if order_field:
        if order_field[0] == "-":
            return sqlalchemy.desc(order_field[1:])
        return sqlalchemy.asc(order_field)
    return sqlalchemy.desc("total")


def validate_items_date(items: list[Item]) -> None:
    """
    Проверяет, чтобы дата объекта была меньше либо равна текущей (не была из будущей)
    """
    current_date = datetime.now().date()
    for item in items:
        if item.date > current_date:
            raise HTTPException(status_code=400, detail="Date is invalid")


def create_pie_chart(db: Session) -> None:
    """
    Создаёт диаграмму на основе 10 самых частовстречающихся покупок и сохраняет её в /pie_images
    """
    query = (
        db.query(Purchase.name, func.count(Purchase.name).label("count"))
        .group_by(Purchase.name)
        .order_by(sqlalchemy.desc("count"))[:10]
    )

    values = [item.count for item in query]
    labels = [f"{item.name} ({item.count})" for item in query]

    plt.pie(values, labels=labels)
    plt.savefig("pie.jpeg")


def add_new_notes(notes: list[NoteSchema], db: Session):
    """
    Добавляет заметки в базу данных
    """

    notes_list = [
        Note(title=note.title.title(), tag=note.tag.lower(), date=note.date)
        for note in notes
    ]

    db.add_all(notes_list)
    db.commit()


def remove_note(db: Session, title: str | None = None, tag: str | None = None):
    """
    Удаляет все заметки по тегу или заголовку, который содержит title
    """
    if tag:
        db.query(Note).filter(Note.tag == tag).delete()
    elif title:
        query = db.query(Note).filter(Note.title.contains(title)).all()
        if query:
            for item in query:
                db.delete(item)

    db.commit()


def get_notes_from_db(
    db: Session, tag: str | None, title: str | None):

    query = db.query(Note)

    if tag:
        query = query.filter(Note.tag == tag.lower())
    if title:
        query = query.filter(Note.title.contains(title))

    result = [
        NoteDict(title=note.title, tag=note.tag, date=note.date) for note in query.all()
    ]

    return result
