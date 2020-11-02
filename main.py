from Functions import *
from Classes import *


# ---------- Setup ----------

# Load users
with open('users.pkl', 'rb') as load:
    users = pickle.load(load)

with open('vendors.pkl', 'rb') as load:
    vendors = pickle.load(load)

# Set active areas
Play = True
Game = False
Fish = False
Mine = False
Shop = False
Hunt = False

# Standard messages
UCError = 'Unknown command.'                        # Unknown Command
PError = 'You do not have permission to do this.'   # Permission
DNEError = 'This does not exist.'                   # Does Not Exist

quit_message = 'Thanks for playing Adventure text!'
logout_message = 'has logged out.'

# ---------- Game ----------

# Welcome Screen
print('''
### Welcome to Adventure Text! ###
To create a new user, type 'new user'.
If you already have a user, type 'login' to log in.
If you are stuck, use the 'help' command.''')

# Main menu - Area: Main Menu
while Play:
    area = 'Main Menu'
    print(users)
    command = input(f'Command: ').lower().strip()
    if command == 'quit':
        print(quit_message)
        Play = False
    elif command == 'help':
        help_area('Main Menu')
    elif command == 'new user':
        username = input('Please enter a username: ')
        password = input('Please enter a password: ')
        add_user(username, password, users)
    elif command == 'login':
        username = input('Username: ').strip()
        password = input('Password: ').strip()
        no_match = 0
        for obj in users:
            if obj.username == username and obj.password == password:
                user = load_user(username, password, users)
                Game = True
            elif obj.username == username and obj.password != password:
                print('Password is incorrect.')
            else:
                no_match += 1
        if no_match == len(users):
            print('Username not recognized.')
    else:
        print(UCError)

    # Main Game Loop - Area: The Town Square
    while Game:
        area = 'Town Square'
        command = input(f'\n[{area}]Command: ').lower().strip()
        if command == 'logout':
            print(logout_message)
            Game = False
        elif command == 'quit':
            print(quit_message)
            Game = False
            Play = False
        elif command == 'help':
            help_area('the Town Square')
        elif command == 'go trade':
            print('You go to the Market.')
            Shop = True
            # Shops and vendors - Area: the Market
            while Shop:
                area = 'Market'
                command = input(f'\n[{area}]Command: ').lower().strip()
                if command == 'help':
                    help_area('the Market')
                elif command == 'leave':
                    print('You leave the Market and head back to the Town Square.')
                    Shop = False
                elif command == 'logout':
                    print(logout_message)
                    Shop = False
                    Game = False
                elif command == 'quit':
                    print(quit_message)
                    Shop = False
                    Game = False
                    Play = False
                elif command == 'trade':
                    print('    Available Vendors')
                    print(display_vendors(vendors))
                    who = input('\nWho would you like to trade with? ').lower().strip()
                    vendor = load_vendor(who, vendors)
                    if vendor:
                        print('    Vendor Stock')
                        print(vendor.display_stock())
                        trade = input('\nWould you like to buy or sell? ').lower().strip()
                        if trade == 'buy':
                            item = input('\nwhat do you want to buy? ').lower().strip()
                            amount = int(input('Enter amount: ').strip())
                            vendor_has_item = vendor.check_stock(item, amount)
                            if vendor_has_item:
                                price = vendor.stock[item]['sell_price'] * amount
                                user_has_coins = (user.coins >= price)
                                if user_has_coins:
                                    vendor.remove_from_stock(item, amount)
                                    user.remove_coins(price)
                                    user.add_to_inv(item, amount)
                                    vendor.successful_trades += 1
                                    vendor.successful_sales += 1
                                    save_users(users)
                                    save_vendors(vendors)
                                    print(f'You bought {amount} of {item} for {price} coins.')
                                else:
                                    print('You do not have enough coins.')
                            else:
                                print(f'{vendor.name.title()} does not have enough this item.')
                        elif trade == 'sell':
                            print('    Your Inventory:')
                            print(user.display_inv())
                            item = input('\nwhat do you want to sell? ').lower().strip()
                            amount = int(input('Enter amount: ').strip())
                            user_has_item = user.check_inv(item, amount)
                            if user_has_item:
                                vendor_wants_item = vendor.check_stock(item)
                                if vendor_wants_item:
                                    price = vendor.stock[item]['buy_price'] * amount
                                    user.remove_from_inv(item, amount)
                                    user.add_coins(price)
                                    vendor.add_to_stock(item, amount)
                                    vendor.successful_trades += 1
                                    vendor.successful_purcases += 1
                                    save_users(users)
                                    save_vendors(vendors)
                                    print(f'You sold {amount} {item} for {price} coins.')
                                else:
                                    print(f'{vendor.name.title()} does not want this item.')
                            else:
                                print('You do not have enough of this item.')
                        else:
                            print(UCError)
                elif command == '/admin help':
                    if user.admin:
                        print(admin_help())
                    else:
                        print(PError)
                elif command == '/make admin':
                    if user.admin:
                        who = input('Enter name of player you want to make Admin: ').strip()
                        set_admin(who, users)
                        print(f'{who} has been made Admin.')
                        save_users(users)
                    else:
                        print(PError)
                elif command == '/remove admin':
                    if user.admin:
                        who = input('Enter name of player you want to remove as Admin: ').strip()
                        remove_admin(who, users)
                        print(f'{who} has been removed as Admin.')
                        save_users(users)
                    else:
                        print(PError)
                elif command == '/delete user':
                    if user.admin:
                        who = input('Enter name of user you want to delete: ').strip()
                        admin_remove_user(who, users)
                        save_users(users)
                    else:
                        print(PError)
                elif command == '/list users':
                    if user.admin:
                        print(f'User-list: {users}')
                    else:
                        print(PError)
                elif command == '/user info':
                    if user.admin:
                        print(f'User-list: {users}')
                        who = input('Name of user: ').strip()
                        who_user = admin_load_user(who, users)
                        if who_user:
                            print(who_user.info())
                            print(who_user.display_inv)
                        else:
                            print(DNEError)
                    else:
                        print(PError)
                elif command == '/add coins':
                    who = input('Who gets coins? ').strip()
                    amount = int(input('How much? ').strip())
                    admin_add_coins(who, amount, users)
                    save_users(users)
                elif command == '/vendor':
                    print('New, Delete, Info, Update vendor, Reset stock')
                    print('Edit price, Add item, Remove item, Delete item')
                    what = input('What do you want to do with vendors? ').lower().strip()
                    if what == 'add item':
                        print(f'Available Vendors: \n{vendors}')
                        who = input('Name of Vendor: ').lower().strip()
                        vendor = load_vendor(who, vendors)
                        if vendor:
                            item = input('Item: ').lower().strip()
                            amount = input('Amount: ').strip()
                            if item in vendor.stock:
                                amount = int(amount)
                                vendor.add_to_stock(item, amount)
                                print(f'{amount} {item} added to {vendor.name.title()}\'s stock.')
                                save_vendors(vendors)
                            else:
                                sell_price = int(input('Vendor will sell this for: ').strip())
                                buy_price = int(input('Vendor will buy this for: ').strip())
                                vendor.new_item_in_stock(item, buy_price, sell_price, amount)
                                print(f'\n{amount} {item} added to {vendor.name.title()}\'s stock.')
                                print(f'{vendor.name.title()} will buy this for: {buy_price}c, and sell for: {sell_price}c.')
                                save_vendors(vendors)
                        else:
                            print(DNEError)
                    elif what == 'remove item':
                        print(vendors)
                        who = input('Name of Vendor: ').lower().strip()
                        vendor = load_vendor(who, vendors)
                        if vendor:
                            print('    Vendor Stock')
                            print(vendor.display_stock())
                            item = input('Item: ').lower().strip()
                            amount = int(input('Amount: ').strip())
                            if vendor.check_stock(item):
                                vendor.remove_from_stock(item, amount)
                                print(f'New stock: {item.title()}, {vendor.stock[item]["stock"]}')
                                save_vendors(vendors)
                            else:
                                print(f'{vendor.name.title()} does not have this item.')
                        else:
                            print(DNEError)
                    elif what == 'delete item':
                        print(vendors)
                        who = input('Name of Vendor: ').lower().strip()
                        vendor = load_vendor(who, vendors)
                        if vendor:
                            print('    Vendor Stock')
                            print(vendor.display_stock())
                            item = input('Item: ').lower().strip()
                            if vendor.check_stock(item):
                                confirm = input('Are you sure you want to delete this item? [Y/N]').lower().strip()
                                if confirm in ('y', 'ye', 'yes'):
                                    vendor.delete_item_from_stock(item)
                                    print(vendor.display_stock())
                                    print(f'{item.title()} removed from {vendor.name.title()}\'s stock.')
                                    save_vendors(vendors)
                                else:
                                    print('Delete aborted.')
                            else:
                                print(DNEError)
                        else:
                            print(DNEError)
                    elif what == 'new':
                        name = input('Name of vendor: ').lower().strip()
                        v_type = input('Type of vendor: ').lower().strip()
                        # price = input('Price factor: ')
                        new_vendor = add_vendor(name, v_type, 0, vendors)
                        if new_vendor:
                            new_vendor.automatic_stock()
                            print(new_vendor.display_stock())
                            print(f'{new_vendor.name.title()} has arrived to the Market.')
                            save_vendors(vendors)
                        else:
                            print(f'A vendor by that name already exists.')
                    elif what == 'delete':
                        print(vendors)
                        who = input('Name of vendor: ').strip()
                        vendor = load_vendor(who, vendors)
                        if vendor:
                            confirm = input(
                                f'Are you sure you want to remove {vendor.name.title()}? ').lower().strip()
                            if confirm in ('y', 'ye', 'yes'):
                                remove_vendor(vendor.name, vendors)
                                print('Vendor removed from Market.')
                                save_vendors(vendors)
                            else:
                                print(f'Removal of {vendor.name.title()} aborted.')
                        else:
                            print(DNEError)
                    elif what == 'info':
                        print(vendors)
                        who = input('Name of Vendor: ').strip()
                        vendor = load_vendor(who, vendors)
                        if vendor:
                            print(vendor.info())
                            print(vendor.display_stock())
                        else:
                            print(DNEError)
                    elif what == 'edit price':
                        print(vendors)
                        who = input('Name of Vendor: ').lower().strip()
                        vendor = load_vendor(who, vendors)
                        if vendor:
                            print(vendor.display_stock())
                            item = input('Item: ').lower().strip()
                            new_buy = int(input('Sell: ').strip())
                            new_sell = int(input('Buy: ').strip())
                            vendor.edit_price(item, new_buy, new_sell)
                            save_vendors(vendors)
                            print(vendor.display_stock())
                        else:
                            print(DNEError)
                    elif what == 'reset stock':
                        print(vendors)
                        who = input('Name of Vendor: ').lower().strip()
                        vendor = load_vendor(who, vendors)
                        if vendor:
                            vendor.automatic_stock()
                            print(vendor.display_stock())
                            print(f'{vendor.name.title()}\'s stock has been reset.')
                            save_vendors(vendors)
                        else:
                            print(DNEError)
                    elif what == 'update vendor':
                        print(vendors)
                        who = input('Name of Vendor: ').lower().strip()
                        vendor = load_vendor(who, vendors)
                        if vendor:
                            update_vendor(vendor, vendors)
                            updated_vendor = load_vendor(who, vendors)
                            if vendor:
                                print('Success.')
                                print(updated_vendor.info())
                                save_vendors(vendors)
                            else:
                                print('Something went wrong')
                        else:
                            print(DNEError)
                    else:
                        print('Alrighty then.')
            else:
                print(UCError)
        elif command == '/admin help':
            if user.admin:
                print(admin_help())
            else:
                print(PError)
        elif command == '/make admin':
            if user.admin:
                who = input('Enter name of player you want to make Admin: ').strip()
                set_admin(who, users)
                print(f'{who} has been made Admin.')
                save_users(users)
            else:
                print(PError)
        elif command == '/remove admin':
            if user.admin:
                who = input('Enter name of player you want to remove as Admin: ').strip()
                remove_admin(who, users)
                print(f'{who} has been removed as Admin.')
                save_users(users)
            else:
                print(PError)
        elif command == '/delete user':
            if user.admin:
                who = input('Enter name of user you want to delete: ').strip()
                admin_remove_user(who, users)
                save_users(users)
            else:
                print(PError)
        elif command == '/list users':
            if user.admin:
                print(f'User-list: {users}')
            else:
                print(PError)
        elif command == '/user info':
            if user.admin:
                print(f'User-list: {users}')
                who = input('Name of user: ').strip()
                who_user = admin_load_user(who, users)
                if who_user:
                    print(who_user.info())
                    print(who_user.display_inv)
                else:
                    print(DNEError)
            else:
                print(PError)
        elif command == '/add coins':
            who = input('Who gets coins? ').strip()
            amount = int(input('How much? ').strip())
            admin_add_coins(who, amount, users)
            save_users(users)
        elif command == '/vendor':
            print('''New, Delete, Info, Update vendor, Reset stock
Edit price, Add item, Remove item, Delete item''')
            what = input('What do you want to do with vendors? ').lower().strip()
            if what == 'add item':
                print(vendors)
                who = input('Name of Vendor: ').lower().strip()
                vendor = load_vendor(who, vendors)
                if vendor:
                    item = input('Item: ').lower().strip()
                    amount = input('Amount: ').strip()
                    if item in vendor.stock:
                        amount = int(amount)
                        vendor.add_to_stock(item, amount)
                        print(f'{amount} {item} added to {vendor.name.title()}\'s stock.')
                        save_vendors(vendors)
                    else:
                        sell_price = int(input('Vendor will sell this for: ').strip())
                        buy_price = int(input('Vendor will buy this for: ').strip())
                        vendor.new_item_in_stock(item, buy_price, sell_price, amount)
                        print(f'''\n{amount} {item} added to {vendor.name.title()}'s stock.
{vendor.name.title()} will buy this for: {buy_price}c, and sell for: {sell_price}c.''')
                        save_vendors(vendors)
                else:
                    print(DNEError)
            elif what == 'remove item':
                print(vendors)
                who = input('Name of Vendor: ').lower().strip()
                vendor = load_vendor(who, vendors)
                if vendor:
                    print('    Vendor Stock')
                    print(vendor.display_stock())
                    item = input('Item: ').lower().strip()
                    amount = int(input('Amount: ').strip())
                    if vendor.check_stock(item):
                        vendor.remove_from_stock(item, amount)
                        print(f'New stock: {item.title()}, {vendor.stock[item]["stock"]}')
                        save_vendors(vendors)
                    else:
                        print(f'{vendor.name.title()} does not have this item.')
                else:
                    print(DNEError)
            elif what == 'delete item':
                print(vendors)
                who = input('Name of Vendor: ').lower().strip()
                vendor = load_vendor(who, vendors)
                if vendor:
                    print('    Vendor Stock')
                    print(vendor.display_stock())
                    item = input('Item: ').lower().strip()
                    if vendor.check_stock(item):
                        # Todo: Maybe add a way to store items for easier re-introduction.
                        confirm = input('Are you sure you want to delete this item? [Y/N]').lower().strip()
                        if confirm in ('y', 'ye', 'yes'):
                            vendor.delete_item_from_stock(item)
                            print(vendor.display_stock())
                            print(f'{item.title()} removed from {vendor.name.title()}\'s stock.')
                            save_vendors(vendors)
                        else:
                            print('Delete aborted.')
                    else:
                        print(DNEError)
                else:
                    print(DNEError)
            elif what == 'new':
                name = input('Name of vendor: ').lower().strip()
                v_type = input('Type of vendor: ').lower().strip()
                # price = input('Price factor: ')
                new_vendor = add_vendor(name, v_type, 0, vendors)
                if new_vendor:
                    new_vendor.automatic_stock()
                    print(new_vendor.display_stock())
                    print(f'{new_vendor.name.title()} has arrived to the Market.')
                    save_vendors(vendors)
                else:
                    print(f'A vendor by that name already exists.')
            elif what == 'delete':
                print(vendors)
                who = input('Name of vendor: ').strip()
                vendor = load_vendor(who, vendors)
                if vendor:
                    confirm = input(f'Are you sure you want to remove {vendor.name.title()}? ').lower().strip()
                    if confirm in ('y', 'ye', 'yes'):
                        remove_vendor(vendor.name, vendors)
                        print('Vendor removed from Market.')
                        save_vendors(vendors)
                    else:
                        print(f'Removal of {vendor.name.title()} aborted.')
                else:
                    print(DNEError)
            elif what == 'info':
                print(vendors)
                who = input('Name of Vendor: ').strip()
                vendor = load_vendor(who, vendors)
                if vendor:
                    print(vendor.info())
                    print(vendor.display_stock())
                else:
                    print(DNEError)
            elif what == 'edit price':
                print(vendors)
                who = input('Name of Vendor: ').lower().strip()
                vendor = load_vendor(who, vendors)
                if vendor:
                    print(vendor.display_stock())
                    item = input('Item: ').lower().strip()
                    new_buy = int(input('Sell: ').strip())
                    new_sell = int(input('Buy: ').strip())
                    vendor.edit_price(item, new_buy, new_sell)
                    save_vendors(vendors)
                    print(vendor.display_stock())
                else:
                    print(DNEError)
            elif what == 'reset stock':
                print(vendors)
                who = input('Name of Vendor: ').lower().strip()
                vendor = load_vendor(who, vendors)
                if vendor:
                    vendor.automatic_stock()
                    print(vendor.display_stock())
                    print(f'{vendor.name.title()}\'s stock has been reset.')
                    save_vendors(vendors)
                else:
                    print(DNEError)
            elif what == 'update vendor':
                print(vendors)
                who = input('Name of Vendor: ').lower().strip()
                vendor = load_vendor(who, vendors)
                if vendor:
                    update_vendor(vendor, vendors)
                    updated_vendor = load_vendor(who, vendors)
                    if vendor:
                        print('Success.')
                        print(updated_vendor.info())
                        save_vendors(vendors)
                    else:
                        print('Something went wrong')
                else:
                    print(DNEError)
            else:
                print('Alrighty then.')

        else:
            print(UCError)
