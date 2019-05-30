# lab26.py
'''Skeleton Dungeon'''

import random

'''Game Classes'''

# Separate classes for each type of enemy, designated with different unicode symbols
class Entity:
    def __init__(self, location_i, location_j, character):
        self.location_i = location_i
        self.location_j = location_j
        self.character = character

class Player(Entity):
    def __init__(self, location_i, location_j):
        super().__init__(location_i, location_j, '☺')

class Zombie(Entity):
    def __init__(self, location_i, location_j):
        super().__init__(location_i, location_j, '۞')

class Skeleton(Entity):
    def __init__(self, location_i, location_j):
        super().__init__(location_i, location_j, '࿈')

class Matador(Entity):
    def __init__(self, location_i, location_j):
        super().__init__(location_i, location_j, '☠')

class Lich(Entity):
    def __init__(self, location_i, location_j):
        super().__init__(location_i, location_j, '࿇')

class Bomb(Entity):
    def __init__(self, location_i, location_j):
        super().__init__(location_i, location_j, '⨶')

# Creates the board and records the location of entities
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def random_location(self):
        return random.randint(0, self.width - 2), random.randint(0, self.height - 2)

    def print(self, entities):
        for i in range(self.height):
            for j in range(self.width):
                for k in range(len(entities)):
                    if entities[k].location_i == i and entities[k].location_j == j:
                        print(entities[k].character, end=' ')
                        break
                else: # the else executes if the loop does NOT break
                    print('  ', end='') # no entity found, break
            print('|')

# Keeps track of score that goes up every time you slay an enemy
class Score:
    def __init__(self, score = 0):
        self.score = score

# different enemies give different levels of points
    def get_points(self, monster):
        point_dict = {
        'zombie': 1,
        'skeleton': 5,
        'lich': 10,}
        self.score += point_dict[monster]

# victory at over 30 points
    def score_victory(self):
        if self.score > 30:
            return True

    def check_points(self):
        return f'You have {self.score} points.'

# keeps track of inventory, items drop whenever you kill an enemy
class Inventory:
    def __init__(self, items = []):
        self.items = items

# there is a random chance to get a trash item that doesn't contribute to the win condition
    def get_item(self, mon_type):
        self.mon_type = mon_type
        item_dict = {
          'zombie': ['useless decoration', 'wilted salad'],
          'skeleton': ['notched saber', 'bony finger'],
          'lich': ['phylactery', 'old laundry']}
        lucky_draw = []
        for item in item_dict[mon_type]:
            lucky_draw.append(item)
        add_item = random.choice(lucky_draw)
        self.items.append(add_item)
        return f'You received "{add_item}."'

# when you have all three items in the victory list, you can defeat Matador
    def item_victory(self):
        winning = 0
        victory_list = ['useless decoration', 'notched saber', 'phylactery']
        for item in victory_list:
            if item in self.items:
                winning += 1
        if winning == 3:
            return True

    def check_inventory(self):
        return f'You have {self.items}'


'''Flavor Functions'''
# Functions for fun that play at specific triggers to tell the player what's going on.

def flavor_intro(instring):
    if instring == 'zombie':
        return 'A zombie shambles blindly into you.'
    if instring == 'skeleton':
        return 'A skeleton warrior draws their sword, gnashing their teeth.'
    if instring == 'lich':
        return 'An undead sorcerer, a lich, turns to you with empty eye sockets.'
    if instring == 'matador':
        return 'A skeleton matador challenges you, swearing they will once again prove victorious.'
    if instring == 'bomb':
        return 'You run into a bomb and explode. Life is unfair. Like this game.'

