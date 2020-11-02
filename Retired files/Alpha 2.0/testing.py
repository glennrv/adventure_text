import pickle

valid_users = {
    'Admin': {
        'password': '1337',
        'carry': '',
        'coins': 0,
        'inv': {

        },
        'stats': {
            'fishing': {'level': 1, 'exp': 0},
            'hunting': {'level': 1, 'exp': 0},
            'mining': {'level': 1, 'exp': 0}}}}

with open("valid_users.pickle", "wb") as vuw:
    pickle.dump(valid_users, vuw)

vendors = {'blacksmith': {'pickaxe': 0,
                          'ore': 0},
           'carpenter': {'hatchet': 0,
                         'logs': 0},
           'fisherman': {'small net': {'stock': 2, 'buy': 0, 'sell': 0},
                         'harpoon': {'stock': 1, 'buy': 50, 'sell': 10},
                         'fishing rod': {'stock': 1, 'buy': 200, 'sell': 50},
                         'shrimp': {'stock': 0, 'buy': 2, 'sell': 1},
                         'tuna': {'stock': 0, 'buy': 4, 'sell': 2},
                         'herring': {'stock': 0, 'buy': 8, 'sell': 4},
                         'anchovies': {'stock': 0, 'buy': 16, 'sell': 8},
                         'trout': {'stock': 0, 'buy': 32, 'sell': 16},
                         'swordfish': {'stock': 0, 'buy': 128, 'sell': 64}}}

with open("vendors.pickle", "wb") as vw:
    pickle.dump(vendors, vw)

#with open("valid_users.pickle", "rb") as vur:
#    valid_users = pickle.load(vur)
#    print(valid_users)