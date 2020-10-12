import random
import pickle
import math
import pprint
from time import sleep

# To-do
# Fix help function
# Finish start_fishing function
# Format list-prints to strings (check inv, lvl up, etc)


def fish():
    """Function for the fishing skill"""
    # Area - The Docks

    print('You head to the docks.')
    global area
    area = 'The docks'
    avaliable_commands = {**command_prompts['global'], **command_prompts[area]}

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
    # Tools for the fishing mini-game
    fishing = user['stats']['fishing']
    tool = user['carry']
    tool_modifiers = {'small net': 1, 'harpoon': 5, 'fishing rod': 10}
    catch_modifiers = {'shrimp': 1, 'tuna': 2, 'herring': 3, 'anchovies': 4, 'trout': 5, 'swordfish': 7}
    catch_list = {'small net': ['shrimp', 'anchovies'], 'harpoon': ['tuna', 'swordfish'], 'fishing rod': ['herring', 'trout']}
    avaliable_tools = [] # Avaliable tools based on users fishing lvl
    avaliable_catch = [] # Avaliable catches based on users fishing lvl
    valid_catch = [] # Avaliable catches based on fishing lvl and equipped tool

    # Adds the valid tools to avaliable_tool list
    for level in fishing_levels:
        if fishing['level'] >= level:
            avaliable_tools += fishing_levels[level]['tools']
    # Checks if equipped tool is valid, then adds catches to avaliable_catch list
    if tool in avaliable_tools:
        for level in fishing_levels:
            if fishing['level'] >= level:
                avaliable_catch += fishing_levels[level]['catch']
    # If tool is not valid, returns message
    else:
        return print('You have to equip a valid tool before you can start fishing.')

    # Makes the final list of valid catches based on tool and lvl
    for fish in avaliable_catch:
        if fish in catch_list[tool]:
            valid_catch.append(fish)

    # Initiates actual fishing if all previous conditions are fulfilled
    print(f'You start fishing with your {tool}.')
    while True:
        # Chance of catch
        atempt = random.randint(1, 100)
        chance = (math.atan(fishing['level']/tool_modifiers[tool]) - 0.58) * 100

        # Time before catching/not catching
        time = random.uniform(0.5, 10 - 0.1 * fishing['level'])
        delay = int(round(time, 0))

        # Loading screen between starting fishing and catching/not catching
        for i in range(1, delay):
            print('. . .')
            sleep(1)

        # To-do
        # Add to inv
        # Add ability to catch more than 1 catch
        # Maybe add better waiting graphics

        # If there's a catch
        if atempt <= chance:

            # Randomized catch from valid_catch list, add xp, catch message
            catch = valid_catch[random.randint(0, len(valid_catch)-1)]
            fishing['exp'] += 10 * catch_modifiers[catch]
            print(f'Congratulations, you caught a {catch}!')

            # Asks if user would like to continue fishing
            com = input('Would you like to keep fishing? (y/n): ').lower()
            if com == 'y':
                continue
            elif com == 'n':
                break
            else:
                print('Unknown command.')

        # If theres no catch
        else:
            print('You did not catch anything')
            com = input('Would you like to keep fishing? (y/n): ').lower()
            if com == 'y':
                continue
            elif com == 'n':
                break
            else:
                print('Unknown command.')

    # Checks if user has enough exp to lvl-up
    if fishing['exp'] >= fishing['level'] * 50:
        fishing['exp'] -= fishing['level'] * 50
        fishing['level'] += 1
        print(f'''Congratulations, you advanced to fishing level {fishing['level']}!''')

        # Checks if the new lvl unlocks anything, if yes, prints the new tools and/or catches
        if fishing['level'] in fishing_levels:
            print('You unlocked: ')
            if len(fishing_levels[fishing['level']]['tools']) > 0:
                print(f'''Tools: {fishing_levels[fishing['level']]['tools']}''')
            else:
                pass
            if len(fishing_levels[fishing['level']]['catch']) > 0:
                print(f'''Catch: {fishing_levels[fishing['level']]['catch']}''')
            else:
                pass
def options_fishing():
    print("""   Level   -    Tools    -   Catch
       1   -  Small net  -   Shrimp
       5   -   Harpoon   -   Tuna
      10   - Fishing rod -   Herring
      15   -             -   Anchovies
      20   -             -   Trout
      25   -             -   
      30   -             -   Swordfish""")
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
    global_commands = '''
    Help        -       Shows the help menu for the local area.
    Check       -       Checks (stats, inv, skill [skill], carry).
    Equip       -       Equips item to carry.
    Unequip     -       Unequips carry.'''
    town_square = '''
    Go          -       Takes you to new area (fish, hunt, mine, trade).
    Logout      -       Logs out user and returns to main menu.'''
    the_docks = '''
    Fish        -       Start fishing with currently equipped carry.
    Options     -       Shows the option menu for fishing skill.
    Leave       -       Leaves the docks, heads back to Town square.'''
    areas = {'Town square': town_square, 'The docks': the_docks}
    if area in areas:
        print(f'''
    Help menu for {area}''')
        print(global_commands, end='')
        print(areas[area])
def equip(tool):
    if tool in user['inv']:
        user['carry'] = tool
        return user
    else:
        return print('You do not have this tool in your inventory.')
def unequip():
    user['carry'] = ''
    return user
def new_user(dictionary):
    """Adds a new user with all the default settings."""
    new_username = input("Please enter the new users username: ")
    new_user_password = input("Please enter the new users password: ")
    with open("valid_users.pickle", "wb") as vuw:
        dictionary[new_username] = {
        'password': '',
        'carry': '',
        'inv': {},
        'stats': {
            'fishing': {'level': 1, 'exp': 0},
            'hunting': {'level': 1, 'exp': 0},
            'mining': {'level': 1, 'exp': 0}}}
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
fishing_levels = {1: {'tools': ['small net'], 'catch': ['shrimp']},
                  5: {'tools': ['harpoon'], 'catch': ['tuna']},
                  10: {'tools': ['fishing rod'], 'catch': ['herring']},
                  15: {'tools': [], 'catch': ['anchovies']},
                  20: {'tools': [], 'catch': ['trout']},
                  25: {'tools': [], 'catch': []},
                  30: {'tools': [], 'catch': ['swordfish']}}

# Loads in the file containing all the valid users and their stats
valid_users_in = open("valid_users.pickle", "rb")
valid_users = pickle.load(valid_users_in)


# Main menu screen - used for logging in to the game
while True:
    area = 'Main menu'
    username = input('Username: ')
    if username.lower() == 'quit':
        print('You have left the game.')
        break

    password = input('Password: ')
    if username in valid_users and password == valid_users[username]['password']:
        user = valid_users[username]
        print(f'Welcome {username}!')

        # Actual Game Loop
        while True:
            area = 'Town square'
            avaliable_commands = {**command_prompts['global'], **command_prompts[area]}
            command_raw = input('Command: ').lower()
            command = command_raw.split()
            if len(command_raw) > 0:
                if command[0] == 'logout':
                    break
                elif command[0] in avaliable_commands:
                    if len(command) == 1:
                        try:
                            avaliable_commands[command[0]]()
                        except (TypeError, KeyError):
                            print('Unknown command.')
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
                print('Invalid command.')
    else:
        print('Invalid username or password.')