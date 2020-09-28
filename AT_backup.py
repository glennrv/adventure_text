import random
import pickle


# Functions
def date_of_birth(string):
    dob_int = []
    if len(string) == 10 and string[2] == '-' and string[5] == '-':
        dob = string.split('-')
        for i in dob:
            dob_int.append(int(i))
    return dob_int


def first_last_name(string):
    names = string.split()
    return names


def new_user(dictionary):
    new_user_name = input("Please enter the new users full name: ")
    new_user_dob = input("Please enter the new users date of birth: ")
    new_username = input("Please enter the new users username: ")
    new_user_password = input("Please enter the new users password: ")
    with open("valid_users.pickle", "wb") as vuw:
        dictionary[new_username] = {
        'password': '',
        'name': '',
        'dob': '',
        'inventory': {},
        'fishing level': 1,
        'fishing exp': 0}
        dictionary[new_username]['password'] = new_user_password
        dictionary[new_username]['name'] = new_user_name
        dictionary[new_username]['dob'] = new_user_dob
        pickle.dump(dictionary, vuw) # VIKTIG!!!!!!!
    return print("New user added.")


def fish_options(user):
    lvl = user['fishing level']
    if lvl < 5:
        return fish_methods[:1]
    elif lvl < 10:
        return fish_methods[:2]
    elif lvl >= 10:
        return fish_methods[:3]


def fish(user, method):
    lvl = user['fishing level']
    while True:
        if method == 'small net':
            print('You cast your net into the water.')
            chance = random.randint(1, lvl*10)
            if chance > 5:
                shrimp = random.randint(1, 10)
                user['fishing exp'] += 5 * shrimp
                add_to_inv('shrimp', shrimp)
                return print(f'Congratulations, you caught {shrimp} shrimp!')
            else:
                user['fishing exp'] += 1
                return print('You take out the net, but there is no catch.')
        elif method == 'spear' and lvl >= 5:
            print('You stab your spear into the lake.')
            chance = random.randint(1, lvl * 8)
            if chance > 20:
                tuna = random.randint(1, 5)
                user['fishing exp'] += 20 * tuna
                add_to_inv('tuna', tuna)
                return print(f'Congratulations, you caught {tuna} tuna!')
            else:
                user['fishing exp'] += 2
                return print('Your arm feels sore after repeated stabbings into the water.')
        elif method == 'fishing rod' and lvl >= 10:
            print('You cast the line far into the lake.')
            chance = random.randint(1, lvl * 6)
            if chance > 40:
                user['fishing exp'] += 50
                add_to_inv('salmon', 1)
                return print('Congratulations, you caught a big salmon!')
            else:
                user['fishing exp'] += 5
                return print('Nothing bites.')
        else:
            return print('The option you chose is not avaliable to you.')


def add_to_inv(item, amount):
    with open("valid_users.pickle", "wb") as vuw:
        if item in user['inventory']:
            user['inventory'][item] += amount
            pickle.dump(valid_users, vuw) # VIKTIG!!!!!!!
        else:
            user['inventory'][item] = amount
            pickle.dump(valid_users, vuw) # VIKTIG!!!!!!!


# Program setup
fish_methods = ['small net', 'spear', 'fishing rod']
valid_users_in = open("valid_users.pickle", "rb")
valid_users = pickle.load(valid_users_in)

# Game loop
while True:
        print("""
        Welcome to Adventure Text
    The #1 way to avoid doing anything productive!""")
        username = input("""
        Please enter your username and password to log in.\nUsername: """)
        password = input("""Password: """)

        if password == 'Admin_exit':
            print("ADMIN CODE: EXIT ENABLED.")
            valid_users_in.close()
            break

        if username in valid_users and password == valid_users[username]['password']:
            user = valid_users[username]
            print(f"""Welcome, {user['name']}!""")
            while True:
                command = input("Type Command: ").lower()

                commands = {
                    'help': """
                    List of avaliable commands:
                        Help - Prints a list of all avaliable commands.
                        New user - Creates a new user.
                        Go fish - Initiates fishing mini-game.
                        Logout - Log out to main screen.""",
                    'test_name': f"""
                    {user['name']}""",   # TEST KOMMANDO - SKAL SLETTES!
                    'test_dob': f"""
                    {user['dob']}""",   # TEST KOMMANDO - SKAL SLETTES!
                    'test_inv': f"""
                    {user['inventory']}""",   # TEST KOMMANDO - SKAL ENDRES!
                    'fish_lvl': f"""Your fishing level is: {user['fishing level']}""",
                    'fish_exp': f"""Your fishing experience is: {user['fishing exp']}/{user['fishing level'] * 50}"""
                }

                if command == 'logout':
                    print("""
                Thanks for now, hope to see you again later!""")
                    break

                elif command in commands:
                    print(commands[command])

                elif command == "new user":
                    new_user(valid_users)

                elif command == 'add_to_inv':   # TEST KOMMANDO - SKAL SLETTES!
                    item = input('Item: ')
                    amount = int(input('Amount: '))
                    add_to_inv(item, amount)
                    print('Item successfully added.')

                elif command == 'go fish':
                    print("""\nYou go to the nearest lake to fish.""")
                    while True:
                        method = input("""
        What would you like to do at the lake?
        """).lower()
                        if method == 'leave':
                            break
                        elif method == 'help':
                            print("""
            Help - shows avaliable commands.
            Options - shows avaliable fishing options.
            *option* - initiates fishing with said option.""")
                        elif method == 'options':
                            print(fish_options(user))
                        elif method in fish_methods:
                            fish(user, method)
                            if user['fishing exp'] >= (user['fishing level'] * 50):
                                user['fishing level'] += 1
                                user['fishing exp'] -= (user['fishing level'] - 1) * 50
                                print(f"Congratulations, your fishing level increased to {user['fishing level']}!")
                        else:
                            print("Unknown command.")
                else:
                    print("""    Unknown command.""")
        else:
            print("Invalid key.")
