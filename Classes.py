
"""Every class used in Adventure text belongs in this file."""
from Functions import *
import pickle
from prettytable import PrettyTable


class Player:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.admin = False

        self.max_hp = 100
        self.current_hp = 100

        self.coins = 0
        self.inv = {}

        self.level = 1
        self.exp = 0
        self.fish_lvl = 1
        self.fish_exp = 0
        self.hunt_lvl = 1
        self.hunt_exp = 0
        self.mine_lvl = 1
        self.mine_exp = 0

    def __repr__(self):
        return self.username

    def __str__(self):
        return self.username

    def info(self):
        information = f'''
    Information about user: [{self.username}]
    Username:   {self.username}
    Admin:      {self.admin}
    
    Main level: {self.level}
    Main exp:   {self.exp}
    HP:         {self.current_hp}/{self.max_hp}
    Fishing:    lvl - {self.fish_lvl}, exp - {self.fish_exp}/{self.fish_lvl * 50}
    Hunting:    lvl - {self.hunt_lvl}, exp - {self.hunt_exp}/{self.hunt_lvl * 50}
    Mining:     lvl - {self.mine_lvl}, exp - {self.mine_lvl}/{self.mine_lvl * 50}
    '''
        return information

    def display_inv(self):
        inventory = PrettyTable(['Item', 'Amount'])
        inventory.add_row(['Coins', self.coins])
        for item in self.inv:
            inventory.add_row([item.title(), self.inv[item]])
        return inventory

    def take_damage(self, damage):
        """Take """
        self.current_hp -= damage
        if self.current_hp <= 0:
            return self.dead()
        else:
            return True

    def heal(self, amount):
        self.current_hp += amount
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp
        return True

    def dead(self):
        self.coins = 0
        if self.level > 1:
            self.level -= 1
        self.current_hp = 30
        self.exp = 0
        self.inv = {}
        print('You died.')
        return True

    def lvl_up(self):
        if self.exp >= self.level * 50:
            self.exp -= self.level * 50
        self.level += 1
        self.max_hp += 10
        print(f'Congratulations, you are now level {self.level}!')
        return True

    def add_exp(self, amount):
        self.exp += amount
        while self.exp >= self.level * 50:
            self.lvl_up()
        return True

    def add_coins(self, coins):
        self.coins += coins
        return self.coins

    def remove_coins(self, coins):
        if self.coins >= coins:
            self.coins -= coins
            return self.coins
        else:
            return self.coins

    def display_inv(self):
        inv = PrettyTable(['Item', 'Amount'])
        for item in self.inv:
            inv.add_row([item.title(), self.inv[item]])
        return inv

    def check_inv(self, item, amount=1):
        item = item.lower()
        if item in self.inv:
            if self.inv[item] >= amount:
                return True
            else:
                return False
        else:
            return False

    def add_to_inv(self, item, amount=1):
        item = item.lower()
        if self.check_inv(item):
            self.inv[item] += amount
            return self.inv
        else:
            self.inv[item] = amount
            return self.inv

    def remove_from_inv(self, item, amount=1):
        if self.check_inv(item, amount):
            self.inv[item] -= amount
            if self.inv[item] == 0:
                self.inv.pop(item)
        return self.inv


