import os
import pytest
import mongomock
import pymongo
from dotenv import load_dotenv, find_dotenv
from todo_app.app import create_app, todo_status, doing_status, done_status
from todo_app.tests.sample_data import sample_database_card, sample_form_input

@pytest.fixture
def client():
    try:
        file_path = find_dotenv('.env.test')
        load_dotenv(file_path, override=True)
    except:
        pass
    
    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = create_app()
        with test_app.test_client() as client:
            yield client

def get_mock_collection():
    mock_mongo_client = pymongo.MongoClient('fakemongo.com')
    db = mock_mongo_client[os.getenv('DATABASE_NAME')]
    collection = db['todo_app_items']
    return collection

def test_index_page(client):
    response = client.get('/')
    assert response.status_code in [301,302,303,307,308]

def test_create_todo(client):
    collection = get_mock_collection()
    response = client.post(f'/create-todo/', data = sample_form_input)
    assert collection.find_one({'name':sample_database_card['name']}) != None
    assert response.status_code in [301,302,303,307,308]

def test_update_todo(client):
    collection = get_mock_collection()
    collection.insert_one(sample_database_card)
    id = str(sample_database_card['_id'])
    response = client.post(f'/todo/{id}')
    card = collection.find_one({'_id':sample_database_card['_id']})
    assert card['status'] == todo_status
    assert response.status_code in [301,302,303,307,308]

def test_update_doing(client):
    collection = get_mock_collection()
    collection.insert_one(sample_database_card)
    id = str(sample_database_card['_id'])
    response = client.post(f'/doing/{id}')
    card = collection.find_one({'_id':sample_database_card['_id']})
    assert card['status'] == doing_status
    assert response.status_code in [301,302,303,307,308]

def test_update_done(client):
    collection = get_mock_collection()
    collection.insert_one(sample_database_card)
    id = str(sample_database_card['_id'])
    response = client.post(f'/done/{id}')
    card = collection.find_one({'_id':sample_database_card['_id']})
    assert card['status'] == done_status
    assert response.status_code in [301,302,303,307,308]

def test_delete_card(client):
    collection = get_mock_collection()
    collection.insert_one(sample_database_card)
    id = str(sample_database_card['_id'])
    response = client.post(f'/delete/{id}')
    card = collection.find_one({'_id':sample_database_card['_id']})
    assert card == None
    assert response.status_code in [301,302,303,307,308]
