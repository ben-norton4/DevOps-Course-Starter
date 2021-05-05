class Item():
    def __init__(self, id, name, description, due_date, id_list, id_board, status='To Do'):
        self.id = id
        self.name = name
        self.description = description
        self.due_date = due_date
        self.id_list = id_list
        self.id_board = id_board
        self.status = status

""" class TrelloBoard():
    def __init__(self, id, name):
        self.id = id
        self.name = name

class TrelloList():
    def __init__(self, id, name):
        self.id = id
        self.name = name """