class Vendor:

    def __init__(self, name, v_type, price_factor):
        self.name = name
        self.v_type = v_type
        # Stock template
        # '[item]': {'stock': xx, 'buy_price': xx, 'sell_price': xx}
        self.stock = {}
        # Todo: implement price_factor.
        self.price_factor = price_factor
        self.successful_trades = 0
        self.successful_purchases = 0
        self.successful_sales = 0

    def __repr__(self):
        return self.name

    def info(self):
        information = f'''
    Information about vendor: [{self.name}]
    Name:           {self.name}
    Type:           {self.v_type}
    Price factor:   {self.price_factor}
    
    Trades:         {self.successful_trades}
    Sales:          {self.successful_sales}
    Purcases:       {self.successful_purchases}
    '''
        return information

    def display_stock(self):
        stock = PrettyTable(['Item', 'Buy', 'Sell', 'In stock'])
        for item in self.stock:
            stock.add_row([item.title(), f'{self.stock[item]["sell_price"]}c', f'{self.stock[item]["buy_price"]}c', self.stock[item]["stock"]])
        return stock

    def check_stock(self, item, amount=0):
        item = item.lower()
        if item in self.stock:
            if self.stock[item]['stock'] >= amount:
                return True
            else:
                return False
        else:
            return False

    def edit_price(self, item, new_buy, new_sell):
        self.stock[item]['buy_price'] = new_buy
        self.stock[item]['sell_price'] = new_sell
        return self.stock

    def add_to_stock(self, item, amount=1):
        item = item.lower()
        if item in self.stock:
            self.stock[item]['stock'] += amount
        return self.stock

    def remove_from_stock(self, item, amount=1):
        self.stock[item]['stock'] -= amount
        if self.stock[item]['stock'] < 0:
            self.stock[item]['stock'] = 0
        return self.stock

    def new_item_in_stock(self, item, buy_price, sell_price, amount=0):
        self.stock[item] = {'stock': amount, 'buy_price': buy_price, 'sell_price': sell_price}
        return self.stock

    def delete_item_from_stock(self, item):
        self.stock.pop(item)
        return self.stock

    def automatic_stock(self):
        if len(self.stock) > 0:
            self.stock = {}
        stock_items = self.general_stocks()
        for item in stock_items:
            stock = stock_items[item]['stock']
            buy_price = stock_items[item]['buy_price']
            sell_price = stock_items[item]['sell_price']
            self.new_item_in_stock(item, buy_price, sell_price, stock)
        return self.stock

    def general_stocks(self):
        stocks = {'fisherman': {'small net': {'stock': 5, 'buy_price': 5, 'sell_price': 10},
                                'harpoon': {'stock': 5, 'buy_price': 5, 'sell_price': 10},
                                'fishing rod': {'stock': 5, 'buy_price': 5, 'sell_price': 10},
                                'shrimp': {'stock': 0, 'buy_price': 5, 'sell_price': 10},
                                'anchovies': {'stock': 0, 'buy_price': 5, 'sell_price': 10},
                                'tuna': {'stock': 0, 'buy_price': 5, 'sell_price': 10},
                                'herring': {'stock': 0, 'buy_price': 5, 'sell_price': 10},
                                'salmon': {'stock': 0, 'buy_price': 5, 'sell_price': 10},
                                'swordfish': {'stock': 0, 'buy_price': 5, 'sell_price': 10}},
                  'miner': {'pickaxe': {'stock': 5, 'buy_price': 5, 'sell_price': 10},
                            'tnt': {'stock': 0, 'buy_price': 5, 'sell_price': 10},
                            'torch': {'stock': 5, 'buy_price': 5, 'sell_price': 10},
                            'oil': {'stock': 0, 'buy_price': 5, 'sell_price': 10},
                            'coal ore': {'stock': 0, 'buy_price': 5, 'sell_price': 10},
                            'iron ore': {'stock': 0, 'buy_price': 5, 'sell_price': 10}},
                  'lumberjack': {'Axe': {'stock': 5, 'buy_price': 5, 'sell_price': 10},
                                 'Adze': {'stock': 5, 'buy_price': 5, 'sell_price': 10},
                                 'knife': {'stock': 5, 'buy_price': 5, 'sell_price': 10},
                                 'oak logs': {'stock': 0, 'buy_price': 5, 'sell_price': 10},
                                 'willow logs': {'stock': 0, 'buy_price': 5, 'sell_price': 10},
                                 'oak planks': {'stock': 0, 'buy_price': 5, 'sell_price': 10},
                                 'willow planks': {'stock': 0, 'buy_price': 5, 'sell_price': 10},
                                 'charcoal': {'stock': 0, 'buy_price': 5, 'sell_price': 10}},
                  'smith': {'hammer': {'stock': 5, 'buy_price': 5, 'sell_price': 10},
                            'coal': {'stock': 5, 'buy_price': 5, 'sell_price': 10},
                            'charcoal': {'stock': 0, 'buy_price': 5, 'sell_price': 10},
                            'knife': {'stock': 0, 'buy_price': 5, 'sell_price': 10},
                            'axe': {'stock': 0, 'buy_price': 5, 'sell_price': 10},
                            'adze': {'stock': 0, 'buy_price': 5, 'sell_price': 10},
                            'harpoon': {'stock': 0, 'buy_price': 5, 'sell_price': 10},
                            'pickaxe': {'stock': 0, 'buy_price': 5, 'sell_price': 10},
                            'iron': {'stock': 0, 'buy_price': 5, 'sell_price': 10},
                            'steel': {'stock': 0, 'buy_price': 5, 'sell_price': 10}}}
        if self.v_type in stocks:
            return stocks[self.v_type]

if __name__ == '__main__':
    # users = []
    # save_users(users)
    # vendors = []
    # save_vendors(vendors)
    # Charles is the OG Vendor.

    with open('users.pkl', 'rb') as load:
        users = pickle.load(load)

    with open('vendors.pkl', 'rb') as load:
        vendors = pickle.load(load)

    # Trading algorithm
    #
    #   Buy from vendor:
    #   1. Check if vendor has item and enough                      - check_stock(item, amount)
    #   2. Check if user has enough coins                           - user.coin >= amount
    #   3. Remove item(s) from vendor inventory                     - remove_from_stock(item, amount)
    #   4. Remove coins from user inventory                         - remove_coins(amount)
    #   5. Add item(s) to user inventory                            - add_to_inv(item, amount)
    #
    #   Sell to vendor:
    #   1. Check if user has item                                   - check_inv(item, amount)
    #   2. Check if vendor wants item (has item slot in inventory)  - check_stock(item)
    #   3. Remove item from user inventory                          - remove_from_inv(item, amount)
    #   4. Add coins to user inventory                              - add_coins(amount)
    #   5. Add item to vendor inventory                             - add_to_stock(item, amount)
