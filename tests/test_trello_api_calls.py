'''
Integration Tests for Trello API - 
create_trello_board() and delete_trello_board() functions
'''

import pytest, os
from dotenv import load_dotenv, find_dotenv
from todo_app.trello_api_calls import create_trello_board, delete_trello_board

def test_create_delete_trello_board():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override = True)
    result = create_trello_board()
    assert len(result) == 13
    test_board_id = result["id"]
    print('ID of the created board', test_board_id)
    assert result["name"] == os.environ.get('TRELLO_BOARD_NAME_CREATE')
    result = delete_trello_board(test_board_id)
    print('Status code for delete request', result.status_code)
    assert result.status_code == 200
