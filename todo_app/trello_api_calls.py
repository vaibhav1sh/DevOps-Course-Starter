import os, requests
import dateutil.parser

class TrelloCard:
    def __init__(self,title,id,status,updated_time):
        self.title = title
        self.status = status
        self.id = id
        self.updated_time = \
            (dateutil.parser.isoparse(updated_time)).replace(tzinfo = None)

    def create_card(title, list_category):
        list_id = get_list_id(list_category)
        payload = {
            'key':os.environ.get('TRELLO_KEY'),
            'token':os.environ.get('TRELLO_TOKEN'),
            'idList':list_id
            }
        url = api_prefix + '1/cards'
        card_title = {"name": title}
        api_response = requests.post(url, params=payload, data = card_title)
        api_response_list = api_response.json()
        return TrelloCard(api_response_list["name"], api_response_list["id"], \
            list_category, api_response_list["dateLastActivity"])

api_prefix = 'https://api.trello.com/'

def call_api(api_suffix):
    payload = {'fields': ['name','dateLastActivity'],'key':os.environ.get('TRELLO_KEY'), \
    'token':os.environ.get('TRELLO_TOKEN')}
    url = api_prefix + api_suffix
    api_response = requests.get(url, params=payload)
    api_response_list = api_response.json()
    return api_response_list

def get_board_id():
    api_suffix_get_board = '1/members/' + os.environ.get('TRELLO_USER_NAME')+ '/boards'
    api_response_list = call_api(api_suffix_get_board)
    for x in api_response_list:
        if x["name"] == os.environ.get('TRELLO_BOARD_NAME'):
            board_id = x["id"]
    return board_id  

def get_list_id(list_category):  
    board_id = get_board_id()
    api_suffix_get_lists = '1/boards/' + board_id + '/lists'
    api_response_list = call_api(api_suffix_get_lists)
    for x in api_response_list:
        if x["name"] == list_category:
            list_id = x["id"]
    return list_id

def fetch_all_cards(*args): 
    all_cards_obj = []
    for arg in args:
        list_id = get_list_id(arg)
        api_suffix_get_lists = '1/lists/' + list_id + '/cards'
        all_cards = call_api(api_suffix_get_lists)
        for i, card in enumerate(all_cards):
            all_cards[i] = TrelloCard(all_cards[i]["name"], all_cards[i]["id"], arg, all_cards[i]["dateLastActivity"])
        all_cards_obj.extend(all_cards)
    return all_cards_obj

def change_card_status(card_id,to_state="Done"):
    payload = {'key':os.environ.get('TRELLO_KEY'),'token':os.environ.get('TRELLO_TOKEN')}
    list_id = get_list_id(to_state)
    url = api_prefix + '1/cards/' + card_id
    listdata = {"idList" : list_id}
    requests.put(url,params=payload, data = listdata)

# Written solely for the purpose of testing. 
def create_trello_board():
    payload = {
        'key': os.environ.get('TRELLO_KEY'),
        'token': os.environ.get('TRELLO_TOKEN'),
        'name': os.environ.get('TRELLO_BOARD_NAME_CREATE')
    }
    url = api_prefix + '1/boards/'
    api_response = requests.post(url, params=payload)
    api_response_list = api_response.json()
    return api_response_list

def delete_trello_board(board_id):
    payload = {
        'key': os.environ.get('TRELLO_KEY'),
        'token': os.environ.get('TRELLO_TOKEN')
    }
    url = api_prefix + '1/boards/' + board_id
    api_response = requests.delete(url, params=payload)
    return api_response