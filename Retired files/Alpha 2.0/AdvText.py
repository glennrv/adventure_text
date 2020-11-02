import random
import pickle
import math
import pprint
from time import sleep
from texttable import Texttable

# Patch notes
# Added trade functions
# - Fixed bugs (empty equip command; space command break)

# To-do
# Finish start_fishing function
# Format list-prints to strings (check inv, lvl up, etc)
# Finish trade functions
#   Fix vendor stock


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
                try:
                    avaliable_commands[command[0]]()
                except(TypeError, KeyError):
                    print('Unknown command')
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
            add_to_inv(catch, 1)
            print(f'Congratulations, you caught a {catch}!')

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
    with open("vendors.pickle", "rb") as vendors_in:
        global vendors
        vendors = pickle.load(vendors_in)
        print('You go to the market')
        global area
        area = 'The market'
        avaliable_commands = {**command_prompts['global'], **command_prompts[area]}
        print(f'At the market you see {len(vendors)} vendors open for trading.')
        while True:
            command_raw = input(f'[{area}]Command: ').lower()
            command = command_raw.split()
            if command_raw == 'leave':
                print('You head back to the Town Square.')
                break
            elif command[0] in avaliable_commands:
                if len(command) == 1:
                    try:
                        avaliable_commands[command[0]]()
                    except(TypeError, KeyError):
                        print('Unknown command')
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
def trade(vendor_str):
    if vendor_str in vendors:
        inventory = [['Item', 'Stock', 'Buy', 'Sell']]
        for item in vendors[vendor_str]:
            inventory.append([item.capitalize(), vendors[vendor_str][item]['stock'], vendors[vendor_str][item]['buy'], vendors[vendor_str][item]['sell']])
        t = Texttable()
        t.add_rows(inventory)
        print(t.draw())

        while True:
            vendor = vendors[vendor_str]
            command_raw = input(f'''What would you like to do? [buy/sell amount item]: ''').lower()
            if command_raw == 'exit':
                break

            command = command_raw.split(' ')
            sb = command[0]
            # todo: make possible to not enter amount (sell all)
            amount = int(command[1])
            if len(command) == 3:
                item = command[2]
            elif len(command) == 4:
                item = f"{command[2]} {command[3]}"
            else:
                print('Unknown Command...')

            if sb == 'buy':
                price = amount * vendor[item]['buy']
                if item in vendor and vendor[item]['stock'] >= amount:
                    if user['coins'] >= price:
                        add_to_inv(item, amount, price)
                        remove_from_vendor(vendor_str, item, amount)
                        return print(f'''You bought {amount} {item}''')
                    else:
                        print(f'''You need {price} coins to buy that.''')
                else:
                    print(f'''{item} not in stock.''')
            elif sb == 'sell':
                price = amount * vendor[item]['sell']
                if item in (vendor and user['inv']):
                    if user['inv'][item] >= amount:
                        remove_from_inv(item, amount, price)
                        add_to_vendor(vendor_str, item, amount)
                        return print(f'''You sold {amount} {item} for {price} coins.''')
                    else:
                        print(f'''You only have {user['inv'][item]} in your inventory.''')
                else:
                    print('You do not have that item in your inventory.')
            else:
                print('Unknown command.')
    else:
        print('Vendor is not avaliable.')
def options_fishing():
    print('''    The vendors open for trading are:
    Blacksmith  -   
    Carpenter   -   
    Fisherman   -   ''')
def check_inv():
    print(user['inv'])
def check_stats():
    pprint.pprint(user['stats'])
def check_skill(skill):
    print(user['stats'][skill])
def check_carry():
    print(user['carry'])
