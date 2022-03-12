from bson.objectid import ObjectId

sample_database_card = {
    '_id': ObjectId(),
    'name': 'test',
    'description': 'desc',
    'due_date': '04/04/2022',
    'status': 'To do'
}

sample_form_input = {
    'title': 'test',
    'description': 'desc',
    'due-date': '2022-04-04',
}