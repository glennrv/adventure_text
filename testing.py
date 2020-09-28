import pickle

valid_users = {
    'Test': {
        'password': '1337',
        'name': 'Test User',
        'dob': '04-20-1337',
        'inventory': {

        },
        'fishing level': 1,
        'fishing exp': 0}}

with open("valid_users.pickle", "wb") as vuw:
    pickle.dump(valid_users, vuw)