'''Integration test for app.py'''

import pytest
from dotenv import load_dotenv, find_dotenv
from todo_app.app import create_app
import requests, os
from todo_app import trello_api_calls

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override = True)
    test_app = create_app()

    with test_app.test_client() as client:
        yield client

class MockBoard():
    def __init__(self):
        self.resp = [
            {"name": "my_board_name",
            "id": "600f38a6286a44556081313d"}]
    def json(self):
        return self.resp

class MockList():
    def __init__(self):
        self.resp = [
            {"id": "600f38a6286a445560813140",
            "name": "To Do"},
            {"id": "600f38a6286a445560813141",
            "name": "Doing"},
            {"id": "600f38a6286a445560813144",
            "name": "Done"}]
    def json(self):
        return self.resp

class MockCard():
    def __init__(self):
        self.resp = [
            {"id":"601986528991736637adde6e",
            "name":"This is one of the tasks",
            "dateLastActivity":"2021-02-02T17:05:22.145Z"},
            {"id":"602edfaa1e5d80695594af39",
            "name":"Add new Card in TODO-again",
            "dateLastActivity":"2021-02-18T21:44:10.974Z"},
            {"id":"6036ca7c12d7b740e9ca072f",
            "name":"To Do 3",
            "dateLastActivity":"2021-02-24T21:51:56.358Z"}]
    def json(self):
        return self.resp


@pytest.fixture
def mock_get_requests(monkeypatch):
    def mock_get(url,params):
        if (os.environ.get('TRELLO_USER_NAME') + '/boards') in url:
            return MockBoard()
        elif '1/boards' in url:
            return MockList()
        else:
            return MockCard()
    monkeypatch.setattr(requests, 'get', mock_get)

def test_index_page(mock_get_requests, client):
    
    response = client.get('/')
    assert response.status_code == 200
    assert (b'To Do 3' in response.get_data()) == True
    assert (response.get_data().count(b'This is one of the tasks')) == 3
    assert (response.get_data().count(b'Mark As Complete')) == 6