# Write a class to hold player information, e.g. what room they are in
# currently.
from item import Item, Weapon, LightSource

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

    def equipItem(self, hand, item):
        if isinstance(item, Weapon) or isinstance(item, LightSource):
            #remove the item from the current room
            self.current_room.items.remove(item)
            #store the current attack value before equipping a new item (used in output)
            old_attack = self.attack_damage()

            had_light = self.has_light()

            if hand == "l":
                self.leftHandItem = item
            elif hand == "r":
                self.rightHandItem = item       
            else:
                sys_print(f"`{hand}` isn't a hand you can equip to. Please choose `l` or `r`")
                return
            
            #Inner-Mark: Output
            
            #Attack value changed:
            if old_attack != self.attack_damage():
                sys_print(f"your attack was {old_attack} and after equipping {item.name} it is now {self.attack_damage()}")
            
            #light changed:
            if had_light == False and self.has_light() == True:
                sys_print("You can see again!")
        else:
            sys_print(f"You can only equip weapons and light sources at this time. {item.name} isn't a weapon or light source.")
            return
        #output
        if hand == "l":
            hand_description = "Left Hand"
        elif hand == "r":
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

    def dropItem(self, item):
        old_attack = self.attack_damage()
        had_light = self.has_light()

        thisItem = self.get_from_inventory(item)
        if thisItem:
            if thisItem != self.fist:
                if thisItem in self.inventory:
                    self.inventory.remove(thisItem)
                elif thisItem == self.leftHandItem:
                    self.leftHandItem = self.fist
                elif thisItem == self.rightHandItem:
                    self.rightHandItem = self.fist
                self.current_room.items.append(thisItem)
                #Attack value changed:
                if old_attack != self.attack_damage():
                    sys_print(f"your attack was {old_attack} and after equipping {item.name} it is now {self.attack_damage()}")
            
                #light changed:
                if had_light == False and self.has_light() == True:
                    sys_print("You can't see anything!")
            else:
                sys_print("Please, don't try to drop your hands. That would be fatal.")

    def fight(self, monster_name):
        monster = self.find(monster_name)

        if isinstance(monster, Monster):
            sys_print(f"{self.name} is fighting {monster.name}. {self.name} has {self.health} health and {monster} has {monster.health} health" )
            while monster.health > 0 and self.health > 0:
                if monster.health > 0:                    
                    self.health -= monster.attack
                    sys_print(f"{monster.name} hits {self.name} for {monster.attack} damage. {self.name} has {self.health} health remaining")                    

                if self.health > 0:
                    damage = self.attack_damage()                    
                    monster.health -= damage
                    sys_print(f"{self.name} hits {monster.name} for {damage} damage. {monster.name} has {monster.health} health remaining")

            if monster.health <= 0:
                self.current_room.monsters.remove(monster)
                print(f"{monster.name} died!")
            else:
                print(f"{self.name} met their demise by {monster.name}. Thanks for playing!")
                exit(0)
        else:
            sys_print(f"If you really thought you could fight a {monster}, you probably also believe in \"the rock\"!")

    def find(self, monster_name):
        for m in self.current_room.monsters:
            if m.name == monster_name:
                return m

        return monster_name

class Monster(Mob):
    def __init__(self, id, name, health, attack, experience):
        super().__init__(name, health, experience)
        self.attack = attack

    def __str__(self):
        return f"{self.name} has {self.health} health and is worth {self.experience} experience"