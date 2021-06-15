class ViewModel:
    def __init__(self, items):
        self._items = items
        self.todo_items = items
        self.doing_items = items
        self.done_items = items

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, items):
        self._items = items

    @property
    def todo_items(self):
        return self._todo_items
    
    @todo_items.setter
    def todo_items(self, items):
        self._todo_items = [item for item in items if item.status.lower() == 'to do']

    @property
    def doing_items(self):
        return self._doing_items

    @doing_items.setter
    def doing_items(self, items):
        self._doing_items = [item for item in items if item.status.lower() == 'doing']

    @property
    def done_items(self):
        return self._done_items
    
    @done_items.setter
    def done_items(self, items):
        self._done_items = [item for item in items if item.status.lower() == 'done']
