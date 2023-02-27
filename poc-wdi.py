#!/home/mike/script/game/venv/bin/python
import blessed
import random

term = blessed.Terminal()


class NPC:

    def __init__(self, name):
        self.name = name
        self.location = None
        self.roam = {}  # { "Game Status", [[site1, lingertime],[site2, lingertime],...}

    def set_location(self, location):
        self.location = location

    def roaming_pattern(self, status, site, lingertime):
        self.roam[(status, site)] = [ lingertime]

    def random_move(self, state):

        where_to_go = [self.location]
        probability_to_go = [0]
        available_exists = locations[self.location].exit_list()
        for (roam_state, roaming_location) in list(self.roam):
            if roam_state == state and roaming_location in available_exists:
                where_to_go.append(roaming_location)
                probability_to_go.append(self.roam[(state,roaming_location)][0])

        ## Remain in the same place as much as
        probability_to_go[0] = max(probability_to_go[1:])*15

        ## Goto exit or remain in the same place according to weights
        go_to = random.choices(where_to_go, weights=probability_to_go, k=1)
        self.location = go_to[0]


class Location:

    def __init__(self, title, description):

        self.title = title
        self.description = description
        self.go_east = None
        self.go_west = None
        self.go_north = None
        self.go_south = None

    def __str__(self):
        return self.title

    def exits(self):
        exit_string = ""
        if self.go_north is not None:
            exit_string = "North you go to " + self.go_north
        if self.go_south is not None:
            exit_string = exit_string + ". South you go to " + self.go_south
        if self.go_west is not None:
            exit_string = exit_string + ". West you go to " + self.go_west
        if self.go_east is not None:
            exit_string = exit_string + ". East you go to " + self.go_east
        return exit_string

    def exit_list(self):
        exit_list = []
        if self.go_north is not None:
            exit_list.append(self.go_north)
        if self.go_south is not None:
            exit_list.append(self.go_south)
        if self.go_west is not None:
            exit_list.append(self.go_west)
        if self.go_east is not None:
            exit_list.append(self.go_east)
        return exit_list

    def north(self, loc):
        self.go_north = loc

    def south(self, loc):
        self.go_south = loc

    def east(self,loc):
        self.go_east = loc

    def west(self,loc):
        self.go_west = loc


listofloc = [["Deck",\
              "Port side deck of the ship. It is where guests board the ship. A Door lies north to the Ships Salon-bar."],
             ["Salon",\
              " Ship Salon equipped with a bar and comfortable seats. This is also used as the restaurant area "],
             ["Women's Quarters",
              "The women's quarters, The area is tastefully decorated with ornate wood paneling, plush carpets, and elegant furniture. \
               The walls are adorned with art, fine draperies, and other luxurious touches."],
             ["VIP Quarters",
              "The VIP cabins are spacious and elegantly appointed, with plush carpets, fine furnishings, and tasteful \
              artwork adorning the walls. The lighting is subdued, lending the space an air of quiet opulence."],
             ["Writer's Cabin",
              "The cabin itself is designed with the needs of a writer in mind, with a spacious writing desk, a \
              comfortable armchair, and a collection of books and writing supplies. The bed is plush and inviting, \
              with soft linens and a variety of pillows to ensure a good night's rest."],
             ["Corridor",
              "A long, narrow passageway that is both functional and stylish. A plush carpet underfoot that muffles the sound of your footsteps.\
              The lighting is dim, with softly glowing lamps spaced at regular intervals along the walls. As you walk, you catch the faint scent\
               of perfume or cologne, a reminder of the luxury and refinement of the ship."],
             ["Infirmary",
              "The infirmary consists of a single room, with just a few beds pushed up against the walls. There's a \
              small table with some basic medical supplies, including bandages and antiseptics, but nothing that would \
              be considered state-of-the-art by today's standards."],
             ["Smoking Room","The walls are paneled in rich mahogany, and intricate carvings and decorations adorn every\
              surface. The room is divided into several sections, each designed for a different purpose. There's a large \
              central area with a grouping of comfortable armchairs and sofas, perfect for lounging and enjoying a cigar \
              or pipe. A smaller alcove off to one side contains a bar, complete with an array of fine wines, spirits, \
              and liqueurs."],
             ["Library",
              "As you step into the small library, you're struck by the warmth and intimacy of the surroundings. The\
               room is small, with just a handful of bookcases lining the walls, but it's filled with the scent of \
               old books and polished wood."],
             ["Cargo","The air is thick with the scent of oil, wood, and other materials, and you can hear the \
             creaking and groaning of the ship's hull as it rolls on the waves. The lighting is sparse, with just \
             a few flickering lanterns and candles providing a dim glow that barely penetrates the darkness.\
                As you move deeper into the hold, you realize just how much cargo the ship is carrying. There are \
                crates of food and drink, barrels of oil and other chemicals, and sacks of grain and other materials. \
                The space is cramped and cluttered, with just enough room for the crew to move around and perform their\
                 duties."],
             ["Bridge", "At the center of the room is the helm, a large wooden wheel that the ship's steerer uses to \
             control the ship's direction. A series of gauges and dials line the walls, providing information on the \
             ship's speed, direction, and other critical data.\
             The captain's chair is positioned near the front of the room, facing forward to provide an unobstructed \
             view of the ship's path. Maps and charts are spread out across a nearby table, and the captain and crew \
             frequently consult them to plot their course and make adjustments as needed."]]


