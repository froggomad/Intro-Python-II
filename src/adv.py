from room import Room, Item
from item import Item, Weapon, LightSource
from player import Player, Monster
from os import system, name

#Item list

items = {}
torch = LightSource(0,                            
                    "torch",
                    "a crude stick with an oil soaked rag at its tip",
                    "a torch lies on the floor next to it, hastily discarded.",
                    0,
                    1,
                    4)
t = torch.name
items[t] = torch

brokenChest = Item(1,
            "chest",
            "its lock clearly having been picked by an adventurer before you, and it's contents emptied - there's nothing you can do with this.",
            "a battered wooden chest sits in the corner",            
            0)
bc = brokenChest.name
items[bc] = brokenChest


# Declare all the rooms
rooms = {
    'outside':  Room("Outside Cave Entrance",

"""You are standing to the South of the mouth of what
appears to be a large cavern. It's dark inside of the
cavern, but you think you make out the shadow of what
appears to be a foyer with connected rooms...

There also appears to be something skittering on the floor.""",
                        
                     [brokenChest, torch]),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east.""", []),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""", []),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air.""", []),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""", []),
}

# Link rooms together

rooms['outside'].n_to = rooms['foyer']
rooms['foyer'].s_to = rooms['outside']
rooms['foyer'].n_to = rooms['overlook']
rooms['foyer'].e_to = rooms['narrow']
rooms['overlook'].s_to = rooms['foyer']
rooms['narrow'].w_to = rooms['foyer']
rooms['narrow'].n_to = rooms['treasure']
rooms['treasure'].s_to = rooms['narrow']

room = rooms['outside']

#
# Main
#

# Print important messages
def sys_print(s):
    print(f"\n***{s}***")

def clear():
    if name == "nt":
        system("cls")
    else:
        system("clear")
    
# Make a new player object that is currently in the 'outside' room.
i = input("Welcome to Cavern of Marvelous Adventures! Please enter your name:\n")
player = Player(i, room, 100, 0, 0)

clear()
sys_print(f"Welcome to your doom, {player.name}")
# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.
def help():
    return """
            A friendly digitized voice that seems out of place in this dank, harsh environment says to you:

            * [L] to look around
            * [N,S,E,W] to travel
            * [Inspect] [item] to inspect an item (ex: `inspect rock` to inspect an item named rock)
            * [Take] [item] to take an item (ex: `take rock` to take a rock)
            * [Q|q] to quit

            Written on the wall nearby you see a message, hastily scrawled:
            The rock is a lie
        """

def travel(input):    
    availableDirs = directions()

    input = input.lower()
    if input in availableDirs:
        if input == "n":
            player.current_room = player.current_room.n_to
        elif input == "s":
            player.current_room = player.current_room.s_to
        elif input == "e":
            player.current_room = player.current_room.e_to
        elif input == "w":
            player.current_room = player.current_room.w_to
    else:
        sys_print("There's nothing in that direction. Try again.")

def parse(input):
    input = input.lower()
    clear()
    inputList = input.split()
    if len(inputList) > 1:
        cmd1 = inputList[0]
        cmd2 = inputList[1]

        if cmd2 == "rock":
                sys_print("The rock is a lie!!!")
                return

        if cmd1 == "take":
            item = get(cmd2)
            if item:
                take(item)
                return
        elif cmd1 == "inspect":            
            item = get(cmd2)
            inspect(item)
            return
        if len(inputList) >2:
            sys_print("warning, a maximum of 2 commands (words separated by a space) will be used")
            return
    else:    
        dirs = ["n", "e", "s", "w"]
        
        if input == "q":
            exit(0)
        elif input == "help" or input == "?" or input.lower() == "h":
            print(help())
            return
        elif input in dirs:
            travel(input)
            return
        elif input == "l":
            look()
            return        
    sys_print("invalid command")

def look():    
    sys_print("You look around the room and see:")
    instructions = "try \"take rock\" to take a rock, or \"inspect rock\" to inspect it"
    #empty line
    print()
    if player.current_room.items == 0:
        print(f"Nothing. If there were items here, you could {instructions}")
    #print the room_description(s)
    item_descs = [x.room_description for x in player.current_room.items]
    for i, _ in enumerate(item_descs):
        print(f"{player.current_room.items[i].name}: {item_descs[i]}")
    
    # print(f"{item_names}\n{item_descs}\n")
    sys_print(instructions)

def get(item_name):
    try:
        item = items[item_name]
    except KeyError:
        sys_print(f"{item_name} isn't a valid item name")
        return
    return item

def inspect(item):    
    if isinstance(item, Item):
        sys_print(f"You are inspecting a(n) {item.name}")
        print(item.description)
    else:
        return

def take(item):
    if isinstance(item, LightSource) or isinstance(item, Weapon):
        hand = input(f"{item.name} is equippable. Which hand would you like to equip it in? l or L for left | r or R for right:")
        player.equipItem(hand, item)
    else:
        if item.id != 1:            
            player.inventory.append(item)
        else:
            sys_print(f"You aren't able to equip {item}. Try inspecting it")

def directions():
    directions = []

    if hasattr(player.current_room, "n_to"):
        directions.append("n")
    if hasattr(player.current_room, "s_to"):
        directions.append("s")
    if hasattr(player.current_room, "e_to"):
        directions.append("e")
    if hasattr(player.current_room, "w_to"):
        directions.append("w")

    return directions

def prompt(s):
    # print a lit of commands, printing every other element in directions as a str
    commands = f"([l|L] to look around | {' | '.join(directions())} to travel | [q|Q] to quit | [Help|?] for common commands): "
    prompt = f"\nWhat would you like to do, {player.name}?\n{commands}"

    return input(s + prompt)

while True:
    p = prompt(f"\n{player.current_room.description}\n")
    parse(p)