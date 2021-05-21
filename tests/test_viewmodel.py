'''Unit Tests for ViewModel'''

import pytest
from datetime import datetime, timedelta, time
from todo_app.view_model import ViewModel
from todo_app.trello_api_calls import TrelloCard


midnight = (datetime.combine(datetime.now(), time.min))
midnight_plus_six = midnight + timedelta(hours=6)
midnight_minus_six = midnight - timedelta(hours=6)

trello_card_list = [
    TrelloCard('T1',1,'Doing',midnight_plus_six.strftime("%Y-%m-%dT%H:%M:%SZ")),
    TrelloCard('T2',2,'Doing',midnight.strftime("%Y-%m-%dT%H:%M:%SZ")),
    TrelloCard('T3',3,'Doing',midnight_minus_six.strftime("%Y-%m-%dT%H:%M:%SZ")),
    TrelloCard('T4',4,'Done',midnight_plus_six.strftime("%Y-%m-%dT%H:%M:%SZ")),
    TrelloCard('T5',5,'Done',midnight.strftime("%Y-%m-%dT%H:%M:%SZ")),
    TrelloCard('T6',6,'Done',midnight_minus_six.strftime("%Y-%m-%dT%H:%M:%SZ")),
    TrelloCard('T7',7,'To Do',midnight_plus_six.strftime("%Y-%m-%dT%H:%M:%SZ")),
    TrelloCard('T8',8,'To Do',midnight.strftime("%Y-%m-%dT%H:%M:%SZ")),
    TrelloCard('T9',9,'To Do',midnight_minus_six.strftime("%Y-%m-%dT%H:%M:%SZ"))
]

@pytest.fixture
def prep_trello_card() -> list:
    return trello_card_list

@pytest.fixture
def prep_view_model(prep_trello_card) -> ViewModel:
    object_viewmodel = ViewModel(prep_trello_card)
    return object_viewmodel

# Testing initial implementation of get_cards
@pytest.mark.parametrize('card_state',['To Do','Doing', 'Done'])
def test_cards(prep_view_model,card_state):
    assert len(prep_view_model.get_cards(card_state)) == 3
    assert (prep_view_model.get_cards(card_state)[0].status) == card_state
    assert (prep_view_model.get_cards(card_state)[1].updated_time) \
        == (midnight)

# Testing decorated version of get_cards
@pytest.mark.parametrize('from_threshold, result',[
    (midnight, 2),
    (midnight + timedelta(hours=5), 1),
    (midnight - timedelta(hours=7), 3)
    ])
def test_get_cards_from_threshold(prep_view_model, from_threshold, result):
    assert len(prep_view_model.get_cards("Done", from_threshold)) == result

@pytest.mark.parametrize('to_threshold, result',[
    (midnight, 1),
    (midnight + timedelta(hours=5), 2),
    (midnight - timedelta(hours=7), 0)
    ])
def test_get_cards_to_threshold(prep_view_model, to_threshold, result):
    assert len(prep_view_model.get_cards("Done", to_threshold=to_threshold)) \
         == result

def test_return_all_done_cards(prep_view_model):
    assert len(prep_view_model.return_all_done_cards(2)) == 4
    assert prep_view_model.return_all_done_cards(2)[0] == False
    assert len(prep_view_model.return_all_done_cards(2)[1]) == 3
    assert len(prep_view_model.return_all_done_cards(2)[2]) == 2
    assert len(prep_view_model.return_all_done_cards(2)[3]) == 1