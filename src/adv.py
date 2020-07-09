from room import Room, Item
from item import Item, Weapon, LightSource
from player import Player, Monster
from os import system, name

#Item list
torch = LightSource(
    0,
    "torch",
    "a crude stick with an oil soaked rag at its tip",
    "a torch lies on the floor next to it, hastily discarded.",
    0,
    0,
    4
)

broken_chest = Item(
    1,
    "chest",
    "its lock clearly having been picked by an adventurer before you, and it's contents emptied - there's nothing you can do with this.",
    "a battered wooden chest sits in the corner",
    0
)

rusty_sword = Weapon(
    2,
    "rusty_sword",
    "rusting, it could probably do better if it were sharpened",
    "a rusty sword lies nearby under a drip somewhere on the cavern's ceiling",
    2,
    4
)

golden_sword = Weapon(
    3,
    "golden_sword",
    "This brilliant blade has clearly been well taken care of",
    "a golden sword lies buried to the hilt in a large stone just before the mouth of the chasm",
    2000,
    200
)

#Monster list
small_spider = Monster(
    0,
    "spider",
    5,
    1,
    1
)

skeleton = Monster(
    1,
    "skeleton",
    10,
    3,
    5
)

dragon = Monster(
    2,
    "dragon",
    200,
    88,
    1000
)


# Declare all the rooms
rooms = {

    'outside': Room(
        "Outside Cave Entrance",
        """
        You are standing to the South of the mouth of what
        appears to be a large cavern. It's dark inside of the
        cavern, but you think you make out the shadow of what
        appears to be a foyer with connected rooms...
        There also appears to be something skittering on the floor.
        """,
        [broken_chest, torch],
        []
    ),

    'foyer': Room(
        "Foyer",
        """
        Dim light filters in from the south. Dusty
        passages run north and east.
        """,
        [broken_chest, rusty_sword],
        [small_spider]
    ),

    'overlook': Room(
        "Grand Overlook",
        """
        A steep cliff appears before you, falling
        into the darkness. Ahead to the north, a light flickers in
        the distance, but there is no way across the chasm.
        """,
        [golden_sword],
        [skeleton]),
    'narrow':   Room(
        "Narrow Passage",
        """
        The narrow passage bends here from west
        to north. The smell of gold permeates the air.
        """,
        [],
        []
    ),

    'treasure': Room(
        "Treasure Chamber",
        """
        You've found the long-lost treasure
        chamber! Sadly, it has already been completely emptied by
        earlier adventurers. A dragon stubbornly guards the far end
        of the room. The only exit is to the south.
        """,
        [],
        [dragon]
    ),
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
#initial room
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

def help():
    return """
            A friendly digitized voice that seems out of place in this dank, harsh environment says to you:

            * [L] to look around
            * [N,S,E,W] to travel
            * [Inspect] [item] to inspect an item 
                (ex: `inspect rock` to inspect an item named rock)
            * [Take] [item] to take an item 
                (ex: `take rock` to take a rock)
            * [Drop] [item] to drop an item 
                (ex: `drop rock` to drop a rock)
            * [Equip] [Item] to equip an item in your inventory 
                (ex: `equip sword` to equip a sword you already have)
            * [Q|q] to quit

            Written on the wall nearby you see a message, hastily scrawled:
            The rock is a lie
        """

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

def travel(input):    
    availableDirs = directions()

    input = input.lower()
    if input in availableDirs:
        if input == "n" or input == "north":
            player.current_room = player.current_room.n_to
        elif input == "s" or input == "south":
            player.current_room = player.current_room.s_to
        elif input == "e" or input == "east":
            player.current_room = player.current_room.e_to
        elif input == "w" or input == "west":
            player.current_room = player.current_room.w_to
    else:
        sys_print("There's nothing in that direction. Try again.")

def look():
    if player.has_light() or player.current_room == rooms['outside']:
        sys_print("You look around the room and see:")

        item_instructions = "try \"take rock\" to take a rock, or \"inspect rock\" to inspect it"
        monster_instructions = "try \"fight spider\" to fight a spider"    

        #empty line
        print()

        if len(player.current_room.items) == 0:
            print(f"There are no items here. If there were, you could {item_instructions}")
            item_instructions = ""

        if len(player.current_room.monsters) == 0:
            print(f"There are no monsters here. If there were, you could {monster_instructions}")
            monster_instructions = ""

        #print the room_description(s)
        item_descs = [x.room_description for x in player.current_room.items]
        for i, _ in enumerate(item_descs):
            print(f"{player.current_room.items[i].name}: {item_descs[i]}")
        #empty line
        print()
        #print monsters in the room:
        for i in player.current_room.monsters:
            print(i.name)
        instructions = item_instructions + "\n" + monster_instructions
        sys_print(f"\n{instructions}\n")
    else:
        sys_print(f"Maybe if you had some light, you could see what the heck was happening!")

def inspect(item):    
    if isinstance(item, Item):
        sys_print(f"You are inspecting a(n) {item.name}")
        print(item.description)
    else:
        return

def prompt(s):
    # print a lit of commands, printing every other element in directions as a str
    commands = f"([l|L] to look around | {' | '.join(directions())} to travel | [q|Q] to quit | [Help|?] for common commands): "
    prompt = f"\nWhat would you like to do, {player.name}?\n{commands}"

    return input(s + prompt)

def parse(input):
    input = input.lower()
    clear()
    inputList = input.split()
    if len(inputList) > 1:
        cmd1 = inputList[0]
        cmd2 = inputList[1]

        if cmd2 == "rock":
                if player.current_room != rooms['treasure']:
                    sys_print("The rock is a lie!!!")
                else:
                    sys_print("You win! ... ... a rock? Thanks for playing!")
                    #empty line
                    print()
                    exit(0)
                return

        if cmd1 == "take":
                player.take(cmd2)
                return

        elif cmd1 == "inspect":            
            item = player.find(cmd2)
            inspect(item)
            return

        elif cmd1 == "equip":
            item = player.get_from_inventory(cmd2)
            player.equipItem(item)
            return

        elif cmd1 == "drop":
            player.dropItem(cmd2)
            return

        elif cmd1 == "fight":            
            player.fight(cmd2)
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

while True:
    # check if the player can see
    if player.has_light() == True or player.current_room == rooms['outside']:
        sys_print(f"{player.current_room.name}")
        p = prompt(f"\n{player.current_room.description}\n")
    else:
        dark_text = "It's dark. Maybe you should find some light"
        
        if player.current_room == rooms['overlook']:
            print("""
You stumble forward, hands in front of you - feeling
for something to familiarize yourself with.

You hear an echo and see a light in the distance.
You continue forward...""")
            sys_print("You have fallen to your death!")
            # empty line
            print()
            exit(0)
        else:
            p = prompt(f"\n{dark_text}\n")
    parse(p)