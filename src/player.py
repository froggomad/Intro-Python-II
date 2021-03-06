# Write a class to hold player information, e.g. what room they are in
# currently.
from item import Item, Weapon, LightSource, Gold


# TODO: Monster system

def sys_print(s):
    print(f"\n***{s}***")

class Mob:
    def __init__(self, name, health, experience):
        self.name = name
        self.health = health
        self.experience = experience
        
class Player(Mob):
    fist = Weapon(1, "hand", "empty fist", "", 0, 1)

    def __init__(self, name, current_room, health, experience = 0, gold = 0):
        super().__init__(name, health, experience)        
        self.current_room = current_room
        self.gold = gold
        self.inventory = []
        self.leftHandItem = self.fist
        self.rightHandItem = self.fist

    def attack_damage(self):        
        return self.leftHandItem.attack + self.rightHandItem.attack
    
    def has_light(self):
        return isinstance(self.leftHandItem, LightSource) or isinstance(self.rightHandItem, LightSource)

    def equipItem(self, item):
        hand = input("Which hand would you like to equip this item to? ").lower()

        if isinstance(item, Weapon) or isinstance(item, LightSource):
           
            #store the current attack value before equipping a new item (used in output)
            old_attack = self.attack_damage()

            had_light = self.has_light()
            if hand == "l" or hand == "r":
                #remove the item from the current room or inventory
                if item in self.current_room.items:
                    self.current_room.items.remove(item)
                elif item in self.inventory:
                    self.inventory.remove(item)
                #equip it
                if hand == "l" or hand == "left":
                    if self.leftHandItem != self.fist:
                        self.inventory.append(self.leftHandItem)
                        self.leftHandItem.to_inventory()
                    self.leftHandItem = item
                elif hand == "r" or hand == "right":
                    if self.rightHandItem != self.fist:
                        self.inventory.append(self.rightHandItem)
                        self.rightHandItem.to_inventory()
                    self.rightHandItem = item
            else:
                sys_print(f"`{hand}` isn't a hand you can equip to. Please choose `l` for left or `r` for right")
                return
            
        #Inner-Mark: Output
            
            #Attack value changed:
            if old_attack != self.attack_damage():
                sys_print(f"your attack was {old_attack} and after equipping {item.name} it is now {self.attack_damage()}")
            
            #light changed:
            if had_light == False and self.has_light() == True:
                sys_print("You can see again!")
        else:
            sys_print(f"You can only equip weapons and light sources at this time. {item} isn't a weapon or light source.")
            return
        
        if hand == "l" or hand == "left":
            hand_description = "Left Hand"
        elif hand == "r" or hand == "right":
            hand_description = "Right Hand"

        #empty line
        print()

        sys_print(f"You've equipped {item} to your {hand_description}")

    def __str__(self):
        return f"{self.name} has {self.health} health, {self.gold} gold, and {self.experience} experience"

    def get_from_inventory(self, item):
        for i in self.inventory:
            if item == i.name:
                return i
        if item == self.leftHandItem.name:
            return self.leftHandItem
        elif item == self.rightHandItem.name:
            return self.rightHandItem
        sys_print(f"Item not found: {item}")

    def take(self, item_name):
        item = self.find(item_name)
        if isinstance(item, Item):
            if item.name == "golden_sword" and not hasattr(self, 'arthur'):
                sys_print("Did you think you could just take that? It's obviously buried to the hilt!")
                return

            if isinstance(item, LightSource) or isinstance(item, Weapon):            
                self.equipItem(item)
            elif item.id != 1:
                item.to_inventory()
                self.inventory.append(item)
            else:
                sys_print(f"You aren't able to equip {item}. Try inspecting it")

    def pull(self, item_name):
        item = self.find(item_name)
        if isinstance(item, Item):
            if item.name == "golden_sword":
                self.equipItem(item)
            else:
                print(f"""
You pull {item_name} with all your might, but nothing happens.
Did you mean to pull your finger?
                """)
        elif item_name == "finger":
                sys_print("You're disgusting!")
        else: sys_print("Invalid item to pull. What were you thinking?")

    def letter_to_int(self, letter):
        alphabet = list('abcdefghijklmnopqrstuvwxyz')
        if letter in alphabet:
            return alphabet.index(letter)
    
    def int_to_letter(self, index):
        alphabet = list('abcdefghijklmnopqrstuvwxyz')
        if len(alphabet) >= index + 1:
            return alphabet[index]

    def list_inventory(self):
        if self.leftHandItem.name == "hand":
            print(f"Left Hand: fist")
        else:
            print(f"Left Hand: {self.leftHandItem}")

        if self.rightHandItem.name == "hand":
            print(f"Right Hand: fist")
        else:
            print(f"Right Hand: {self.rightHandItem}")

        
        for item in self.inventory:            
            #output            
            print(f"{item.name}")
            #increment to the next byte (this will convert to the next character)                                    
            

        equippables = [i.name for i in self.inventory if isinstance(i, Weapon) or isinstance(i, LightSource)]

        if len(equippables) > 0:
            sys_print("Items you can equip:")
            #empty line
            print()

            #decode to string and make uppercase
            letter_i = self.letter_to_int('a')
            for item in equippables:
                letter_s = self.int_to_letter(letter_i)
                upper_str = letter_s.upper()

                print(f"{upper_str}: {item}")
                letter_i += 1

            loot = input("select a letter to loot an item: ").lower()
            index = self.letter_to_int(loot)

            equip_item = self.get_from_inventory(equippables[index])

            if len(equippables) >= index + 1:
                self.equipItem(equip_item)

    def find(self, item_name):
        for i in self.current_room.items:
            if item_name == i.name:
                return i
        return item_name

    def dropItem(self, item_name):
        old_attack = self.attack_damage()
        had_light = self.has_light()

        this_item = self.get_from_inventory(item_name)
        if this_item:
            if this_item != self.fist:
                if this_item in self.inventory:
                    self.inventory.remove(this_item)
                elif this_item == self.leftHandItem:
                    self.leftHandItem = self.fist
                elif this_item == self.rightHandItem:
                    self.rightHandItem = self.fist
                self.current_room.items.append(this_item)
                this_item.to_floor()

                #Attack value changed:
                if old_attack != self.attack_damage():
                    sys_print(f"your attack was {old_attack} and after dropping {this_item.name} it is now {self.attack_damage()}")
            
                #light changed:
                if had_light == True and self.has_light() == False:
                    sys_print("You can't see anything!")
            else:
                if hasattr(self, "hand_drop"):
                    hand = input(f"Which hand would you like to drop? ")
                    print("""
                    You pull and pull with all your might, finally loosening
                    the connection between your wrist and forearm.
                    """)
                    sys_print(f"You drop your {hand} hand for {self.health} damage")
                    sys_print(f"{self.name} died of a not listening overdose.")
                    exit(0)
                else:
                    sys_print("Please, don't try to drop your hands. That would be fatal.")
                    self.hand_drop = True

    def fight(self, monster_name):
        monster = self.find_monster(monster_name)

        if isinstance(monster, Monster):
            sys_print(f"{self.name} is fighting {monster.name}. {self.name} has {self.health} health and {monster} has {monster.health} health" )
            while monster.health > 0 and self.health > 0:
                if monster.health > 0:
                    self.health -= monster.attack
                    sys_print(f"{monster.name} hits {self.name} for {monster.attack} damage. {self.name} has {self.health} health remaining")

                if self.health > 0:
                    damage = self.attack_damage()
                    if self.has_light():
                        sys_print(f"{self.name} hits {monster.name} for {damage} damage. {monster.name} has {monster.health} health remaining")
                        monster.health -= damage
                    else:
                        self.health -= damage
                        print(f"You try your best to hit {monster.name} but you can't see anything!")
                        sys_print(f"You hit yourself for {damage} damage! You have {self.health} health remaining")

            if monster.health <= 0:
                self.current_room.monsters.remove(monster)
                print(f"{monster.name} died!")
            else:
                print(f"{self.name} met their demise by {monster.name}. Thanks for playing!")
                exit(0)
        else:
            sys_print(f"If you really thought you could fight a {monster}, you probably also believe in \"the rock\"!")

    def find_monster(self, monster_name):
        for monster in self.current_room.monsters:
            if monster.name == monster_name:
                return monster
            else:
                return monster_name

class Monster(Mob):
    def __init__(self, id, name, room_description, health, attack, experience):
        super().__init__(name, health, experience)
        self.attack = attack
        self.room_description = room_description

    def __str__(self):
        return f"{self.name} has {self.health} health. {self.name} is worth {self.experience} experience"


class Merchant(Player):
    def __init__(self, current_room, room_description):        
        super().__init__("merchant", current_room, 10000, 0, 10000000)
        self.room_description = room_description
        armor = Item(9999, "armor", "some armor", "", 10)
        self.inventory = [armor]
        