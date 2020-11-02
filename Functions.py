"""Most functions used in Adventure text belongs in this file."""

from Classes import *
import pickle
from prettytable import PrettyTable

# Game functions


def help_area(area):
    areas = {'Main Menu': '''
    Help        -   Display help menu
    Login       -   Opens login prompt
    New user    -   Create new user
    Quit        -   Quit game
    ''',
             'the Town Square': '''
    Help        -   Display help menu
    Go          -   Go to area
    Logout      -   Log out from user
    Quit        -   Quit game
    ''',
             'the Market': '''
    Help        -   Display help menu
    Go          -   Go to area
    Leave       -   Return to town square
    Logout      -   Log out from user
    Quit        -   Quit game
    '''}

    if area in areas:
        print(f'''
    Help menu for {area}''')
        print(areas[area])
    else:
        print('Help menu is not yet implemented for this area.')


# User functions

def save_users(users):
    with open('users.pkl', "wb") as save:
        return pickle.dump(users, save)


def load_user(username, password, users):
    for obj in users:
        if obj.username == username and obj.password == password:
            print(f'Welcome {obj.username}!')
            return obj


def add_user(username, password, users):
    for obj in users:
        if obj.username == username:
            print('Username not available.')
            return False
    new = Player(username, password)
    users.append(new)
    save_users(users)
    return True


def remove_user(username, password, users):
    for obj in users:
        if obj.username == username and obj.password == password:
            undo = input('Are you sure you want to remove user?')
            if undo.lower() in ['yes', 'y']:
                users.remove(obj)
                save_users(users)


# Vendor functions

def save_vendors(vendors):
    with open('vendors.pkl', "wb") as save:
        return pickle.dump(vendors, save)


def load_vendor(vendor, vendors):
    for obj in vendors:
        if obj.name == vendor:
            return obj
    return False


def add_vendor(vendor, v_type, price, vendors):
    for obj in vendors:
        if obj.name == vendor:
            return False
    new = Vendor(vendor, v_type, price)
    vendors.append(new)
    save_vendors(vendors)
    return new


def remove_vendor(vendor, vendors):
    vendor = vendor.lower()
    for obj in vendors:
        if obj.name == vendor:
            vendors.remove(obj)
            save_vendors(vendors)
            return vendors
    return False


def display_vendors(vendors):
    display = PrettyTable(['Name', 'Type'])
    for vendor in vendors:
        display.add_row([vendor.name.title(), vendor.v_type.title()])
    return display


def update_vendor(vendor, vendors):
    """Actively edit this to fit the current situation of update."""
    old_name = vendor.name
    old_type = vendor.v_type
    old_stock = vendor.stock
    old_price_factor = vendor.price_factor
    old_s_t = vendor.successful_trades
    old_s_p = vendor.successful_purchases
    old_s_s = vendor.successful_sales
    remove_vendor(vendor.name, vendors)
    add_vendor(old_name, old_type, old_price_factor, vendors)
    new_vendor = load_vendor(old_name, vendors)
    new_vendor.stock = old_stock
    new_vendor.successful_trades = old_s_t
    new_vendor.successful_purchases = old_s_p
    new_vendor.successful_sales = old_s_s
    save_vendors(vendors)
    return vendors



# Admin functions

def admin_load_user(username, users):
    for obj in users:
        if obj.username == username:
            return obj


def admin_remove_user(username, users):
    for obj in users:
        if obj.username == username:
            undo = input('Are you sure you want to remove user?')
            if undo.lower() in ['yes', 'y']:
                users.remove(obj)
                print(f'{username} removed.')
                return users
            return False
    return False


def set_admin(player, users):
    a_player = admin_load_user(player, users)
    a_player.admin = True
    return a_player.admin


def remove_admin(player, users):
    a_player = admin_load_user(player, users)
    a_player.admin = 0
    return a_player.admin


def admin_add_coins(player, amount, users):
    a_player = admin_load_user(player, users)
    a_player.coins += amount
    return a_player.coins


def admin_help():
    help_str = f'''
    [Admin commands]
    - All admin commands start with '/'

    Admin help      -   Displays admin help menu
    Make admin      -   Give user administrative privileges
    Remove admin    -   Removes administrative privileges from user
    Delete user     -   Permanently deletes user
    List users      -   Displays list of all users registered
    Info user       -   Displays all info about user
    '''
    return help_str