def flavor_combat(monster, action):
    if monster == 'zombie':
        effective = ['attack', 'magic', 'throw', 'dance']
        if action in effective:
            result = 'win'
            if action == 'attack':
                flavor = 'You easily slay the zombie by removing the head or destroying the brain.'
            elif action == 'magic':
                flavor = 'You blow the zombie up. They were just minding their own business, you know.'
            elif action == 'throw':
                flavor = 'You throw a flaming torch at the zombie. They don\'t even notice themselves burning to ash.'
            elif action == 'dance':
                flavor = 'You and the zombie have a dance off. They leave, impressed with your moves.'
        else:
            flavor ='The zombie has no idea what you\'re trying to do and just eats you.'
            result = 'lose'

    elif monster == 'skeleton':
        effective = ['attack', 'magic']
        if action in effective:
            result = 'win'
            if action == 'attack':
                flavor = 'You fight the skeleton warrior. No bones about it; you\'re much stronger.'
            elif action == 'magic':
                flavor = 'Your spells shatter the skeleton warrior, leaving only a chittering skull.\nNot enough calcium, apparently.'
        else:
            result = 'lose'
            if action == 'throw':
                flavor = 'You hurl a throwing star straight through the skeleton\'s ribcage. Good job.'
            elif action == 'dance':
                flavor = 'You dance with the skeleton. Their grave gyrations chill you to the bone.'
            else:
                flavor = 'The skeleton warrior has a bone to pick with you.'

    elif monster == 'lich':
        effective = ['throw']
        if action in effective:
            result = 'win'
            flavor = 'You shatter a canopic jar at the lich\'s waist with a throwing star.\nIt contained their spirit, and the lich turns to dust.'
        else:
            result = 'lose'
            if action == 'attack':
                flavor = 'You attempt to slice the lich but they turn your sword into a string of beetles.\nGross.'
            elif action == 'magic':
                flavor = 'Trying to beat an undead sorcerer in a magic duel?\n...lol'
            elif action == 'dance':
                flavor = 'The lich is a horrible dancer. Rigor mortis isn\'t fun.\nThey\'re also a horrible loser, as you find out, engulfed in flames.'
            else:
                flavor = 'Is it lich or liche? Anyway, they kill you.'

    elif monster == 'matador':
        result = 'lose'
        if action == 'attack':
            flavor = 'Your sword hits nothing but the red capote. They skewer you with an obnoxious flourish.'
        elif action == 'magic':
            flavor = 'They are too impatient to let you finish casting. You bleed out cursing at how unfair it is.'
        elif action == 'throw':
            flavor = 'Your throwing star ruins the red capote, which only makes the matador really, really mad.'
        elif action == 'dance':
            flavor = 'The matador dances circles around you, being experienced at pasadoble. You feel so embarrassed you could die.\nAnd you do.'
        else:
            flavor = 'The matador wasn\'t kidding.'
    return (flavor, result)

box = Inventory()
exp = Score()

board = Board(25, 25)

pi, pj = board.random_location()
player = Player(pi, pj)

entities = [player]
enemies = []
enemy_types = []

for i in range(6):
    ei, ej = board.random_location()
    enemy = Zombie(ei, ej)
    entities.append(enemy)
    enemies.append(enemy)
    enemy_types.append('zombie')

for i in range(4):
    ei, ej = board.random_location()
    enemy = Skeleton(ei, ej)
    entities.append(enemy)
    enemies.append(enemy)
    enemy_types.append('skeleton')

for i in range(3):
    ei, ej = board.random_location()
    enemy = Lich(ei, ej)
    entities.append(enemy)
    enemies.append(enemy)
    enemy_types.append('lich')

for i in range(4):
    ei, ej = board.random_location()
    enemy = Bomb(ei, ej)
    entities.append(enemy)
    enemies.append(enemy)
    enemy_types.append('bomb')

for i in range(1):
    ei, ej = board.random_location()
    enemy = Matador(ei, ej)
    entities.append(enemy)
    enemies.append(enemy)
    enemy_types.append('matador')

while True:

    board.print(entities)

    command = input('what is your command? ').lower()  # get the command from the user

    if command == 'done':
        break  # exit the game
    elif command in ['inv', 'i', 'inventory', 'inventory check', 'check inventory', 'itm', 'items']:
        print(box.check_inventory())
    elif command in ['pts', 'p', 'points', 'point check', 'check points', 'score', 'check score']:
        print(exp.check_points())
    elif command in ['l', 'left', 'w', 'west']:
        player.location_j -= 1  # move left
        if player.location_j < 0:
            player.location_j += 1
            print('You can\'t go that way.')
    elif command in ['r', 'right', 'e', 'east']:
        player.location_j += 1  # move right
        if player.location_j > 24:
            player.location_j -= 1
            print('You can\'t go that way.')
    elif command in ['u', 'up', 'n', 'north']:
        player.location_i -= 1  # move up
        if player.location_i < 0:
            player.location_i += 1
            print('You can\'t go that way.')
    elif command in ['d', 'down', 's', 'south']:
        player.location_i += 1  # move down
        if player.location_i > 24:
            player.location_i -= 1
            print('You can\'t go that way.')

    for enemy in enemies:
        if enemy.location_i == player.location_i and enemy.location_j == player.location_j:
            for index in range(len(enemies)):
                if enemies[index] == enemy:
                    for i in range(len(enemy_types)):
                        if i == index:
                            finder = i
                            encounter_type = enemy_types[index]
                    print(flavor_intro(encounter_type))
                    if encounter_type == 'bomb':
                        print('\nYou Died.')
                        exit()
                    elif encounter_type == 'matador':
                        slow_matador = box.item_victory()
                        if slow_matador == True:
                            print('You slay the infamous matador and obtain their red capote. You win!')
                            exit()
                    action = input('What will you do? ').lower()
                    result = flavor_combat(encounter_type, action)
                    print(result[0])
                    if result[1] == 'win':
                        for j in range(len(enemy_types)):
                            if j == finder:
                                enemy_types.remove(enemy_types[j])
                        entities.remove(enemy)
                        enemies.remove(enemy)
                        item = box.get_item(encounter_type)
                        print(item)
                        reward = exp.get_points(encounter_type)
                        exp_victory = exp.score_victory()
                        if exp_victory == True:
                            print('You\'ve become strong enough to escape the dungeon. You win!')
                            exit()
                        break
                    else:
                        print('\nYou Died.')
                        exit()
