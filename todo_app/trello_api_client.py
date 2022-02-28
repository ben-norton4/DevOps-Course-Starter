import os
from dotenv import load_dotenv
import requests
from todo_app.item import Item
from todo_app.trello_board import TrelloBoard
from todo_app.trello_list import TrelloList
from datetime import datetime

class TrelloAPIClient():
    def __init__(self):
        load_dotenv()
        pass

    def create_board(self, name):
        url = 'https://api.trello.com/1/boards/'
        query = {'name': name, 'key': self.get_api_key(), 'token': self.get_api_token()}
        response = requests.post(url, data=query).json()
        board = TrelloBoard(response['id'], response['name'])
        return board

    def create_item(self, list_id, title, description, due_date):
        url = 'https://api.trello.com/1/cards'
        query = {'name': title, 'desc': description, 'due': due_date, 'idList': list_id, 'key': self.get_api_key(), 'token': self.get_api_token()}
        response = requests.post(url, data=query).json()
        card = Item(response['id'], response['name'], response['desc'], self.datetime_formatted_as_date(response['due']), response['idList'], response['idBoard'], self.get_list_name(response['idList']))
        return card

    def get_boards(self):
        url = f'https://api.trello.com/1/members/me/boards'
        query = {'key': self.get_api_key(), 'token': self.get_api_token()}
        response = requests.get(url, data=query).json()
        boards = []
        for board in response:
            boards.append(TrelloBoard(board['id'], board['name']))
        return boards

    def get_lists_on_a_board(self, board_id):
        url = f'https://api.trello.com/1/boards/{board_id}/lists'
        query = {'key': self.get_api_key(), 'token': self.get_api_token()}
        response = requests.get(url, data=query).json()
        lists = []
        for item in response:
            lists.append(TrelloList(item['id'], item['name']))
        return lists

    def get_items_on_a_board(self, board_id):
        url = f'https://api.trello.com/1/boards/{board_id}/cards'
        query = {'key': self.get_api_key(), 'token': self.get_api_token()}
        response = requests.get(url, data=query).json()
        cards = []
        for item in response:
            cards.append(Item(item['id'], item['name'], item['desc'], self.datetime_formatted_as_date(item['due']), item['idList'], item['idBoard'], self.get_list_name(item['idList'])))
        return cards

    def get_list_name(self, list_id):
        url = f'https://api.trello.com/1/lists/{list_id}'
        query = {'key': self.get_api_key(), 'token': self.get_api_token()}
        response = requests.get(url, data=query).json()
        return response['name']

    def update_item_status(self, item_id, list_id):
        url = f"https://api.trello.com/1/cards/{item_id}"
        query = {'idList': list_id, 'key': self.get_api_key(), 'token': self.get_api_token()}
        requests.put(url, data=query)

    def delete_board(self, board_id):
        url = f"https://api.trello.com/1/boards/{board_id}"
        query = {'key': self.get_api_key(), 'token': self.get_api_token()}
        requests.delete(url, data=query)

    def delete_item(self, item_id):
        url = f"https://api.trello.com/1/cards/{item_id}"
        query = {'key': self.get_api_key(), 'token': self.get_api_token()}
        requests.delete(url, data=query)

    @staticmethod
    def get_api_key():
        return os.getenv('TRELLO_API_KEY')

    @staticmethod
    def get_api_token():
        return os.getenv('TRELLO_API_TOKEN')

    @staticmethod
    def datetime_formatted_as_date(date_time):
        if date_time != None:
            date_time = datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d/%m/%Y')
        else:
            date_time = ''
        return date_time