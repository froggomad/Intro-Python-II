class Item:
    def __init__(self, id, name, description, room_description, gold):
        self.id = id
        self.name = name
        self.description = description
        self.room_description = room_description
        self.gold = gold

    def __str__(self):
        return f"{self.name} worth {self.gold} gold"

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