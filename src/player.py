# Write a class to hold player information, e.g. what room they are in
# currently.
from item import Item, Weapon, LightSource
#from adv import sys_print

# TODO: Monster system

class Mob:
    def __init__(self, name, health, experience):
        self.name = name
        self.health = health
        self.experience = experience
        
class Player(Mob):   

    def __init__(self, name, current_room, health, experience = 0, gold = 0):
        fist = Weapon(1, "hand", "empty fist", "", 0, 1)
        
        super().__init__(name, health, experience)        
        self.current_room = current_room
        self.gold = gold
        self.inventory = []
        self.leftHandItem = fist
        self.rightHandItem = fist
        self.attack = 0

    def equipItem(self, hand, item):
        if isinstance(item, Weapon) or isinstance(item, LightSource):            
            if hand == "l":
                self.attack -= self.leftHandItem.attack
                self.leftHandItem = item
                self.attack += item.attack
            elif hand == "r":
                self.attack -= self.rightHandItem.attack
                self.rightHandItem = item
                self.attack += item.attack
            else:
                print(f"{hand} isn't a hand you can equip to. Please choose `l` or `r`")
                return
        else:
            print(f"You can only equip weapons and light sources at this time. {item.name} isn't a weapon or light source.")
            return
        #output
        if hand == "l":
            hand_description = "Left Hand"
        elif hand == "r":
            hand_description = "Right Hand"

        print(f"\nYou've equipped {item} to your {hand_description}")


    def __str__(self):
        return f"{self.name} has {self.health} health, {self.gold} gold, and {self.experience} experience"

class Monster(Mob):
    def __init__(self, name, health, experience):
        super().__init__(name, health, experience)        

    def __str__(self):
        return f"{self.name} has {self.health} health and is worth {self.experience} experience"