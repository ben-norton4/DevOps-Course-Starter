from todo_app.trello_list import TrelloList
from todo_app.trello_board import TrelloBoard
import pytest
from todo_app.app import create_app
from todo_app.trello_api_client import TrelloAPIClient
from threading import Thread
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

trello_api_client = TrelloAPIClient()

@pytest.fixture(scope='module')
def app_with_temp_board():
    test_board = trello_api_client.create_board('E2E Test Board')
    application = create_app()
    thread = Thread(target = lambda: application.run(use_reloader = False))
    thread.daemon = True
    thread.start()
    yield application
    thread.join(1)
    trello_api_client.delete_board(test_board.id)

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.headless = True
    with webdriver.Firefox(options = options) as driver:
        driver
        yield driver

def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000')
    assert driver.title == 'To-Do App'



