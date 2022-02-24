import pytest
import mongomock
import pymongo
from dotenv import load_dotenv, find_dotenv
from todo_app.app import create_app
from todo_app.trello_api_client import TrelloAPIClient
from todo_app.tests.sample_data import sample_trello_boards, sample_trello_card, sample_trello_cards, sample_trello_list, sample_trello_lists
from unittest.mock import patch, Mock

TEST_BOARD_ID = '604153265cd41321654ddebb'
TEST_LIST_ID = '604153265cd41321654ddebc'
TEST_CARD_ID = '605cc4e70c309a11a058f53b'
trello_api_client = TrelloAPIClient()

@pytest.fixture
def client():
    try:
        file_path = find_dotenv('.env.test')
        load_dotenv(file_path, override=True)
    except:
        pass
    
    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = create_app()
        with test_app.test_client() as client:
            yield client

@mongomock.patch(servers=(('fakemongo.com', 27017),))
def test_create_todo_mongo():
    mock_mongo_client = pymongo.MongoClient('fakemongo.com')
    post = {
        'name': 'test',
        'description': 'desc',
        'due_date': '04/04/2022',
        'status': 'To do'
    }
    mock_mongo_client.db.collection.insert_one(post)
    #I guess I need to assert that the collection has a thing in it
    assert mock_mongo_client.db.collection.find({'name':'test'}) != None

