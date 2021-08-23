from todo_app.trello_api_client import TrelloAPIClient
from todo_app.view_model import ViewModel
from flask import Flask, render_template, request, redirect

trello_api_client = TrelloAPIClient()

def create_app():
    app = Flask(__name__)
    app.config.from_object('todo_app.flask_config.Config')

    @app.route('/')
    def index():
        boards = trello_api_client.get_boards()
        selected_board = boards[0]

        for board in boards:
            if board.name == 'ToDo App':
                selected_board = board
                break
        
        board_id = selected_board.id
        return redirect(f'/select_board/{board_id}')

    @app.route('/select_board/<id>', methods=['GET'])
    def select_board(id):
        boards = trello_api_client.get_boards()
        
        for board in boards:
            if board.id == id:
                selected_board = board
                break

        selected_board_items = trello_api_client.get_items_on_a_board(selected_board.id)
        selected_board_lists = trello_api_client.get_lists_on_a_board(selected_board.id)
        item_view_model = ViewModel(selected_board_items)
        return render_template('index.html', selected_board = selected_board, selected_board_lists = selected_board_lists, view_model = item_view_model, boards = boards)

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

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
