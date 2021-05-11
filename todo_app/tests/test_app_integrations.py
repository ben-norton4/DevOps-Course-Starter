import pytest
from dotenv import load_dotenv, find_dotenv
from todo_app.app import create_app
from todo_app.trello_api_client import TrelloAPIClient
from unittest.mock import patch, Mock

TEST_BOARD_ID = '604153265cd41321654ddebb'
TEST_LIST_ID = '604153265cd41321654ddebc'
TEST_CARD_ID = '605cc4e70c309a11a058f53b'
trello_api_client = TrelloAPIClient()

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    test_app = create_app()
    with test_app.test_client() as client:
        yield client

@patch('requests.get')
def test_index_page(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_cards
    response = client.get('/')
    assert response.status_code in [301,302,303,307,308]

@patch('requests.get')
def test_select_board(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_cards
    response = client.get(f'/select_board/{TEST_BOARD_ID}')
    assert TEST_CARD_ID in str(response.data)

@patch('requests.post')
@patch('requests.get')
def test_create_todo(mock_get_requests, mock_post_requests, client):
    mock_post_requests.side_effect = mock_create_card
    mock_get_requests.side_effect = mock_get_cards
    response = client.post(f'/create-todo/{TEST_BOARD_ID}')
    assert response.status_code in [301,302,303,307,308]

@patch('requests.put')
@patch('requests.get')
def test_update_status(mock_get_requests, mock_put_requests, client):
    mock_put_requests.side_effect = mock_update_card
    mock_get_requests.side_effect = mock_get_cards
    response = client.post(f'/update_status/{TEST_BOARD_ID}/{TEST_LIST_ID}/{TEST_CARD_ID}')
    assert response.status_code in [301,302,303,307,308]

@patch('requests.delete')
def test_delete_card(mock_delete_requests, client):
    mock_delete_requests.side_effect = mock_delete_card
    response = client.post(f'/delete/{TEST_BOARD_ID}/{TEST_CARD_ID}')
    assert response.status_code in [301,302,303,307,308]

def mock_get_cards(url, data):
    if url == f'https://api.trello.com/1/boards/{TEST_BOARD_ID}/cards':
        response = Mock()        
        sample_trello_cards = [{"id":"605cc4e70c309a11a058f53b","checkItemStates":None,"closed":False,"dateLastActivity":"2021-03-25T17:14:15.152Z","desc":"Blah","descData":None,"dueReminder":None,"idBoard":"604153265cd41321654ddebb","idList":"604153265cd41321654ddebc","idMembersVoted":[],"idShort":73,"idAttachmentCover":None,"idLabels":[],"manualCoverAttachment":False,"name":"Some thing","pos":49152,"shortLink":"iYIXXjrN","isTemplate":False,"cardRole":None,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":False,"votes":0,"viewingMemberVoted":False,"subscribed":False,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":None,"comments":0,"attachments":0,"description":True,"due":"2021-03-25T00:00:00.000Z","dueComplete":False,"start":None},"dueComplete":None,"due":"2021-03-25T00:00:00.000Z","idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/iYIXXjrN","start":None,"subscribed":False,"url":"https://trello.com/c/iYIXXjrN/73-some-thing","cover":{"idAttachment":None,"color":None,"idUploadedBackground":None,"size":"normal","brightness":"dark","idPlugin":None}}]
        response.json.return_value = sample_trello_cards
        return response

    if url == f'https://api.trello.com/1/lists/{TEST_LIST_ID}':
        response = Mock()        
        sample_trello_list = {"id": "604153265cd41321654ddebc","name": "To Do","closed": False,"pos": 16384,"idBoard": "604153265cd41321654ddebb"}
        response.json.return_value = sample_trello_list
        return response

    if url == f'https://api.trello.com/1/boards/{TEST_BOARD_ID}/lists':
        response = Mock()        
        sample_trello_lists = [{"id": "604153265cd41321654ddebc","name": "To Do","closed": False,"pos": 16384,"softLimit": None,"idBoard": "604153265cd41321654ddebb","subscribed": False}]
        response.json.return_value = sample_trello_lists
        return response
    
    return None

def mock_create_card(url, data):
    if url == 'https://api.trello.com/1/cards':
        response = Mock()        
        sample_trello_card = {"id":"605cc4e70c309a11a058f53b","checkItemStates":None,"closed":False,"dateLastActivity":"2021-03-25T17:14:15.152Z","desc":"Blah","descData":None,"dueReminder":None,"idBoard":"604153265cd41321654ddebb","idList":"604153265cd41321654ddebc","idMembersVoted":[],"idShort":73,"idAttachmentCover":None,"idLabels":[],"manualCoverAttachment":False,"name":"Some thing","pos":49152,"shortLink":"iYIXXjrN","isTemplate":False,"cardRole":None,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":False,"votes":0,"viewingMemberVoted":False,"subscribed":False,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":None,"comments":0,"attachments":0,"description":True,"due":"2021-03-25T00:00:00.000Z","dueComplete":False,"start":None},"dueComplete":None,"due":"2021-03-25T00:00:00.000Z","idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/iYIXXjrN","start":None,"subscribed":False,"url":"https://trello.com/c/iYIXXjrN/73-some-thing","cover":{"idAttachment":None,"color":None,"idUploadedBackground":None,"size":"normal","brightness":"dark","idPlugin":None}}
        response.json.return_value = sample_trello_card
        return response

    return None

