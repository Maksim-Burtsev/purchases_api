from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_add_purchase():

    response = client.post(
        '/add_purchase',
        json={'name': 'test', 'price': 100, 'date': '2022-02-22'}
    )
    assert response.status_code == 201
    assert response.json() == {'date': '2022-02-22',
                               'name': 'test', 'price': 100}


def test_get_purchases():
    response = client.get('/get_purchases')

    assert response.status_code == 200
    assert response.json() == [{'count': 1, 'name': 'Test', 'total': 100}]
#сделать тесты на фильтры

def test_delete_purchase():

    response = client.delete('/delete_purchase/test')

    assert response.status_code == 200
