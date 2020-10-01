# This is just used for testing various solutions
# that may or may not be implemented into the main
# game.


def fish():
    print("You go fishing")
def hunt():
    print("You go hunting")
def mine():
    print("You go mining")
def check_levels():
    return levels
def check_inv():
    return inv
def check_skill():
    return skill
def help_local(area):
    print(f"Helpmenu for {area}")



users = {
    'User1': {
        'password': '12345',
        'inv': {
            'fish': 13,
            'ore': 25,
            'meat': 17
        },
        'levels': {'fishing': {'level': 1, 'exp': 0},
                   'hunting': {'level': 1, 'exp': 0},
                   'mining': {'level': 1, 'exp': 0}}},
    'User2': {
        'password': '12345',
        'inv': {},
        'levels': {'fishing': {'level': 1, 'exp': 0},
                   'hunting': {'level': 1, 'exp': 0},
                   'mining': {'level': 1, 'exp': 0}}}}

command_prompts = {
    'help': help_local,
    'go': {
        'fish': fish,
        'hunt': hunt,
        'mine': mine
    },
    'check': {
        'levels': check_levels,
        'inv': check_inv,
        'skill': check_skill
    }

}
while True:
    user = input("Username: ")
    password = input("Password: ")
    if user in users and password == users[user]['password']:
        print(f"Welcome {user}!")
        while True:
            command_raw = input("Command: ").lower()
            command = command_raw.split(' ')
            if command[0] == 'exit':
                break
            elif command[0] in command_prompts:
                command_prompts[command[0]](command[1], command[2])
            else:
                print("Unknown command.")
    elif password.lower == "quit":
        break
    else:
        print("Invalid username or password.")