def mock_update_card(url, data):
    if url == f'https://api.trello.com/1/cards/{TEST_CARD_ID}':
        response = Mock()        
        sample_trello_card = {"id":"605cc4e70c309a11a058f53b","checkItemStates":None,"closed":False,"dateLastActivity":"2021-03-25T17:14:15.152Z","desc":"Blah","descData":None,"dueReminder":None,"idBoard":"604153265cd41321654ddebb","idList":"604153265cd41321654ddebc","idMembersVoted":[],"idShort":73,"idAttachmentCover":None,"idLabels":[],"manualCoverAttachment":False,"name":"Some thing","pos":49152,"shortLink":"iYIXXjrN","isTemplate":False,"cardRole":None,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":False,"votes":0,"viewingMemberVoted":False,"subscribed":False,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":None,"comments":0,"attachments":0,"description":True,"due":"2021-03-25T00:00:00.000Z","dueComplete":False,"start":None},"dueComplete":None,"due":"2021-03-25T00:00:00.000Z","idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/iYIXXjrN","start":None,"subscribed":False,"url":"https://trello.com/c/iYIXXjrN/73-some-thing","cover":{"idAttachment":None,"color":None,"idUploadedBackground":None,"size":"normal","brightness":"dark","idPlugin":None}}
        response.json.return_value = sample_trello_card
        return response

    return None

def mock_delete_card(url, data):
    if url == f'https://api.trello.com/1/cards/{TEST_CARD_ID}':
        response = Mock()        
        sample_trello_card = {"id":"605cc4e70c309a11a058f53b","checkItemStates":None,"closed":False,"dateLastActivity":"2021-03-25T17:14:15.152Z","desc":"Blah","descData":None,"dueReminder":None,"idBoard":"604153265cd41321654ddebb","idList":"604153265cd41321654ddebc","idMembersVoted":[],"idShort":73,"idAttachmentCover":None,"idLabels":[],"manualCoverAttachment":False,"name":"Some thing","pos":49152,"shortLink":"iYIXXjrN","isTemplate":False,"cardRole":None,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":False,"votes":0,"viewingMemberVoted":False,"subscribed":False,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":None,"comments":0,"attachments":0,"description":True,"due":"2021-03-25T00:00:00.000Z","dueComplete":False,"start":None},"dueComplete":None,"due":"2021-03-25T00:00:00.000Z","idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/iYIXXjrN","start":None,"subscribed":False,"url":"https://trello.com/c/iYIXXjrN/73-some-thing","cover":{"idAttachment":None,"color":None,"idUploadedBackground":None,"size":"normal","brightness":"dark","idPlugin":None}}
        response.json.return_value = sample_trello_card
        return response

    return None
