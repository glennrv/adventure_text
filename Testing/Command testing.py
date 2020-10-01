# This is just used for testing various solutions
# that may or may not be implemented into the main
# game.

import pprint

def fish():
    print("You go fishing")
def hunt():
    print("You go hunting")
def mine():
    print("You go mining")
def check_inv():
    print(user['inv'])
def check_stats():
    print(user['stats'])
def check_skill(skill):
    print(user['stats'][skill])
def help_local():
    print(f"Helpmenu for {area}")

users = {
    'User1': {
        'password': '12345',
        'inv': {
            'fish': 13,
            'ore': 25,
            'meat': 17
        },
        'stats': {
            'fishing': {'level': 1, 'exp': 0},
            'hunting': {'level': 1, 'exp': 0},
            'mining': {'level': 1, 'exp': 0}}},
    'User2': {
        'password': '12345',
        'inv': {},
        'stats': {
            'fishing': {'level': 1, 'exp': 0},
            'hunting': {'level': 1, 'exp': 0},
            'mining': {'level': 1, 'exp': 0}}}}

command_prompts = {
    'help': help_local,             # 'help' - prints a help menu for the local area
    'go': {
        'fish': fish,               # 'go fish' - initiates fishing
        'hunt': hunt,               # 'go hunt' - initiates hunting
        'mine': mine                # 'go mine' - initiates mining
    },
    'check': {
        'stats': check_stats,       # 'check stats' - prints the lvl of every skill
        'inv': check_inv,           # 'check inv' - prints the content of your inventory
        'skill': check_skill        # 'check skill (fishing, hunting, mining)' - prints your level and experience in a specific skill
    }

}

while True:
    area = 'Main menu'
    username = input("Username: ")
    password = input("Password: ")
    if username in users and password == users[username]['password']:
        user = users[username]
        print(f"Welcome {username}!")
        while True:
            area = 'Town square'
            command_raw = input("Command: ").lower()
            command = command_raw.split()
            if command[0] == 'exit':
                break
            elif command[0] in command_prompts:
                if len(command) == 1:
                    command_prompts[command[0]]()
                elif len(command) == 2:
                    command_prompts[command[0]][command[1]]()
                elif len(command) == 3:
                    command_prompts[command[0]][command[1]](command[2])
            else:
                print("Unknown command.")
    elif password.lower == "quit":
        break
    else:
        print("Invalid username or password.")