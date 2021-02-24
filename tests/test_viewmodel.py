'''Unit Tests for ViewModel'''

import pytest
from todo_app.view_model import ViewModel
from todo_app.trello_api_calls import TrelloCard

@pytest.fixture
def prep_trello_card() -> list:
    trello_card_list = []
    trello_card_list.append(TrelloCard('Test1',1,'Doing'))
    trello_card_list.append(TrelloCard('Test2',2,'Doing'))
    trello_card_list.append(TrelloCard('Test3',3,'Done'))
    trello_card_list.append(TrelloCard('Test4',4,'Done'))
    trello_card_list.append(TrelloCard('Test5',5,'To Do'))
    trello_card_list.append(TrelloCard('Test6',6,'To Do'))
    return trello_card_list

@pytest.fixture
def prep_view_model(prep_trello_card) -> ViewModel:
    object_viewmodel = ViewModel(prep_trello_card)
    return object_viewmodel

@pytest.mark.parametrize('card_state',['To Do','Doing', 'Done'])
def test_cards(prep_view_model,card_state):
    assert len(prep_view_model.get_cards(card_state)) == 2
    assert (prep_view_model.get_cards(card_state)[0].status) == card_state