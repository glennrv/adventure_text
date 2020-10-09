# This is just used for testing various solutions
# that may or may not be implemented into the main
# game.

import random
import pickle
import math
import pprint
from time import sleep

# To-do
# Fix help function
# Finish fishing function
# Format list-prints to strings (check inv, lvl up, etc)
#


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
                except (TypeError, KeyError):
                    try:
                        avaliable_commands[command[0]](command[1])
                    except (TypeError, KeyError):
                        print('Unknown command.')
            elif len(command) == 3:
                try:
                    avaliable_commands[command[0]][command[1]][command[2]]()
                except (TypeError, KeyError):
                    try:
                        avaliable_commands[command[0]][command[1]](command[2])
                    except (TypeError, KeyError):
                        try:
                            avaliable_commands[command[0]](command[1] + ' ' + command[2])
                        except (TypeError, KeyError):
                            print('Unknown command.')
        else:
            print('Unknown command.')

def start_fishing():
    fishing = user['stats']['fishing']
    tool = user['carry']
    avaliable_tools = []
    avaliable_catch = []
    tool_modifiers = {'small net': 1, 'harpoon': 5, 'fishing rod': 10}

    for level in fishing_levels:
        if fishing['level'] >= level:
            avaliable_tools += fishing_levels[level]['tools']
            avaliable_catch += fishing_levels[level]['catch']

    if tool in avaliable_tools:
        print(f'You start fishing with your {tool}.')
        while True:
            atempt = random.randint(1, 100)
            chance = (math.atan(fishing['level']/tool_modifiers[tool]) - 0.58) * 100
            fishing['exp'] += 100
            print('it funks')
            break
    else:
        return print('You have to equip a valid tool before you can start fishing.')

    if fishing['exp'] >= fishing['level'] * 100:
        fishing['exp'] -= fishing['level'] * 100
        fishing['level'] += 1
        print(f"Congratulations, you advanced to fishing level {fishing['level']}!")
        if fishing['level'] in fishing_levels:
            print("You unlocked: ")
            if len(fishing_levels[fishing['level']]['tools']) > 0:
                print(f"Tools: {fishing_levels[fishing['level']]['tools']}")
            else:
                pass
            if len(fishing_levels[fishing['level']]['catch']) > 0:
                print(f"Catch: {fishing_levels[fishing['level']]['catch']}")
            else:
                pass

def options_fishing():
    print("""   Level   -    Tools    -   Catch
       1   -  Small net  -   Shrimp, Anchovies
       5   -   Harpoon   -   Tuna, Swordfish
      10   - Fishing rod -   Herring, Trout""")


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
            'fishing rod': 1,
            'small net': 1
        },
        'stats': {
            'fishing': {'level': 1, 'exp': 0},
            'hunting': {'level': 1, 'exp': 0},
            'mining': {'level': 1, 'exp': 0}}}
}
fishing_levels = {1: {'tools': ['small net'], 'catch': ['shrimp']},
                  5: {'tools': ['harpoon'], 'catch': ['tuna']},
                  10: {'tools': ['fishing rod'], 'catch': ['herring']},
                  15: {'tools': [], 'catch': ['anchovies']},
                  20: {'tools': [], 'catch': ['trout']},
                  25: {'tools': [], 'catch': []},
                  30: {'tools': [], 'catch': ['swordfish']}}


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
                    except (TypeError, KeyError):
                        try:
                            avaliable_commands[command[0]](command[1])
                        except (TypeError, KeyError):
                            print('Unknown command.')
                elif len(command) == 3:
                    try:
                        avaliable_commands[command[0]][command[1]][command[2]]()
                    except (TypeError, KeyError):
                        try:
                            avaliable_commands[command[0]][command[1]](command[2])
                        except (TypeError, KeyError):
                            try:
                                avaliable_commands[command[0]](command[1] + ' ' + command[2])
                            except (TypeError, KeyError):
                                print('Unknown command.')
            else:
                print('Unknown command.')
    else:
        print('Invalid username or password.')