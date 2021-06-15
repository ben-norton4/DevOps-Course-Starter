import pytest

from todo_app.view_model import ViewModel
from todo_app.item import Item

@pytest.fixture
def view_model() -> ViewModel:
    items = [
        Item(1, 'Test to do', None, None, None, None, 'To Do'),
        Item(2, 'Test doing', None, None, None, None, 'Doing'),
        Item(3, 'Test doing II', None, None, None, None, 'Doing'),
        Item(4, 'Test done', None, None, None, None, 'Done'),
        Item(5, 'Test done II', None, None, None, None, 'Done'),
        Item(6, 'Test done III', None, None, None, None, 'Done')
    ]
    view_model = ViewModel(items)
    return view_model

def test_todo_items(view_model):
    assert len(view_model.todo_items) == 1
    assert all([item.status.lower() == 'to do' for item in view_model.todo_items])

def test_doing_items(view_model):
    assert len(view_model.doing_items) == 2
    assert all([item.status.lower() == 'doing' for item in view_model.doing_items])

def test_done_items(view_model):
    assert len(view_model.done_items) == 3
    assert all([item.status.lower() == 'done' for item in view_model.done_items])
