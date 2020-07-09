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

    def __init__(self, name, current_room, health, experience = 0, gold = 0):
        fist = Weapon(1, "hand", "empty fist", "", 0, 1)
        
        super().__init__(name, health, experience)        
        self.current_room = current_room
        self.gold = gold
        self.inventory = []
        self.leftHandItem = fist
        self.rightHandItem = fist
        self.attack = self.leftHandItem.attack + self.rightHandItem.attack        
    
    def has_light(self):
        return isinstance(self.leftHandItem, LightSource) or isinstance(self.rightHandItem, LightSource)

    def equipItem(self, hand, item):
        if isinstance(item, Weapon) or isinstance(item, LightSource):
            #remove the item from the current room
            self.current_room.items.remove(item)
            #store the current attack value before equipping a new item (used in output)
            old_attack = self.attack
            had_light = self.has_light()

            if hand == "l":
                self.attack -= self.leftHandItem.attack
                self.leftHandItem = item
                self.attack += item.attack
            elif hand == "r":
                self.attack -= self.rightHandItem.attack
                self.rightHandItem = item
                self.attack += item.attack                
            else:
                sys_print(f"`{hand}` isn't a hand you can equip to. Please choose `l` or `r`")
                return
            
            #Inner-Mark: Output
            
            #Attack value changed:
            if old_attack != self.attack:
                sys_print(f"your attack was {old_attack} and after equipping {item.name} it is now {self.attack}")
            
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

class Monster(Mob):
    def __init__(self, name, health, experience):
        super().__init__(name, health, experience)        

    def __str__(self):
        return f"{self.name} has {self.health} health and is worth {self.experience} experience"