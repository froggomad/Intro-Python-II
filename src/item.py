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

class Container(Item):
    def __init__(self, id, name, description, room_description, inventory):
        super().__init__(id, name, description, room_description, 0)
        self.inventory = inventory        

    def letter_to_int(self, letter):
        alphabet = list('abcdefghijklmnopqrstuvwxyz')
        if letter in alphabet:
            return alphabet.index(letter)
    
    def int_to_letter(self, index):
        alphabet = list('abcdefghijklmnopqrstuvwxyz')
        if len(alphabet) >= index + 1:
            return alphabet[index]

    def list_inventory(self, player):
        #letter a to bytes
        letter_i = self.letter_to_int('a')

        for item in self.inventory:
            #decode to string and make uppercase
            letter_s = self.int_to_letter(letter_i)
            upper_str = letter_s.upper()
            #output            
            print(f"{upper_str}: {item.name}")
            #increment to the next byte (this will convert to the next character)                                    
            letter_i += 1
        if len(self.inventory) > 0:
            loot = input("select a letter to loot an item: ").lower()
            index = self.letter_to_int(loot)

            if isinstance(index, int) and len(self.inventory) >= index + 1:            
                player.take(self.inventory[index])
                self.inventory.pop(index)
            else:
                sys_print(f"{loot} is not an item you can loot from this chest")
        else: 
            sys_print(f"{self.name} is empty!")           

class Weapon(Item):
    def __init__(self, id, name, description, room_description, gold, attack):
        super().__init__(id, name, description, room_description, gold)
        self.attack = attack

class LightSource(Weapon):
    def __init__(self, id, name, description, room_description, gold, attack, lightValue):
        super().__init__(id, name, description, room_description, gold, attack)
        self.lightValue = lightValue

    def __str__(self):
        return f"{self.name} - {self.description} with {self.lightValue} light"

class Gold(Item):
    def __init__(self, id, room_description, gold):
        super().__init__(id, "gold", "", room_description, gold)
        self.description = f"gold - a pile of {gold} gold"