from todo_app.item import TrelloBoard
from todo_app.trello_api_client import TrelloAPIClient
from flask import Flask, render_template, request, redirect
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)

trello_api_client = TrelloAPIClient()
boards = trello_api_client.get_boards()

@app.route('/')
def index():
    selected_board = boards[0]
    selected_board_items = trello_api_client.get_items_on_a_board(selected_board.id)
    selected_board_lists = trello_api_client.get_lists_on_a_board(selected_board.id)
    return render_template('index.html', selected_board = selected_board, selected_board_lists = selected_board_lists, selected_board_items = selected_board_items, boards = boards)

@app.route('/select_board/<id>', methods=['GET'])
def select_board(id):
    for board in boards:
        if board.id == id:
            selected_board = board
            break

    selected_board_items = trello_api_client.get_items_on_a_board(selected_board.id)
    selected_board_lists = trello_api_client.get_lists_on_a_board(selected_board.id)
    return render_template('index.html', selected_board = selected_board, selected_board_lists = selected_board_lists, selected_board_items = selected_board_items, boards = boards)

@app.route('/create-todo/<board_id>', methods=['POST'])
def create_todo(board_id):
    title = request.form.get('title')
    desc = request.form.get('description')
    due = request.form.get('due-date')
    list = request.form.get('list')
    trello_api_client.create_item(list, title, desc, due)
    return redirect(f'/select_board/{board_id}')

@app.route('/update_status/<board_id>/<list_id>/<id>', methods=['POST'])
def update_status(board_id, list_id, id):
    trello_api_client.update_item_status(id, list_id)
    return redirect(f'/select_board/{board_id}')

@app.route('/delete/<board_id>/<id>', methods=['POST'])
def delete(board_id, id):
    trello_api_client.delete_item(id)
    return redirect(f'/select_board/{board_id}')

if __name__ == '__main__':
    app.run(debug = True)
