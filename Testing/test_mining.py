import random

def chance(t, f):
    """t = True, f = False"""
    luck = []
    for i in range(0, t):
        luck.append(True)
    for i in range(0, f):
        luck.append(False)
    return luck

mine_inventory = {'pickaxe': {
                'stone': {'count': 0, 'wear': 0},
                'iron': {'count': 0, 'wear': 0},
                'gold': {'count': 0, 'wear': 0},
                'diamond': {'count': 0, 'wear': 0}},
             'minerals': {
                 'stone': 0,
                 'iron': 0,
                 'gold': 0,
                 'diamond': 0}}
def equip():
    if command == 'equip stone pixace' and mine_inventoy['pickaxe']['stone']['count'] >= 1:



def mine():
    equiped = ''
    while True:
        command = input('Mine command: ')
        if command == 'leave':
            print('you have left the mine')
            break







while True:
    user = input('command: ')
    if user == 'exit':
        break
    elif user == 'mine':
        mine()





