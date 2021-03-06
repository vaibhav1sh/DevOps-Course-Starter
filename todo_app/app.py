from flask import Flask, render_template, request, redirect

from todo_app.flask_config import Config
from todo_app.trello_api_calls import fetch_all_cards, change_card_status, \
    TrelloCard

from todo_app.view_model import ViewModel
import requests, os, json

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route('/')
    def index():
        cards = fetch_all_cards("To Do", "Doing", "Done")  
        view_model_obj = ViewModel(cards) 
        return render_template('index.html',
        todo_cards = view_model_obj.get_cards('To Do'),
        doing_cards = view_model_obj.get_cards('Doing'),
        done_cards = view_model_obj.return_all_done_cards(5))

    @app.route('/add-card', methods = ["POST"])
    def add_item():
        title = request.form['title_of_todo']
        status = request.form['status_of_todo']
        if (title != ""):
            TrelloCard.create_card(title, status)
        return redirect("/")

    @app.route('/complete/<id>', methods = ["POST"])
    def complete_item(id): 
        todo_id = request.form['card_id_form']
        change_card_status(todo_id)
        return redirect("/")
    
    return app

wsgi_c = create_app()

if __name__ == '__main__':
    #app.run()
    #create_app().run()
    wsgi_c.run()

