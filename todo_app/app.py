from flask import Flask, render_template, request, redirect

from todo_app.flask_config import Config

import todo_app.data.session_items as session_items
import requests, os, json

app = Flask(__name__)
app.config.from_object(Config)

# Prepare the API payload, fire API, receive response
payload = {'fields':'name,url','key':os.environ.get('TRELLO_KEY'),'token':os.environ.get('TRELLO_TOKEN')}
api_response = requests.get('https://api.trello.com/1/members/vaibhavsharma206/boards',params=payload)
api_response_str = str(json.dumps(api_response.json()))
api_response_str_clean = api_response_str.rstrip("]").lstrip("[")
api_resonse_dict = json.loads(api_response_str_clean)
# print('Data dict',data["name"])


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
