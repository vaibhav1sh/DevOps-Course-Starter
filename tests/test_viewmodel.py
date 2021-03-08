'''Unit Tests for ViewModel'''

import pytest
from datetime import datetime, timedelta, time
from todo_app.view_model import ViewModel
from todo_app.trello_api_calls import TrelloCard

this_is_midnight = datetime.combine(datetime.now(), time.min)
trello_card_list = [
    TrelloCard('Test1',1,'Doing',this_is_midnight + timedelta(hours=6)),
    TrelloCard('Test2',2,'Doing',this_is_midnight),
    TrelloCard('Test3',3,'Doing',this_is_midnight - timedelta(hours=6)),
    TrelloCard('Test4',4,'Done',this_is_midnight + timedelta(hours=6)),
    TrelloCard('Test5',5,'Done',this_is_midnight),
    TrelloCard('Test6',6,'Done',this_is_midnight - timedelta(hours=6)),
    TrelloCard('Test7',7,'To Do',this_is_midnight + timedelta(hours=6)),
    TrelloCard('Test8',8,'To Do',this_is_midnight),
    TrelloCard('Test9',9,'To Do',this_is_midnight - timedelta(hours=6))
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
        == (this_is_midnight)

# Testing decorated version of get_cards
@pytest.mark.parametrize('from_threshold, result',[ \
    (this_is_midnight, 2), \
        (this_is_midnight + timedelta(hours=5), 1), \
            (this_is_midnight - timedelta(hours=7), 3)])
def test_get_cards_from_threshold(prep_view_model, from_threshold, result):
    assert len(prep_view_model.get_cards("Done", from_threshold)) == result

@pytest.mark.parametrize('to_threshold, result',[ \
    (this_is_midnight, 1), \
        (this_is_midnight + timedelta(hours=5), 2), \
            (this_is_midnight - timedelta(hours=7), 0)])
def test_get_cards_to_threshold(prep_view_model, to_threshold, result):
    assert len(prep_view_model.get_cards("Done", to_threshold=to_threshold)) \
         == result

def test_return_all_done_cards(prep_view_model):
    assert len(prep_view_model.return_all_done_cards(2)) == 4
    assert prep_view_model.return_all_done_cards(2)[0] == False
    assert len(prep_view_model.return_all_done_cards(2)[1]) == 3
    assert len(prep_view_model.return_all_done_cards(2)[2]) == 2
    assert len(prep_view_model.return_all_done_cards(2)[3]) == 1






            # return [show_all_done_cards, all_done_cards, recent_done_cards, \
            # older_done_cards]