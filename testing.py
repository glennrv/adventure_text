import pickle

valid_users = {
    'Admin': {
        'password': '1337',
        'carry': '',
        'inv': {

        },
        'stats': {
            'fishing': {'level': 1, 'exp': 0},
            'hunting': {'level': 1, 'exp': 0},
            'mining': {'level': 1, 'exp': 0}}}}

with open("valid_users.pickle", "wb") as vuw:
    pickle.dump(valid_users, vuw)

#with open("valid_users.pickle", "rb") as vur:
#    valid_users = pickle.load(vur)
#    print(valid_users)