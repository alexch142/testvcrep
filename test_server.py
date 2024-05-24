import pytest
import app as tested_app
import json


@pytest.fixture
def client():
    tested_app.app.config['TESTING'] = True
    with tested_app.app.test_client() as client:
        yield client


def test_get_hello_endpoint(client):
    r = client.get('/')
    assert r.data == b'Hello World!'


def test_post_hello_endpoint(client):
    r = client.post('/')
    assert r.status_code == 405


def test_get_api_endpoint(client):
    r = client.get('/api')
    assert r.json == {'status': 'test'}


def test_correct_post_api_endpoint(client):
    r = client.post('/api',
                    content_type='application/json',
                    data=json.dumps({'name': 'Den', 'age': 100}))
    assert r.json == {'status': 'OK'}
    assert r.status_code == 200
    
    r = client.post('/api',
                    content_type='application/json',
                    data=json.dumps({'name': 'Den'}))
    assert r.json == {'status': 'OK'}
    assert r.status_code == 200


def test_not_dict_post_api_endpoint(client):
    r = client.post('/api',
                    content_type='application/json',
                    data=json.dumps([{'name': 'Den'}]))
    assert r.json == {'status': 'bad input'}
    assert r.status_code == 400


def test_no_name_post_api_endpoint(client):
    r = client.post('/api',
                    content_type='application/json',
                    data=json.dumps({'age': 100}))
    assert r.json == {'status': 'bad input'}
    assert r.status_code == 400


def test_bad_age_post_api_endpoint(client):
    r = client.post('/api',
                    content_type='application/json',
                    data=json.dumps({'name': 'Den', 'age': '100'}))
    assert r.json == {'status': 'bad input'}
    assert r.status_code == 400
