from flask import Flask, render_template, request, redirect

from todo_app.flask_config import Config

import todo_app.data.session_items as session_items
import requests, os, json

app = Flask(__name__)
app.config.from_object(Config)

class Item:
    def __init__(self,title,id,status):
        self.title = title
        self.status = status
        self.id = id

    def create_card(title, list_category):
        list_id = get_list_id(list_category)
        payload = {'key':os.environ.get('TRELLO_KEY'),'token':os.environ.get('TRELLO_TOKEN'), \
        'idList':list_id}
        url = api_prefix + '1/cards'
        card_title = {"name": title}
        api_response = requests.post(url, params=payload, data = card_title)
        api_response_list = json.loads(json.dumps(api_response.json()))
        return Item(api_response_list["name"],api_response_list["id"], list_category)
     
api_prefix = 'https://api.trello.com/'

def call_api(api_suffix):
    payload = {'fields':'name','key':os.environ.get('TRELLO_KEY'),'token':os.environ.get('TRELLO_TOKEN')}
    url = api_prefix + api_suffix
    api_response = requests.get(url, params=payload)
    api_response_list = json.loads(json.dumps(api_response.json()))
    return api_response_list

def get_board_id():
    api_suffix_get_board = '1/members/vaibhavsharma206/boards'
    api_response_list = call_api(api_suffix_get_board)
    return api_response_list[0]["id"]  

def get_list_id(list_category):  
    board_id = get_board_id()
    api_suffix_get_lists = '1/boards/' + board_id + '/lists'
    api_response_list = call_api(api_suffix_get_lists)
    for x in api_response_list:
        if x["name"] == list_category:
            list_id = x["id"]
    return list_id

def fetch_all_items(*args): 
    all_cards_obj = []
    for arg in args:
        list_id = get_list_id(arg)
        api_suffix_get_lists = '1/lists/' + list_id + '/cards'
        all_cards = call_api(api_suffix_get_lists)
        for i, card in enumerate(all_cards):
            all_cards[i] = Item(all_cards[i]["name"], all_cards[i]["id"], arg)
        all_cards_obj.extend(all_cards)
    return all_cards_obj

def change_card_status(card_id,to_state="Done"):
    payload = {'key':os.environ.get('TRELLO_KEY'),'token':os.environ.get('TRELLO_TOKEN')}
    list_id = get_list_id(to_state)
    url = api_prefix + '1/cards/' + card_id
    listdata = {"idList" : list_id}
    api_response = requests.put(url,params=payload, data = listdata)


@app.route('/')
def index():
    todos = fetch_all_items("To Do", "Doing", "Done")  
    return render_template('index.html',todos = todos)

@app.route('/add-item', methods = ["POST"])
def add_item():
    title = request.form['title_of_todo']
    status = request.form['status_of_todo']
    if (title != ""):
        Item.create_card(title, status)
    return redirect("/")

@app.route('/complete/<id>', methods = ["POST"])
def complete_item(id): 
    todo_id = request.form['todo_id']
    change_card_status(todo_id)
    return redirect("/")

if __name__ == '__main__':
    app.run()