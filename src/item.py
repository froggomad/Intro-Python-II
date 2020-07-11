def sys_print(s):
    print(f"\n***{s}***")

class Item:
    def __init__(self, id, name, description, room_description, gold):
        self.id = id
        self.name = name
        self.description = description
        self.room_description = room_description
        self.gold = gold

    def __str__(self):
        return f"{self.name} worth {self.gold} gold"

    def to_inventory(self):
        sys_print(f"{self.name} was placed in your inventory")

    def to_floor(self):
        sys_print(f"{self.name} was dropped on the floor.")

class Weapon(Item):
    def __init__(self, id, name, description, room_description, gold, attack):
        super().__init__(id, name, description, room_description, gold)
        self.attack = attack

class LightSource(Weapon):
    def __init__(self, id, name, description, room_description, gold, attack, lightValue):
        super().__init__(id, name, description, room_description, gold, attack)
        self.lightValue = lightValue

    def __str__(self):
        return f"a {self.name} - {self.description} with {self.lightValue} light"

class Gold(Item):
    def __init__(self, id, room_description, gold):
        super().__init__(id, "gold", "", room_description, gold)
        self.description = f"a pile of {gold} gold"