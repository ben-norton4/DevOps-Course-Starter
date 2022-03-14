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

def create_app():
    mongo_db_client = pymongo.MongoClient(os.getenv('DATABASE_CONNECTION_STRING'))
    db = mongo_db_client[os.getenv('DATABASE_NAME')]
    collection = db['todo_app_items']
    users_collection = db['users']

    app = Flask(__name__)
    app.config.from_object('todo_app.flask_config.Config')
    app.secret_key = os.getenv('SECRET_KEY')
    login_manager = LoginManager()

    web_application_client = WebApplicationClient(os.getenv('CLIENT_ID'))

    class User(UserMixin):
        def __init__(self, id):
            self.github_id = id

    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(web_application_client.prepare_request_uri('https://github.com/login/oauth/authorize'))
    
    @login_manager.user_loader     
    def load_user(user_id):         
        user = User(user_id)
        query = {'github_id': user_id}
        db_user = users_collection.find_one(query)
        user.name = db_user['name']
        user.user_role = db_user['user_role']
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
        github_id = response['id']
        
        query = {'github_id': github_id}
        db_user = users_collection.find_one(query)
        
        if(db_user) == None:
            items = collection.find()
            if(items.count() == 0):
                user_role = 'admin'
            else:
                user_role = 'reader'
            
            post = {
                'name': response['login'],
                'github_id': github_id,
                'user_role': user_role
            }
            users_collection.insert_one(post)
            db_user = users_collection.find_one(query)

        user = User(db_user['github_id'])
        login_user(user.github_id)
        return redirect('/')

    def is_writer():
        return current_user.user_role == 'writer'

    def is_admin():
        return current_user.user_role == 'admin'

    @app.route('/')
    @login_required
    def index():
        items = collection.find()
        cards = []
        for item in items:
            cards.append(Item(item['_id'], item['name'], item['description'], item['due_date'].strftime('%d/%m/%Y') , item['status']))
        item_view_model = ViewModel(cards)
        return render_template('index.html', view_model = item_view_model, is_writer = is_writer(), is_admin = is_admin())

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

    @app.route('/users', methods=['GET'])
    def users():
        db_users = users_collection.find()
        users = []
        for item in db_users:
            user = User(item['github_id'])
            user.name = item['name']
            user.user_role = item['user_role']
            users.append(user)
        return render_template('users.html', users=users)

    @app.route('/update-user-role/<id>/<user_role>', methods=['POST'])
    def update_user_role(id, user_role):
        if not is_admin():
            return redirect('/')

        query = {'github_id': id}
        update_values = {'$set': {'user_role':user_role}}
        users_collection.update_one(query, update_values)
        return redirect('/users')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
