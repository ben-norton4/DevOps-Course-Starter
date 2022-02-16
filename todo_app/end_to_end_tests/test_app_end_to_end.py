from todo_app.trello_list import TrelloList
from todo_app.trello_board import TrelloBoard
import pytest
from todo_app.app import create_app
from todo_app.trello_api_client import TrelloAPIClient
from threading import Thread
from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.by import By

trello_api_client = TrelloAPIClient()
test_board_name = 'E2E Test Board'
test_item_name = 'E2E Test Item'

@pytest.fixture(scope='module')
def app_with_temp_board():
    test_board = trello_api_client.create_board(test_board_name)
    application = create_app()
    thread = Thread(target = lambda: application.run(use_reloader = False))
    thread.daemon = True
    thread.start()
    yield application
    thread.join(1)
    trello_api_client.delete_board(test_board.id)

@pytest.fixture(scope='module')
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(options=opts) as driver:
        yield driver

def select_test_board(driver):
    driver.get('http://localhost:5000')
    driver.find_element_by_name('select-board').click()
    select_button = driver.find_element_by_name(test_board_name)
    select_button.click()

def create_test_item(driver, item_name):
    item_title = driver.find_element_by_name('title')
    item_title.send_keys(item_name)
    driver.find_element_by_name('select-list').click()
    driver.find_element_by_id('To Do').click()
    card_title = driver.find_element_by_name('todo-card-title')
    return card_title

def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000')
    assert driver.title == 'To-Do App'

def test_select_board(driver, app_with_temp_board):
    select_test_board(driver)
    board_name = driver.find_element_by_name('selected-board-name')
    assert board_name.text == test_board_name

def test_create_item(driver, app_with_temp_board):
    select_test_board(driver)
    board_name = driver.find_element_by_name('selected-board-name')
    assert board_name.text == test_board_name
    card_title = create_test_item(driver, test_item_name)
    assert test_item_name in card_title.text
    driver.find_element_by_name('delete-button').click()

def test_update_item(driver, app_with_temp_board):
    select_test_board(driver)
    board_name = driver.find_element_by_name('selected-board-name')
    assert board_name.text == test_board_name
    card_title = create_test_item(driver, test_item_name)
    assert test_item_name in card_title.text
    driver.find_element_by_name('move-to-list').click()
    driver.find_element_by_name('Done').click()
    assert driver.page_source.find('Done: ' + test_item_name) > 0
    driver.find_element_by_name('delete-button').click()

def test_delete_item(driver, app_with_temp_board):
    select_test_board(driver)
    board_name = driver.find_element_by_name('selected-board-name')
    assert board_name.text == test_board_name
    card_title = create_test_item(driver, test_item_name)
    assert test_item_name in card_title.text
    driver.find_element_by_name('delete-button').click()
    driver.implicitly_wait(3)
    assert driver.page_source.find(test_item_name) == -1
