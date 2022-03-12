from operator import truediv
import os
import requests
from oauthlib.oauth2 import WebApplicationClient
import pymongo
from datetime import datetime
from bson.objectid import ObjectId
from todo_app.item import Item
from todo_app.view_model import ViewModel
from flask import Flask, render_template, request, redirect, session
from flask_login import LoginManager, login_required, UserMixin, login_user, current_user

todo_status = 'To Do'
doing_status = 'Doing'
done_status = 'Done'

#ToDo: change this out to work with a database user-role
writer_user_id = '78470201'

def create_app():
    mongo_db_client = pymongo.MongoClient(os.getenv('DATABASE_CONNECTION_STRING'))
    db = mongo_db_client[os.getenv('DATABASE_NAME')]
    collection = db['todo_app_items']

    app = Flask(__name__)
    app.config.from_object('todo_app.flask_config.Config')
    app.secret_key = os.getenv('SECRET_KEY')
    login_manager = LoginManager()

    web_application_client = WebApplicationClient(os.getenv('CLIENT_ID'))

    class User(UserMixin):
        def __init__(self, id):
            self.id = id
            if id == writer_user_id:
                self.user_role = 'writer'
            else:
                self.user_role = 'reader'

    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(web_application_client.prepare_request_uri('https://github.com/login/oauth/authorize'))
    
    @login_manager.user_loader     
    def load_user(user_id):         
        user = User(user_id)  
        return user
    
    login_manager.init_app(app)

    @app.route('/login/callback', methods=['GET'])
    def login_user_callback():    
        token_url, headers, data = web_application_client.prepare_token_request(
            'https://github.com/login/oauth/access_token', code = request.args['code'], 
            client_id = os.getenv('CLIENT_ID'), client_secret = os.getenv('CLIENT_SECRET')
        )
        
        headers['Accept'] = 'application/json'
        response = requests.post(token_url, headers=headers, data=data)
        web_application_client.parse_request_body_response(response.text)
        access_token = web_application_client.token['access_token']
        header = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('https://api.github.com/user', headers=header).json()
        user_id = response['id']
        user = User(user_id)
        login_user(user)
        return redirect('/')

    def is_writer():
        return current_user.user_role == 'writer'

    @app.route('/')
    @login_required
    def index():
        items = collection.find()
        cards = []
        for item in items:
            cards.append(Item(item['_id'], item['name'], item['description'], item['due_date'].strftime('%d/%m/%Y') , item['status']))
        item_view_model = ViewModel(cards)
        return render_template('index.html', view_model = item_view_model, is_writer = is_writer())

    @app.route('/create-todo/', methods=['POST'])
    def create_todo():
        if not is_writer():
            return redirect('/')
        
        title = request.form.get('title')
        desc = request.form.get('description')
        due = request.form.get('due-date')
        post = {
            'name': title,
            'description': desc,
            'due_date': datetime.fromisoformat(due),
            'status': todo_status
        }
        collection.insert_one(post)
        return redirect('/')

    @app.route('/todo/<id>', methods=['POST'])
    def to_do(id):
        if not is_writer():
            return redirect('/')

        query = {'_id': ObjectId(id)}
        update_values = {'$set': {'status':todo_status}}
        collection.update_one(query, update_values)
        return redirect('/')

    @app.route('/doing/<id>', methods=['POST'])
    def doing(id):
        if not is_writer():
            return redirect('/')

        query = {'_id': ObjectId(id)}
        update_values = {'$set': {'status':doing_status}}
        collection.update_one(query, update_values)
        return redirect('/')

    @app.route('/done/<id>', methods=['POST'])
    def done(id):
        if not is_writer():
            return redirect('/')

        query = {'_id': ObjectId(id)}
        update_values = {'$set': {'status':done_status}}
        collection.update_one(query, update_values)
        return redirect('/')

    @app.route('/delete/<id>', methods=['POST'])
    def delete(id):
        if not is_writer():
            return redirect('/')

        query = {'_id': ObjectId(id)}
        collection.delete_one(query)
        return redirect('/')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
