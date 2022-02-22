from datetime import datetime

class Item():
    def __init__(self, id, name, description, due_date, status='To Do'):
        self.id = id
        self.name = name
        self.description = description
        self.due_date = due_date
        self.status = status

    @staticmethod
    def datetime_formatted_as_date(date_time):
        if date_time != None or date_time != '':
            date_time = datetime.strptime(date_time, '%Y-%m-%d').strftime('%d/%m/%Y')
        else:
            date_time = ''
        return date_time