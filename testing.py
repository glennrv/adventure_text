import pickle

valid_users = {
    'Test': {
        'password': '1337',
        'inventory': {

        },
        'fishing level': 1,
        'fishing exp': 0}}

with open("valid_users.pickle", "wb") as vuw:
    pickle.dump(valid_users, vuw)

#with open("valid_users.pickle", "rb") as vur:
#    valid_users = pickle.load(vur)
#    print(valid_users)