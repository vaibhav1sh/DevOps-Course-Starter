'''Unit Tests for app.py'''

import pytest
from todo_app.trello_api_calls import fetch_all_cards
from todo_app.view_model import ViewModel

@pytest.fixture
def prep_list_of_cards():
    cards = fetch_all_cards("Done")
    return cards

def test_index_func(prep_list_of_cards):
    view_model_obj = ViewModel(prep_list_of_cards)
    todo_cards = view_model_obj.get_cards('Done')
    assert len(todo_cards) == 6