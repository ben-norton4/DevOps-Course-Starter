from flask import Flask, render_template, request, redirect
from todo_app.data.session_items import get_items, add_item, delete_item, get_item, save_item
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    todo_items = sorted(get_items(), key=lambda items: items['status'], reverse = True)
    return render_template('index.html', todo_items = todo_items)

@app.route('/', methods=['POST'])
def add_todo_item():
    title = request.form.get('add-item')
    add_item(title)
    return redirect('/')

@app.route('/complete/<id>', methods=['POST'])
def complete(id):
    item = get_item(id)
    item['status'] = 'Completed'
    save_item(item)
    return redirect('/')

@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    delete_item(id)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug = True)
