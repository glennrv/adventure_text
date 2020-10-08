# This is just used for testing various solutions
# that may or may not be implemented into the main
# game.

import random
import pickle
import math
import pprint
from time import sleep


def fish():
    """Function for the fishing skill"""
    # Area - The Docks
    # Fish lvl, fish xp, tool, fish type, success rate, xp gain, lvl up

    print('You head to the docks.')
    area = 'The docks'
    avaliable_commands = {**command_prompts['global'], **command_prompts[area]}

    fishing = user['stats']['fishing']
    lvl = fishing['level']
    xp = fishing['exp']

    while True:
        command_raw = input(f'[{area}]Command: ').lower()
        command = command_raw.split()
        if command_raw == 'leave':
            print('You head back to the Town Square.')
            break
        elif command[0] in avaliable_commands:
            if len(command) == 1:
                avaliable_commands[command[0]]()
            elif len(command) == 2:
                try:
                    avaliable_commands[command[0]][command[1]]()
                except TypeError:
                    try:
                        avaliable_commands[command[0]](command[1])
                    except TypeError:
                        print('Unknown command.')
            elif len(command) == 3:
                try:
                    avaliable_commands[command[0]][command[1]][command[2]]()
                except TypeError:
                    try:
                        avaliable_commands[command[0]][command[1]](command[2])
                    except TypeError:
                        print('Unknown command.')
        else:
            print('Unknown command.')

def start_fishing():
    tool = user['carry']
    valid_tools = ['small net', 'spear', 'fishing rod']
    tool_modifiers = {'small net': 1, 'spear': 5, 'fishing rod': 10}
    if tool in valid_tools:
        print(f'You start fishing with your {tool}.')
        while True:
            atempt = random.randint(1, 100)
            chance = (math.atan(lvl/tool_modifiers[tool]) - 0.58) * 100
    else:
        return print('You have to equip a valid tool before you can start fishing.')

def options_fishing():
    print("""   Level   -    Tools    -   Catch
       1   -  Small net  -   Shrimp
       5   -   Spear     -   Tuna
      10   - Fishing rod -   Salmon""")


def hunt():
    print('You go hunting')
def mine():
    print('You go mining')
def shop():
    print('You go to the market')
def check_inv():
    print(user['inv'])
def check_stats():
    pprint.pprint(user['stats'])
def check_skill(skill):
    print(user['stats'][skill])
def check_carry():
    print(user['carry'])
def help_local():
    print(f'Helpmenu for {area}')
def equip(tool):
    if tool in user['inv']:
        user['carry'] = tool
        return user
    else:
        return print('You do not have this tool in your inventory.')
def unequip():
    user['carry'] = ''
    return user

command_prompts = {
    'global': {
        'help': help_local,             # 'help' - prints a help menu for the local area
        'check': {
            'stats': check_stats,       # 'check stats' - prints the lvl of every skill
            'inv': check_inv,           # 'check inv' - prints the content of your inventory
            'skill': check_skill,       # 'check skill (fishing, hunting, mining)' - prints your level and experience in a specific skill
            'carry': check_carry
        },
        'equip': equip,                 # 'equip (tool)' - equips a tool to carry
        'unequip': unequip              # 'unequip' - unequips carry
    },
    'Town square': {
        'go': {
            'fish': fish,               # 'go fish' - initiates fishing
            'hunt': hunt,               # 'go hunt' - initiates hunting
            'mine': mine,               # 'go mine' - initiates mining
            'trade': shop
        },
    },
    'The docks': {
        'fish': start_fishing,
        'options': options_fishing
    },
    'The woods': {

    },
    'The mine': {

    }
}
users = {
    'User1': {
        'password': '12345',
        'carry': '',
        'inv': {
            'fish': 13,
            'ore': 25,
            'meat': 17,
            'fishing rod': 1
        },
        'stats': {
            'fishing': {'level': 1, 'exp': 0},
            'hunting': {'level': 1, 'exp': 0},
            'mining': {'level': 1, 'exp': 0}}}
}


# Main menu screen - used for logging in to the game
while True:
    area = 'Main menu'
    username = input('Username: ')
    if username.lower() == 'quit':
        print('You have left the game.')
        break

    password = input('Password: ')
    if username in users and password == users[username]['password']:
        user = users[username]
        print(f'Welcome {username}!')

        # Actual Game Loop
        while True:
            area = 'Town square'
            avaliable_commands = {**command_prompts['global'], **command_prompts[area]}
            command_raw = input('Command: ').lower()
            command = command_raw.split()
            if command[0] == 'exit':
                break
            elif command[0] in avaliable_commands:
                if len(command) == 1:
                    avaliable_commands[command[0]]()
                elif len(command) == 2:
                    try:
                        avaliable_commands[command[0]][command[1]]()
                    except TypeError:
                        try:
                            avaliable_commands[command[0]](command[1])
                        except TypeError:
                            print('Unknown command.')
                elif len(command) == 3:
                    try:
                        avaliable_commands[command[0]][command[1]][command[2]]()
                    except TypeError:
                        try:
                            avaliable_commands[command[0]][command[1]](command[2])
                        except TypeError:
                            try:
                                avaliable_commands[command[0]](command[1] + ' ' + command[2])

                            except TypeError:
                                print('Unknown command.')
            else:
                print('Unknown command.')
    else:
        print('Invalid username or password.')