import pickle

#users = {'user1': {'pass': '12345', 'health': 25, 'gold': 100},
#         'user2': {'pass': '54321', 'health': 52, 'gold': 200}}

#with open("users.pickle", "wb") as upw:
#    pickle.dump(users, upw)

with open("users.pickle", "rb") as upr:
    users = pickle.load(upr)

print(users)

users['user2']['gold'] += 50

print(users)

with open("users.pickle", "wb") as upw:
    pickle.dump(users, upw)

print(users)