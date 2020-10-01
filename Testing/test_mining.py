import random
from time import sleep


def chance(t, f):
    """type=int
    t = True,
    f = False"""
    luck = []
    for i in range(0, t):
        luck.append(True)
    for i in range(0, f):
        luck.append(False)
    return luck


mine_inventory = {'pickaxe': {
    'stone': {'count': 1, 'wear': 0},
    'iron': {'count': 1, 'wear': 0},
    'gold': {'count': 1, 'wear': 0},
    'diamond': {'count': 1, 'wear': 0}},
    'minerals': {
        'stone': 0,
        'iron': 0,
        'gold': 0,
        'diamond': 0}}


def mineral_chance(d, g, i, s, f):
    """d = diamond
        g = gold
        i = iron
        s = stone
        f = false
        :type d int
        :type g int
        :type i int
        :type s int
        :type f int
        """
    luck = []
    for a in range(0, d):
        luck.append('diamond')

    for b in range(0, g):
        luck.append('gold')

    for c in range(0, i):
        luck.append('iron')

    for x in range(0, s):
        luck.append('stone')

    for y in range(0, f):
        luck.append('none')

    return luck


def pickaxe_type(type):
    """type = stone, iron, gold, diamond"""
    return mine_inventory['pickaxe'][type]['count']





def mine():
    equip = ''
    while True:
        command = input('What would you like to do at the mine? ').lower()
        if command == 'leave':
            print('you have left the mine!')
            break

        # choose pickaxe
        elif command == 'pickaxe':
            while True:
                command = input('choose pickaxe: ').lower()
                if command == 'stone' and pickaxe_type('stone') >= 1:
                    equip = 'stone'
                    print(f'''
                    you have now choosen {equip} pickaxe.'''
                          )
                    break

                elif command == 'iron' and pickaxe_type('iron') >= 1:
                    equip = 'iron'
                    print(f'''
                    you have now choosen {equip} pickaxe.'''
                          )
                    break

                elif command == 'gold' and pickaxe_type('gold') >= 1:
                    equip = 'gold'
                    print(f'''
                    you have now choosen {equip} pickaxe.'''
                          )
                    break

                elif command == 'diamond' and pickaxe_type('diamond') >= 1:
                    equip = 'diamond'
                    print(f'''
                    you have now choosen {equip} pickaxe.'''
                          )

                    break

                else:
                    print('''
                    you do not own that pickaxe yet, 
                    please buy one in the store'''
                          )
                    break

        # mining minerals
        elif command == 'mine':

            # stone picxace todo:fix wear, and mabye make mining loop
            if equip == 'stone':
                a = random.choice(mineral_chance(0, 0, 5, 50, 20))
                if a != 'none':
                    mine_inventory['minerals'][a] += random.choice([i for i in range(1, 2)])
                    print(f'''
                    you found {a}! 
                    you have now {mine_inventory["minerals"][a]} {a}.'''
                          )
                    mine_inventory['pickaxe']['stone']['wear'] += 50
                elif a == 'none':
                    print('''
                    Crap! you found nothing'''
                          )
                    mine_inventory['pickaxe']['stone']['wear'] += 2.5

                elif mine_inventory['pickaxe']['stone']['wear'] >= 100:
                    mine_inventory['pickaxe']['stone']['count'] -= 1
                    equip = ''

            # iron pickaxe
            elif equip == 'iron':
                a = random.choice(mineral_chance(1, 3, 15, 50, 16))
                if a != 'none':
                    mine_inventory['minerals'][a] += random.choice([i for i in range(1, 4)])
                    print(f'''
                    you found {a}! 
                    you have now {mine_inventory["minerals"][a]} {a}.'''
                          )
                    mine_inventory['pickaxe']['iron']['wear'] += 4

                elif a == 'none':
                    print('''
                    Crap! you found nothing'''
                          )
                    mine_inventory['pickaxe']['iron']['wear'] += 2

            # gold pickaxe
            elif equip == 'gold':
                a = random.choice(mineral_chance(3, 10, 30, 40, 12))
                if a != 'none':
                    mine_inventory['minerals'][a] += random.choice([i for i in range(1, 6)])
                    print(f'''
                    you found {a}! 
                    you have now {mine_inventory["minerals"][a]} {a}.'''
                          )
                    mine_inventory['pickaxe']['gold']['wear'] += 8

                elif a == 'none':
                    print('''
                    Crap! you found nothing'''
                          )
                    mine_inventory['pickaxe']['gold']['wear'] += 4

            # diamond pickaxe
            elif equip == 'diamond':
                a = random.choice(mineral_chance(5, 15, 30, 60, 2))
                if a != 'none':
                    mine_inventory['minerals'][a] += random.choice([i for i in range(1, 6)])
                    print(f'''
                    you found {a}! 
                    you have now {mine_inventory["minerals"][a]} {a}.'''
                          )
                    mine_inventory['pickaxe']['diamond']['wear'] += 2

                elif a == 'none':
                    print('''
                    Crap! you found nothing'''
                          )
                    mine_inventory['pickaxe']['diamond']['wear'] += 0.5

            elif equip == '':
                print('''
                    you have not choosen a pickaxe, 
                    type pickaxe to choose a pickaxe, 
                    type "help" for command options''')

            else:
                print('Unknow command..')

        # print inventory
        elif command == 'inventory':
            print("""
            inventory:
            Pickaxes:                         Minerals: 
               
            Stone pickaxe:      {}            Stone:   {} 
            Iron pickaxe:       {}            Iron:    {} 
            Gold pickaxe:       {}            Gold:    {} 
            Diamond pickaxe:    {}            Diamond: {} 
        
            """.format(pickaxe_type('stone'),
                       mine_inventory['minerals']['stone'],
                       pickaxe_type('iron'),
                       mine_inventory['minerals']['iron'],
                       pickaxe_type('gold'),
                       mine_inventory['minerals']['gold'],
                       pickaxe_type('diamond'),
                       mine_inventory['minerals']['diamond']))

while True:
    user = input('command: ')
    if user == 'exit':
        break
    elif user == 'mine':
        print('You are walking to find a mine...')
        sleep(1)
        print('You found a nice mine, and decide to try it out.')
        sleep(1)
        mine()
