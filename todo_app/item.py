class Item():
    def __init__(self, id, name, description, due_date, status='To Do'):
        self.id = id
        self.name = name
        self.description = description
        self.due_date = due_date
        self.status = status
