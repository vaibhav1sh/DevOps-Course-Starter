from flask import Flask, render_template, request, redirect

from todo_app.flask_config import Config

import todo_app.data.session_items as session_items
import requests, os, json

app = Flask(__name__)
app.config.from_object(Config)

api_prefix = 'https://api.trello.com/'

def call_api(api_suffix):
    payload = {'fields':'name','key':os.environ.get('TRELLO_KEY'),'token':os.environ.get('TRELLO_TOKEN')}
    url = api_prefix + api_suffix
    api_response = requests.get(url,params=payload)
    api_response_list = json.loads(json.dumps(api_response.json()))
    return api_response_list

# Fetch board name
api_suffix_get_board = '1/members/vaibhavsharma206/boards'
api_response_list = call_api(api_suffix_get_board)
board_id = api_response_list[0]["id"]

# Fetch all to-do items
api_suffix_get_lists = '1/boards/' + board_id + '/lists'
api_response_list = call_api(api_suffix_get_lists)
for x in api_response_list:
    if x["name"] == "To Do":
        list_id = x["id"]

api_suffix_get_lists = '1/lists/' + list_id + '/cards'
api_response_list = call_api(api_suffix_get_lists)
for x in api_response_list:
    print(x["name"])

# Create new card on to-do list
payload = {'key':os.environ.get('TRELLO_KEY'),'token':os.environ.get('TRELLO_TOKEN'), \
'idList':list_id}
url = api_prefix + '1/cards'
api_response = requests.post(url,params=payload,data = {"name":"To Do New Card"})
api_response_list = json.loads(json.dumps(api_response.json()))

# Move card from to-do to done
payload = {'key':os.environ.get('TRELLO_KEY'),'token':os.environ.get('TRELLO_TOKEN')}
card_id = api_response_list["id"]
url = api_prefix + '1/cards/' + card_id
api_response = requests.put(url,params=payload,data = {"idList":"600f38a6286a445560813144"})
print('PUT response', api_response.status_code)



@app.route('/')
def index():
    todos = session_items.get_items()
    return render_template('index.html',todos=todos)

@app.route('/add-item', methods = ["POST"])
def add_item():
    title = request.form['title_of_todo']
    if (title != ""):
        session_items.add_item(title)
    return redirect("/")

if __name__ == '__main__':
    app.run()