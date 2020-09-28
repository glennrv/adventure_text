import random
import pickle
import math


# Functions
def new_user(dictionary):
    """Adds a new user with all the default settings."""
    new_username = input("Please enter the new users username: ")
    new_user_password = input("Please enter the new users password: ")
    with open("valid_users.pickle", "wb") as vuw:
        dictionary[new_username] = {
        'password': '',
        'inventory': {},
        'fishing level': 1,
        'fishing exp': 0}
        dictionary[new_username]['password'] = new_user_password
        pickle.dump(dictionary, vuw)  # VIKTIG!!!!!!!
    return print("New user added.")


def add_to_inv(item, amount):
    """Adds item and amount to user's inventory"""
    with open("valid_users.pickle", "wb") as vuw:
        if item in user['inventory']:
            user['inventory'][item] += amount
            pickle.dump(valid_users, vuw)  # VIKTIG!!!!!!!
        else:
            user['inventory'][item] = amount
            pickle.dump(valid_users, vuw)  # VIKTIG!!!!!!!


def fish_options(user):
    """Views the avaliable fishing options based on user's fishing level"""
    lvl = user['fishing level']
    if lvl < 5:
        return fish_methods[:1]
    elif lvl < 10:
        return fish_methods[:2]
    elif lvl >= 10:
        return fish_methods[:3]


def fish(user, method):
    """Function for the fishing skill, executed based on chosen method"""
    lvl = user['fishing level']
    while True:
        if method == 'small net':
            print('You cast your net into the water.')
            atempt = random.randint(1, 100)
            chance = (math.atan(lvl) - 0.58) * 100
            if atempt <= chance:
                shrimp = random.randint(1, 10)
                user['fishing exp'] += 5 * shrimp
                add_to_inv('shrimp', shrimp)
                return print(f'Congratulations, you caught {shrimp} shrimp!')
            else:
                user['fishing exp'] += 1
                return print('You take out the net, but there is no catch.')
        elif method == 'spear' and lvl >= 5:
            print('You stab your spear into the lake.')
            atempt = random.randint(1, 100)
            chance = (math.atan(lvl/5) - 0.58) * 100
            if atempt <= chance:
                tuna = random.randint(1, 5)
                user['fishing exp'] += 20 * tuna
                add_to_inv('tuna', tuna)
                return print(f'Congratulations, you caught {tuna} tuna!')
            else:
                user['fishing exp'] += 2
                return print('Your arm feels sore after repeated stabbings into the water.')
        elif method == 'fishing rod' and lvl >= 10:
            print('You cast the line far into the lake.')
            atempt = random.randint(1, 100)
            chance = (math.atan(lvl/10) - 0.58) * 100
            if atempt <= chance:
                user['fishing exp'] += 50
                add_to_inv('salmon', 1)
                return print('Congratulations, you caught a big salmon!')
            else:
                user['fishing exp'] += 5
                return print('Nothing bites.')
        else:
            return print('The option you chose is not avaliable to you.')


### Program setup

# The currently avaliable fishing methods
fish_methods = ['small net', 'spear', 'fishing rod']

# Loads in the file containing all the valid users and their stats
valid_users_in = open("valid_users.pickle", "rb")
valid_users = pickle.load(valid_users_in)

### Game loop

# Main Menu loop - Login screen
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

    # Checks if username and password match, and logs user in.
    if username in valid_users and password == valid_users[username]['password']:
        user = valid_users[username]
        print(f"""Welcome, {username}!""")

        # Logged in game loop
        while True:

            # Command input which is the base of every action in-game
            command = input("Type Command: ").lower()

            # Dictionary of basic print commands
            commands = {
                'help': """
                List of avaliable commands:
                    Help - Prints a list of all avaliable commands.
                    New user - Creates a new user.
                    Go fish - Initiates fishing mini-game.
                    Logout - Log out to main screen.""",
                'test_inv': f"""
                {user['inventory']}""",   # TEST COMMAND - WILL BE CHANGED!
                'fish_lvl': f"""Your fishing level is: {user['fishing level']}""",
                'fish_exp': f"""Your fishing experience is: {user['fishing exp']}/{user['fishing level'] * 50}"""
            }

            # Logout command
            if command == 'logout':
                print("""
            Thanks for now, hope to see you again later!""")
                break

            # Checks if the command is a basic print command
            elif command in commands:
                print(commands[command])

            # Adds a new user
            elif command == "new user":
                new_user(valid_users)

            # Admin command that adds item to inventory (used for testing)
            elif command == 'add_to_inv':   # TEST COMMAND - WILL BE DELETED!
                item = input('Item: ')
                amount = int(input('Amount: '))
                add_to_inv(item, amount)
                print('Item successfully added.')

            # Command to initiate fishing skill/mini-game
            elif command == 'go fish':
                print("""\nYou go to the nearest lake to fish.""")

                # Fishing game-loop
                while True:
                    method = input("""
    What would you like to do at the lake?
    """).lower()

                    # Exits the fishing game-loop, back to logged-in game-loop
                    if method == 'leave':
                        break

                    # Prints avaliable commands within the fishing game-loop
                    elif method == 'help':
                        print("""
        Help - shows avaliable commands.
        Options - shows avaliable fishing options.
        *option* - initiates fishing with said option.""")

                    # Prints avaliable fishing methods for user's level
                    elif method == 'options':
                        print(fish_options(user))

                    # Initiates fishing
                    elif method in fish_methods:
                        fish(user, method)

                        # Checks if user's fishing exp is high enough to level up
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