locations = {}
for [title, desc] in listofloc:
    e = Location(title,desc)
    locations[title] = e

directions = [["N", "Deck", "Salon"],
              ["E", "Deck", "Cargo"],
              ["W", "Deck", "Bridge"],
              ["W", "Salon", "Corridor"],
              ["N", "Salon", "Library"],
              ["E", "Salon", "Smoking Room"],
              ["S", "Corridor", "Women's Quarters"],
              ["W", "Corridor", "VIP Quarters"],
              ["N", "Corridor", "Writer's Cabin"],
              ["N", "Bridge", "Infirmary"],
              ["S", "Bridge", "Cargo"]]


for [l_dir, loc1, loc2] in directions:

    if l_dir == "N":
        locations[loc1].north(loc2)
        locations[loc2].south(loc1)
    elif l_dir == "S":
        locations[loc1].south(loc2)
        locations[loc2].north(loc1)
    elif l_dir == "W":
        locations[loc1].west(loc2)
        locations[loc2].east(loc1)
    else:
        locations[loc1].east(loc2)
        locations[loc2].west(loc1)

###{ "Game Status", [[site1, lingertime],[site2, lingertime],...}

listofnpc = [
             ["General", "Deck",
              ["1", [["Deck", 0.1],
                     ["Salon", 0.2],
                     ["Corridor", 0.1],
                     ["Library", 0.1],
                     ["VIP Quarters", 0.3],
                     ["Smoking Room", 0.2]]]],
             ["Writer", "Deck",
              ["1", [["Deck", 0.1],
                     ["Salon", 0.2],
                     ["Corridor", 0.1],
                     ["Library", 0.2],
                     ["Writer's Cabin", 0.3],
                     ["Smoking Room", 0.1]]]],
            ["Doctor", "Deck",
              ["1", [["Deck", 0.1],
                     ["Salon", 0.2],
                     ["Corridor", 0.1],
                     ["Infirmary", 0.2],
                     ["VIP Quarters", 0.3],
                     ["Smoking Room", 0.1]]]],
             ["Captain", "Bridge",
              ["1", [["Deck", 0.1],
                     ["Salon", 0.1],
                     ["Corridor", 0.1],
                     ["VIP Quarters", 0.1],
                     ["Cargo", 0.1],
                     ["Bridge", 0.5]]]],
            ["First Mate", "Bridge",
              ["1", [["Deck", 0.2],
                     ["Salon", 0.1],
                     ["Corridor", 0.1],
                     ["Cargo", 0.1],
                     ["Bridge", 0.5]]]],
            ["Young Woman", "Corridor",
              ["1", [["Deck", 0.1],
                     ["Salon", 0.2],
                     ["Corridor", 0.1],
                     ["Library", 0.2],
                     ["Infirmary", 0.1],
                     ["Women's Quarters", 0.3]]]],
            ["Oriental Woman", "Corridor",
              ["1", [["Deck", 0.1],
                     ["Salon", 0.2],
                     ["Corridor", 0.1],
                     ["Library", 0.2],
                     ["Infirmary", 0.1],
                     ["Women's Quarters", 0.3]]]]
]

