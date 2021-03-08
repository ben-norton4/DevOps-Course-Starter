from todo_app.trello_api_client import TrelloAPIClient
from todo_app.item import Item
from flask import Flask, render_template, request, redirect
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)
trello_api_client = TrelloAPIClient()

todo_app_board = '604153265cd41321654ddebb'
todo_list = '604153265cd41321654ddebc'
doing_list = '604153265cd41321654ddebd'
done_list = '604153265cd41321654ddebe'

@app.route('/')
def index():
    todo_items = trello_api_client.get_items_on_a_board(todo_app_board)
    return render_template('index.html', todo_items = todo_items)

@app.route('/create-todo', methods=['POST'])
def create_todo():
    title = request.form.get('add-item')
    desc = request.form.get('description')
    due = request.form.get('due-date')
    trello_api_client.create_item(todo_list, title, desc, due)
    return redirect('/')

@app.route('/todo/<id>', methods=['POST'])
def todo(id):
    trello_api_client.update_item_status(id, todo_list)
    return redirect('/')

@app.route('/doing/<id>', methods=['POST'])
def doing(id):
    trello_api_client.update_item_status(id, doing_list)
    return redirect('/')

@app.route('/complete_item/<id>', methods=['POST'])
def complete_item(id):
    trello_api_client.update_item_status(id, done_list)
    return redirect('/')

@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    trello_api_client.delete_item(id)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug = True)
