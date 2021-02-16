from flask import Flask, render_template, request, redirect

from todo_app.flask_config import Config

from todo_app.trello_api_calls import fetch_all_items, change_card_status, Item
import requests, os, json

app = Flask(__name__)
app.config.from_object(Config)

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