npc = []
for i in listofnpc:
    [name, start_location, [state, possibilities]] = i
    new_one = NPC(name)

    for [site, prob] in possibilities:
        new_one.roaming_pattern(state, site, prob)
    new_one.set_location(start_location)

    npc.append(new_one)
    del new_one


def textbox( a, b, text):
    print(term.home + term.white_on_green)
    x, y = a
    w, h = b

    box = " "*w
    text = " ".join(text.split()) # remove whitespaces

    lines = 0
    while len(text)>0:
        print(term.move_xy(x, y) + box)

        lane = text[:w].split(" ")
        text = lane[-1]+text[w:]

        if len(text)<w:
            line = " ".join(lane[:-1])+" "+text
            if len(line)<w:
                print(term.move_xy(x, y) + line)
            else:
                print(term.move_xy(x, y ) + " ".join(lane[:-1]))
                print(term.move_xy(x, y + 1) + text)

            break
        else:
            print(term.move_xy(x, y) + " ".join(lane[:-1]) )
        y += 1
        lines += 1

def reply( text ):
    textbox((18,18),(40,2),text)
    term.inkey()


def show_screen(this_loc):
    global npc

    print(term.home + term.white_on_blue + term.clear)

    # Action Menu
    print(term.move_xy(10, 2)+"⮝")
    print(term.move_xy(10, 3) + "8")
    print(term.move_xy(6, 4) + "⮜ 4   6 ⮞")
    print(term.move_xy(10, 5) + "9")
    print(term.move_xy(10, 6) + "⮟")

    print(term.move_xy(5, 8) + "G:Give")
    print(term.move_xy(5, 9) + "O:Open")
    print(term.move_xy(5, 10) + "C:Close")
    print(term.move_xy(5, 11) + "P:Pickup")
    print(term.move_xy(5, 12) + "L:LookAt")
    print(term.move_xy(5, 13) + "T:TalkTo")
    print(term.move_xy(5, 14) + "U:Use")
    print(term.move_xy(5, 15) + "]:Push")
    print(term.move_xy(5, 16) + "[:Pull")

    # Location Title, Description and Exits
    print(term.move_xy(20, 2) + this_loc.title)
    textbox((18, 5), (60, 10), this_loc.description)
    textbox((18, 16), (40, 5), this_loc.exits())

    # Show who is here
    who_is_here = []
    for _npc in npc:
        if _npc.location == this_loc.title:
            who_is_here.append(_npc.name)

    if len(who_is_here) > 0:
        if len(who_is_here) == 1:
            out = "You see the " + who_is_here[0] + "."
            print(term.move_xy(20, 14) + out)
        else:
            out = "You see the " + " the ,".join(who_is_here[:-1]) + " and the " + who_is_here[-1] + "."
            print(term.move_xy(20, 14) + out)

    print(term.move_xy(1, 20) )


current_loc = "Deck"
to_quit = False
keypress = ""
game_state = "1"

with term.raw(), term.hidden_cursor():
    while keypress.upper() != "Q":
        show_screen(locations[current_loc])

        keypress = term.inkey(timeout=1).upper()

        if keypress in ["Q", "8", "4", "6", "2", "G", "O", "C", "P", "L", "T","U","]","["]:

            if keypress in ["8", "4", "6", "2"]:
                if keypress == "8":
                    newloc = locations[current_loc].go_north
                if keypress == "4":
                    newloc = locations[current_loc].go_west
                if keypress == "6":
                    newloc = locations[current_loc].go_east
                if keypress == "2":
                    newloc = locations[current_loc].go_south

                if newloc is None:
                    reply("You cannot go there.")
                else:
                    current_loc = newloc
        else:
            for _npc in npc:
                _npc.random_move(game_state)