def check_coins():
    print(f'''Your current balance: {user['coins']} coins.''')
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
    the_market = '''
    Trade       -       Trades with (vendor)
    Leave       -       Leaves the market, heads back to Town square'''
    areas = {'Town square': town_square, 'The docks': the_docks, "The market": the_market}
    if area in areas:
        print(f'''
    Help menu for {area}''')
        print(global_commands, end='')
        print(areas[area])
    else:
        print(f'''
    Help menu for {area}''')
        print(global_commands)
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
        'coins': 0,
        'inv': {},
        'stats': {
            'fishing': {'level': 1, 'exp': 0},
            'hunting': {'level': 1, 'exp': 0},
            'mining': {'level': 1, 'exp': 0}}}
        dictionary[new_username]['password'] = new_user_password
        pickle.dump(dictionary, vuw)  # VIKTIG!!!!!!!
    return print("New user added.")
def add_to_inv(item, amount, price=0):
    """Adds item and amount to user's inventory"""
    with open("valid_users.pickle", "wb") as vuw:
        if item in user['inv']:
            user['inv'][item] += amount
            user['coins'] -= price
            pickle.dump(valid_users, vuw)  # VIKTIG!!!!!!!
            return 'item added to inv'
        else:
            user['inv'][item] = amount
            user['coins'] -= price
            pickle.dump(valid_users, vuw)  # VIKTIG!!!!!!!
            return 'item added to inv'
def remove_from_inv(item, amount, price=0):
    """Adds item and amount to user's inventory"""
    with open("valid_users.pickle", "wb") as vuw:
        if item in user['inv']:
            user['inv'][item] -= amount
            user['coins'] += price
            if user['inv'][item] == 0:
                user['inv'].pop(item)
            pickle.dump(valid_users, vuw)  # VIKTIG!!!!!!!
            return 'item removed from inv'
        else:
            pass
def add_to_vendor(vendor, item, amount):
    """Adds item and amount to user's inventory"""
    with open("vendors.pickle", "wb") as vw:
        if item in vendors[vendor]:
            vendors[vendor][item]['stock'] += amount
            pickle.dump(vendors, vw)  # VIKTIG!!!!!!!
        else:
            print('Vendor does not want this item')
def remove_from_vendor(vendor, item, amount):
    """Adds item and amount to user's inventory"""
    with open("vendors.pickle", "wb") as vw:
        if item in vendors[vendor]:
            vendors[vendor][item]['stock'] -= amount
            pickle.dump(vendors, vw)  # VIKTIG!!!!!!!
        else:
            pass


command_prompts = {
    'global': {
        'help': help_local,             # 'help' - prints a help menu for the local area
        'check': {
            'stats': check_stats,       # 'check stats' - prints the lvl of every skill
            'inv': check_inv,           # 'check inv' - prints the content of your inventory
            'skill': check_skill,       # 'check skill (fishing, hunting, mining)' - prints your level and experience in a specific skill
            'carry': check_carry,
            'coins': check_coins
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

    },
    'The market': {
        'trade': trade,
        'options': options_fishing
    }
}
fishing_levels = {1: {'tools': ['small net'], 'catch': ['shrimp']},
                  5: {'tools': ['harpoon'], 'catch': ['tuna']},
                  10: {'tools': ['fishing rod'], 'catch': ['herring']},
                  15: {'tools': [], 'catch': ['anchovies']},
                  20: {'tools': [], 'catch': ['trout']},
                  25: {'tools': [], 'catch': []},
                  30: {'tools': [], 'catch': ['swordfish']}}
vendors = {}

# Loads in the file containing all the valid users and their stats
valid_users_in = open("valid_users.pickle", "rb")
valid_users = pickle.load(valid_users_in)
vendors_in = open("vendors.pickle", "rb")
vendors = pickle.load(vendors_in)


# Main menu screen - used for logging in to the game
while True:
    area = 'Main menu'
    print ('''
Welcome to Adventure text!''')
    already_user = input('''
To create a new user, type 'new' and press enter.
If you already have a user, just press enter.
Command: ''').lower()
    if already_user == 'new':
        new_user(valid_users)
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
                try:
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
                except IndexError:
                    print('Unknown command.')
            else:
                print('Unknown command.')
    else:
        print('Invalid username or password.')