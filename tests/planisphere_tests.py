from nose.tools import *
from ex47.game import Room
from gothonweb.planisphere import *

def test_room():
    gold = Room("GoldRoom", # Initiates Room, passing name and desc params.
                """This room has gold in it you can grab. There's a 
                door to the north.""")
    assert_equal(gold.name, "GoldRoom") # tests that gold.name is called "GoldRoom"
    assert_equal(gold.paths, {}) # tests that gold.paths is an empty dict

def test_room_paths():
    center = Room("Center", "Test room in the center.") # Creates instance of Room
    north = Room("North", "Test room in the north.")
    south = Room("South", "Test room in the south.")

    center.add_paths({'north': north, 'south': south}) # Updates self.paths in center with dict
    assert_equal(center.go('north'), north) # Checks that center.go returns variable north when dict key north is used.
    assert_equal(center.go('south'), south) # Checks that center.go returns variable south when dict key south is used. 

def test_map():
    start = Room("Start", "You can go west and down a hole.") # # initiates Room, passing name and desc params
    west = Room("Trees", "There are trees here, you can go east.")
    down = Room("Dungeon", "It's dark down here, you can go up.")

    start.add_paths({'west': west, 'down': down}) # Updates self.paths in start with keys and values
    west.add_paths({'east': start})
    down.add_paths({'up': start})

    assert_equal(start.go('west'), west) # Checks that start.go returns variable west when dict key west is used
    assert_equal(start.go('west').go('east'), start) # Checks that .go west, followed by .go east is equal to start
    assert_equal(start.go('down').go('up'), start) # Checks that .go down, dollowed by .go up is eual to start

def test_gothon_game_map():
    start_room = load_room(START) # block tests what is returned if selecting shoot/dodge in CC 
    assert_equal(start_room.go('shoot!'), shoot_death)
    assert_equal(start_room.go('dodge'), dodge_death)
    room = start_room.go('tell a joke')
    assert_equal(room, laser_weapon_armory)
    
    current_room = load_room('laser_weapon_armory')
    assert_equal(current_room.go('0132'), the_bridge)
    assert_equal(current_room.go('*'), catch_all_death)
    room = current_room.go('0132')
    assert_equal(room, the_bridge)


    current_room = load_room('the_bridge')
    assert_equal(current_room.go('slowly place the bomb'), escape_pod)
    assert_equal(current_room.go('throw the bomb'), throw_bomb_death)
    room = current_room.go('slowly place the bomb')
    assert_equal(room, escape_pod)

    current_room = load_room('escape_pod')
    assert_equal(current_room.go('2'), the_end_winner)
    assert_equal(current_room.go('*'), the_end_loser)
    room = current_room.go('2')
    assert_equal(room, the_end_winner)

