from urllib import response
from fastapi.testclient import TestClient

from api.main import app
from db.models import Note
from db.database import SessionLocal


client = TestClient(app)


def test_add_one_note():
    response = client.post(
        "/add_notes",
        json=[{"title": "test", "tag": "tag1", "date": "2022-07-17"}]
    )

    assert response.status_code == 201
    assert response.json() == [
        {'date': '2022-07-17', 'tag': 'tag1', 'title': 'test'}]


def test_add_list_notes():
    response = client.post(
        "/add_notes",
        json=[
            {"title": "test1", "tag": "tag3", "date": "2022-07-17"},
            {"title": "test2", "tag": "tag2", "date": "2022-01-17"},
            {"title": "test3", "tag": "tag1", "date": "2022-11-17"}]
    )

    assert response.status_code == 201
    assert response.json() == [
        {'date': '2022-07-17', 'tag': 'tag3', 'title': 'test1'},
        {'date': '2022-01-17', 'tag': 'tag2', 'title': 'test2'},
        {'date': '2022-11-17', 'tag': 'tag1', 'title': 'test3'}]

def test_wrong_delete():

    response = client.delete('/delete_note')
    assert response.status_code == 400

def test_delete_notes_by_title():
    response = client.delete('/delete_note?title=string')

    assert response.status_code == 200

def test_delete_notes_by_tag():
    db = SessionLocal()
    assert len(db.query(Note).filter(Note.tag=='tag1').all()) == 2

    response = client.delete('/delete_note?tag=tag1')
    assert response.status_code == 200

    assert len(db.query(Note).filter(Note.tag=='tag1').all()) == 0
     

def test_tear_down():
    db = SessionLocal()

    for note in db.query(Note).all():
        db.delete(note)

    db.commit()
