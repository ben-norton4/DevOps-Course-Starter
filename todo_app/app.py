import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from todo_app.trello_api_client import TrelloAPIClient
from todo_app.item import Item
from todo_app.view_model import ViewModel
from flask import Flask, render_template, request, redirect

trello_api_client = TrelloAPIClient()
mongo_db_client = MongoClient(os.getenv('DATABASE_CONNECTION_STRING'))
db = mongo_db_client[os.getenv('DATABASE_NAME')]
collection = db['todo_app_items']
todo_status = 'To Do'
doing_status = 'Doing'
done_status = 'Done'

def create_app():
    app = Flask(__name__)
    app.config.from_object('todo_app.flask_config.Config')
    @app.route('/')
    def index():
        items = collection.find()
        cards = []
        for item in items:
            cards.append(Item(item['_id'], item['name'], item['description'], item['due_date'], item['status']))
        item_view_model = ViewModel(cards)
        return render_template('index.html', view_model = item_view_model)

    @app.route('/create-todo/', methods=['POST'])
    def create_todo():
        title = request.form.get('title')
        desc = request.form.get('description')
        due = request.form.get('due-date')
        post = {
            'name': title,
            'description': desc,
            'due_date': Item.datetime_formatted_as_date(due),
            'status': todo_status
        }
        print(title)
        collection.insert_one(post)
        return redirect('/')

    @app.route('/to-do/<id>', methods=['POST'])
    def to_do(id):
        query = {'_id': ObjectId(id)}
        update_values = {'$set': {'status':todo_status}}
        collection.update_one(query, update_values)
        return redirect('/')

    @app.route('/doing/<id>', methods=['POST'])
    def doing(id):
        query = {'_id': ObjectId(id)}
        update_values = {'$set': {'status':doing_status}}
        collection.update_one(query, update_values)
        return redirect('/')

    @app.route('/done/<id>', methods=['POST'])
    def done(id):
        query = {'_id': ObjectId(id)}
        update_values = {'$set': {'status':done_status}}
        collection.update_one(query, update_values)
        return redirect('/')

    @app.route('/delete/<id>', methods=['POST'])
    def delete(id):
        query = {'_id': ObjectId(id)}
        collection.delete_one(query)
        return redirect('/')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
