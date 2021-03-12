'''Unit Tests for ViewModel'''

import pytest, os
from todo_app.trello_api_calls import create_trello_board

def test_create_trello_board():
    result = create_trello_board()
    assert len(result) == 13
    assert result["name"] == os.environ.get('TRELLO_TEST_BOARD_NAME')