@patch('requests.get')
def test_index_page(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_cards
    response = client.get('/')
    assert response.status_code == 200

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
    assert mock_post_requests.call_count == 1
    assert mock_get_requests.call_count == 1
    assert response.status_code in [301,302,303,307,308]

@patch('requests.put')
def test_update_status(mock_put_requests, client):
    mock_put_requests.side_effect = mock_update_card
    response = client.post(f'/update_status/{TEST_BOARD_ID}/{TEST_LIST_ID}/{TEST_CARD_ID}')
    assert mock_put_requests.call_count == 1
    assert response.status_code in [301,302,303,307,308]

@patch('requests.delete')
def test_delete_card(mock_delete_requests, client):
    mock_delete_requests.side_effect = mock_delete_card
    response = client.post(f'/delete/{TEST_BOARD_ID}/{TEST_CARD_ID}')
    assert mock_delete_requests.call_count == 1
    assert response.status_code in [301,302,303,307,308]

def mock_get_cards(url, data):
    if url == f'https://api.trello.com/1/members/me/boards':
        response = Mock()        
        #sample_trello_boards = [{"name":"ToDo App","desc":"","descData":None,"closed":False,"dateClosed":None,"idOrganization":"603ceb6ed1e2db237d5b62cb","idEnterprise":None,"limits":None,"pinned":None,"shortLink":"PN1uMAtI","powerUps":[],"dateLastActivity":"2021-05-11T10:43:00.212Z","idTags":[],"datePluginDisable":None,"creationMethod":"automatic","ixUpdate":None,"enterpriseOwned":False,"idBoardSource":None,"idMemberCreator":"603ceb3cd4d0c98a888e198b","id":"604153265cd41321654ddebb","starred":False,"url":"https://trello.com/b/PN1uMAtI/todo-app","prefs":{"permissionLevel":"private","hideVotes":False,"voting":"disabled","comments":"members","invitations":"members","selfJoin":True,"cardCovers":True,"isTemplate":False,"cardAging":"regular","calendarFeedEnabled":False,"background":"blue","backgroundImage":None,"backgroundImageScaled":None,"backgroundTile":False,"backgroundBrightness":"dark","backgroundColor":"#0079BF","backgroundBottomColor":"#0079BF","backgroundTopColor":"#0079BF","canBePublic":True,"canBeEnterprise":True,"canBeOrg":True,"canBePrivate":True,"canInvite":True},"subscribed":False,"labelNames":{"green":"","yellow":"","orange":"","red":"","purple":"","blue":"","sky":"","lime":"","pink":"","black":""},"dateLastView":"2021-05-11T10:43:00.261Z","shortUrl":"https://trello.com/b/PN1uMAtI","templateGallery":None,"premiumFeatures":[],"memberships":[{"id":"604153265cd41321654ddebf","idMember":"603ceb3cd4d0c98a888e198b","memberType":"admin","unconfirmed":False,"deactivated":False}]}]
        response.json.return_value = sample_trello_boards
        return response

    if url == f'https://api.trello.com/1/boards/{TEST_BOARD_ID}/cards':
        response = Mock()        
        #sample_trello_cards = [{"id":"605cc4e70c309a11a058f53b","checkItemStates":None,"closed":False,"dateLastActivity":"2021-03-25T17:14:15.152Z","desc":"Blah","descData":None,"dueReminder":None,"idBoard":"604153265cd41321654ddebb","idList":"604153265cd41321654ddebc","idMembersVoted":[],"idShort":73,"idAttachmentCover":None,"idLabels":[],"manualCoverAttachment":False,"name":"Test Item","pos":49152,"shortLink":"iYIXXjrN","isTemplate":False,"cardRole":None,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":False,"votes":0,"viewingMemberVoted":False,"subscribed":False,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":None,"comments":0,"attachments":0,"description":True,"due":"2021-03-25T00:00:00.000Z","dueComplete":False,"start":None},"dueComplete":None,"due":"2021-03-25T00:00:00.000Z","idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/iYIXXjrN","start":None,"subscribed":False,"url":"https://trello.com/c/iYIXXjrN/73-test-item","cover":{"idAttachment":None,"color":None,"idUploadedBackground":None,"size":"normal","brightness":"dark","idPlugin":None}}]
        response.json.return_value = sample_trello_cards
        return response

    if url == f'https://api.trello.com/1/lists/{TEST_LIST_ID}':
        response = Mock()        
        #sample_trello_list = {"id": "604153265cd41321654ddebc","name": "To Do","closed": False,"pos": 16384,"idBoard": "604153265cd41321654ddebb"}
        response.json.return_value = sample_trello_list
        return response

    if url == f'https://api.trello.com/1/boards/{TEST_BOARD_ID}/lists':
        response = Mock()        
        #sample_trello_lists = [{"id": "604153265cd41321654ddebc","name": "To Do","closed": False,"pos": 16384,"softLimit": None,"idBoard": "604153265cd41321654ddebb","subscribed": False}]
        response.json.return_value = sample_trello_lists
        return response
    
    return None

def mock_create_card(url, data):
    if url == 'https://api.trello.com/1/cards':
        response = Mock()
        #sample_trello_card = {"id":"605cc4e70c309a11a058f53b","checkItemStates":None,"closed":False,"dateLastActivity":"2021-03-25T17:14:15.152Z","desc":"Blah","descData":None,"dueReminder":None,"idBoard":"604153265cd41321654ddebb","idList":"604153265cd41321654ddebc","idMembersVoted":[],"idShort":73,"idAttachmentCover":None,"idLabels":[],"manualCoverAttachment":False,"name":"Test Item","pos":49152,"shortLink":"iYIXXjrN","isTemplate":False,"cardRole":None,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":False,"votes":0,"viewingMemberVoted":False,"subscribed":False,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":None,"comments":0,"attachments":0,"description":True,"due":"2021-03-25T00:00:00.000Z","dueComplete":False,"start":None},"dueComplete":None,"due":"2021-03-25T00:00:00.000Z","idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/iYIXXjrN","start":None,"subscribed":False,"url":"https://trello.com/c/iYIXXjrN/73-test-item","cover":{"idAttachment":None,"color":None,"idUploadedBackground":None,"size":"normal","brightness":"dark","idPlugin":None}}
        response.json.return_value = sample_trello_card
        return response

    return None

def mock_update_card(url, data):
    if url == f'https://api.trello.com/1/cards/{TEST_CARD_ID}':
        response = Mock()        
        #sample_trello_card = {"id":"605cc4e70c309a11a058f53b","checkItemStates":None,"closed":False,"dateLastActivity":"2021-03-25T17:14:15.152Z","desc":"Blah","descData":None,"dueReminder":None,"idBoard":"604153265cd41321654ddebb","idList":"604153265cd41321654ddebc","idMembersVoted":[],"idShort":73,"idAttachmentCover":None,"idLabels":[],"manualCoverAttachment":False,"name":"Test Item","pos":49152,"shortLink":"iYIXXjrN","isTemplate":False,"cardRole":None,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":False,"votes":0,"viewingMemberVoted":False,"subscribed":False,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":None,"comments":0,"attachments":0,"description":True,"due":"2021-03-25T00:00:00.000Z","dueComplete":False,"start":None},"dueComplete":None,"due":"2021-03-25T00:00:00.000Z","idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/iYIXXjrN","start":None,"subscribed":False,"url":"https://trello.com/c/iYIXXjrN/73-test-item","cover":{"idAttachment":None,"color":None,"idUploadedBackground":None,"size":"normal","brightness":"dark","idPlugin":None}}
        response.json.return_value = sample_trello_card
        return response

    return None

def mock_delete_card(url, data):
    if url == f'https://api.trello.com/1/cards/{TEST_CARD_ID}':
        response = Mock()        
        #sample_trello_card = {"id":"605cc4e70c309a11a058f53b","checkItemStates":None,"closed":False,"dateLastActivity":"2021-03-25T17:14:15.152Z","desc":"Blah","descData":None,"dueReminder":None,"idBoard":"604153265cd41321654ddebb","idList":"604153265cd41321654ddebc","idMembersVoted":[],"idShort":73,"idAttachmentCover":None,"idLabels":[],"manualCoverAttachment":False,"name":"Test Item","pos":49152,"shortLink":"iYIXXjrN","isTemplate":False,"cardRole":None,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":False,"votes":0,"viewingMemberVoted":False,"subscribed":False,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":None,"comments":0,"attachments":0,"description":True,"due":"2021-03-25T00:00:00.000Z","dueComplete":False,"start":None},"dueComplete":None,"due":"2021-03-25T00:00:00.000Z","idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/iYIXXjrN","start":None,"subscribed":False,"url":"https://trello.com/c/iYIXXjrN/73-test-item","cover":{"idAttachment":None,"color":None,"idUploadedBackground":None,"size":"normal","brightness":"dark","idPlugin":None}}
        response.json.return_value = sample_trello_card
        return response

    return None
