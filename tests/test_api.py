import datetime
from pydoc import cli

from fastapi.testclient import TestClient

from api.main import app
from db.database import SessionLocal 
from db.models import Purchase


client = TestClient(app)


def test_add_one_purchase():

    response = client.post(
        '/add_purchase',
        json=[{'name': 'test', 'price': 100, 'date': '2022-02-22'}]
    )
    assert response.status_code == 201
    assert response.json() == [
        {'date': '2022-02-22', 'name': 'test', 'price': 100}]


def test_add_list_purchases():

    response = client.post(
        '/add_purchase',
        json=[{'name': 'test', 'price': 100, 'date': '2022-02-23'},
        {'name': 'test2', 'price': 777, 'date': '2022-02-24'}, {'name': 'test', 'price': 333, 'date': '2022-02-25'}]
    )

    assert response.status_code == 201
    assert response.json() == [{'date': '2022-02-23', 'name': 'test', 'price': 100}, {'date': '2022-02-24', 'name': 'test2', 'price': 777}, {'date': '2022-02-25', 'name': 'test', 'price': 333}]

def test_wrong_add_purchase_wrong_date():

    tomorrow = str(datetime.datetime.now().date() + datetime.timedelta(days=1))
    response = client.post(
        '/add_purchase',
        json=[{'name': 'test', 'price': 1721, 'date': tomorrow}]
    )

    assert response.status_code == 400

def test_get_purchases():

    response = client.get('/get_purchases')

    assert response.status_code == 200
    assert response.json() == [{'count': 1, 'name': 'Test2', 'total': 777}, {'count': 3, 'name': 'Test', 'total': 533}]

def test_get_purchases_with_date():
    response = client.get(
        '/get_purchases?date_start=2022-02-23&date_end=2022-02-24'
    )

    assert response.status_code == 200
    assert response.json() == [{'count': 1, 'name': 'Test2', 'total': 777}, {'count': 1, 'name': 'Test', 'total': 100}]
    

def test_get_purchases_with_date2():
    response = client.get(
        '/get_purchases?date_start=2022-02-26&date_end=2022-03-01'
    )

    assert response.status_code == 200
    assert response.json() == []

def test_get_purchases_with_order_desc():
    
    response = client.get('/get_purchases?order_field=-total')

    assert response.status_code == 200
    assert response.json() == [{'count': 1, 'name': 'Test2', 'total': 777}, {'count': 3, 'name': 'Test', 'total': 533}]

def test_get_purchases_with_order_asc():
    
    response = client.get('/get_purchases?order_field=count')

    assert response.status_code == 200
    assert response.json() == [{'count': 1, 'name': 'Test2', 'total': 777}, {'count': 3, 'name': 'Test', 'total': 533}]

def test_get_purchases_limit():

    response = client.get('/get_purchases?limit=1')

    assert response.status_code == 200
    assert response.json() == [{'count': 1, 'name': 'Test2', 'total': 777}]
    

def test_delete_purchase():

    response = client.delete('/delete_purchase/test2')

    assert response.status_code == 200
    assert response.json() == None

    #see is the test2 deleted
    response = client.get('/get_purchases')
    assert response.status_code == 200
    assert response.json() == [{'count': 3, 'name': 'Test', 'total': 533}]

def test_tear_down():
    
    session = SessionLocal()

    purchases = session.query(Purchase).all()
    
    for purchase in purchases:
        session.delete(purchase)

    session.commit()
