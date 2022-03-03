import os
import pytest
import pymongo
from todo_app.app import create_app
from threading import Thread
from selenium import webdriver
import time

test_item_name = 'E2E Test Item'
test_item_due_date = '01/01/2022'
test_item_description = 'E2E Test Item Description'
os.environ['DATABASE_NAME'] = 'test_todo_app_database'

@pytest.fixture(scope='module')
def app_with_temp_database():
    application = create_app()
    thread = Thread(target = lambda: application.run(use_reloader = False))
    thread.daemon = True
    thread.start()
    yield application
    thread.join(1)
    time.sleep(10)
    mongo_db_client = pymongo.MongoClient(os.getenv('DATABASE_CONNECTION_STRING'))
    mongo_db_client.drop_database(str([os.getenv('DATABASE_NAME')]))

@pytest.fixture(scope='module')
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(options=opts) as driver:
        yield driver

def create_test_item(driver, item_name, due_date, description):
    item_title = driver.find_element_by_name('title')
    item_title.send_keys(item_name)
    item_title = driver.find_element_by_name('due-date')
    item_title.send_keys(due_date)
    item_title = driver.find_element_by_name('description')
    item_title.send_keys(description)
    driver.find_element_by_name('create-to-do-button').click()
    card_title = driver.find_element_by_name('to-do-card-title')
    return card_title

def test_task_journey(driver, app_with_temp_database):
    time.sleep(10)
    driver.get('http://localhost:5000')
    assert driver.title == 'To-Do App'

def test_create_item(driver, app_with_temp_database):
    time.sleep(10)
    card_title = create_test_item(driver, test_item_name, test_item_due_date, test_item_description)
    assert test_item_name in card_title.text
    driver.find_element_by_name('to-do-delete-button').click()

def test_update_item(driver, app_with_temp_database):
    time.sleep(10)
    card_title = create_test_item(driver, test_item_name, test_item_due_date, test_item_description)
    assert test_item_name in card_title.text
    driver.find_element_by_name('to-do-doing-button').click()
    title_text = driver.find_element_by_name('doing-card-title').text
    assert title_text == test_item_name
    driver.find_element_by_name('doing-delete-button').click()

def test_delete_item(driver, app_with_temp_database):
    time.sleep(10)
    card_title = create_test_item(driver, test_item_name, test_item_due_date, test_item_description)
    assert test_item_name in card_title.text
    driver.find_element_by_name('to-do-delete-button').click()
    driver.implicitly_wait(3)
    assert driver.page_source.find(test_item_name) == -1
