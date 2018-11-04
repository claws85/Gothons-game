from random import randint

class Room(object):

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.paths = {}
    
    def go(self, direction):
        return self.paths.get(direction, None)  # 2. Retrieves direction from self.paths
    
    def add_paths(self, paths):
        self.paths.update(paths) # 1. updates self.paths with info provided to the function as a param

central_corridor = Room("Central Corridor",
"""
The Gothons have invaded your ship. You are the only survivor.
Your last mission is to get a bomb from the Weapons Armory and 
put it in the bridge, then blow up the ship before getting into an
escape pod.
        
You are running down the central corridor to the Weapons Armory when a
Gothon jumps out. He's blocking the door to the Armory and about to pull
out a weapon.

What do you do?
""")

central_corridor.success = (
"""
Lucky for you they made you learn Gothon insults in the academy. You
tell the Gothon a joke. He stops and doubles over in laughter. You
take your chance to shoot him in the head, and jump through to the
Laser Weapon Armory room.
""")

central_corridor.help = (
"""
The Gothon is in front of you. Think about the different actions you
could take to ensure your survival. Here are some suggestions - I 
can't guarantee these will work. 

You have a blaster - you could take a shot at it and see if you could 
kill it before it shoots you.

Or you could attempt to dodge the shot it is about to take, and see
happens...

Alternatively... Gothons are renowned for having a sense of humour...
you could tell a joke...
""")

shoot_death = Room("death", 
"""
Quick on the draw you fire your blaster at the Gothon. His costume
is flowing around his body, which thows off your aim. Your laser
hits his costume and misses his. Enraged, he blasts you in the face.
He then eats you.
""")

dodge_death = Room("death",
"""
Like a world-class boxer you dodge as the Gothon's blaster cranks
a laser past your head. As you dodge, your foot slips and you bang
your head on the metal wall and pass out. The Gothon eats you.
""")

laser_weapon_armory = Room("Laser Weapon Armory",
"""
You do a dive roll into the Weapons Armory, crouch and scan the room for 
more Gothons that might be hiding. It's dead quiet, too quiet. You stand 
up and run to the far side of the room and find the bomb.
If you get the code wrong 10 times then the lock closes forever and you
can't get the bomb. The code has 4 digits.

Try entering a four-digit numeric code...
""")

laser_weapon_armory.success = (
"""
The container clicks open and the seal breaks, letting gas out.
You can grab the bomb and run as fast as you can to the bridge.
""")

laser_weapon_armory.help = (
"""
That code is tricky. If you're really stuck, enter the word 'cheat'
and the code armory door should unlock. Cheater!
""")

catch_all_death = Room("death", 
"""
The lock buzzes one last time and you hear a melting sound as the
mechanism is fused together. You decide to sit there, and finally the 
Gothons blow up the ship after leaving for theirs, and you die.
""")

too_many_attempts_death = Room("Too many attempts!",
"""
The lock buzzes one last time and you hear a melting sound as the
mechanism is fused together. You decide to sit there, and finally the 
Gothons blow up the ship after leaving for theirs, and you die.
""")


the_bridge = Room("The Bridge",
"""
You burst onto the Bridge with the neutron destruct bomb under 
your arm and suprise 5 Gothons who are trying to take control
of the ship. They do not pull out their weapons, as they see
the bomb and do not want to set it off.
""")

the_bridge.success = (
"""
You point your blaster at the bomb under your arm, and the Gothons
start to sweat. You inch backwards towards the door, open it,
and then carefully place the bomb on the floor.  You then jump back
 through the door, punch the close button and blast the lock so the 
Gothons can't get out. Now the bomb is placed you run to the escape 
bod, so you can get off this tin can.
""")

the_bridge.help = (
"""
You're carrying a very powerful explosive device in your hands. Don't 
do anything rash with it. You could place the bomb down carefully on the
Bridge floor. The Gothons will try and defuse it - but they might not
be able to do so...
""")

throw_bomb_death = Room("death", 
"""
In a panic you throw a bomb at a group of Gothons and make a leap 
for the door. Right as you drop it, a Gothon shoots you in the back, 
killing you. Regardless of whether the Gothons can defuse the device, 
you're dead. 
""")

escape_pod = Room("Escape Pod",
"""
You rush through the ship desperately trying to make it to the escape pod, 
before the ship explodes. It seems like hardly any Gothons are on the ship,
so your run is free from interference. You get to the chamber with the escape
pods and now need to pick one to take. Some of them could be damaged, but 
don't have time to look. There's five pods. Which one do you take?
""")

the_end_winner = Room("The End",
"""
You jump into pod 2 and hit the eject button. The pod slides 
out into space, heading to the planet below. As it descends, you 
look back and see your ship implode, then explode like a bright
star, taking out the Gothon ship at the same time.
""")

escape_pod.help = (
"""
Make a choice between the five escape pods available. 

Select a pod by entering a number from one to five. If you're lucky it will
detatch from the ship correctly and you'll get to one of the planets below.
""")

the_end_loser = Room("Squish !!!",
"""
You jump into a random pod and hit the eject button. The pod escapes into the 
void of space, then implodes as the hull ruptures, crushing your body into 
jam jelly.
""")

escape_pod.add_paths({
    '2': the_end_winner,
    '1': the_end_loser,
    '3': the_end_loser,
    '4': the_end_loser,
    '5': the_end_loser
})

generic_death = Room("death", "You died.")

the_bridge.add_paths({
    'throw the bomb': throw_bomb_death,
    'slowly place the bomb': escape_pod
})

code = f"{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}"

laser_weapon_armory.add_paths({
    code: the_bridge,
    'cheat': the_bridge
})
print(laser_weapon_armory.paths)

central_corridor.add_paths({
    'shoot!': shoot_death,
    'dodge': dodge_death,
    'tell a joke': laser_weapon_armory
})

START = 'central_corridor'

def load_room(name):
# To do: switch global variables to class variables.
    return globals().get(name)

def name_room(room):
# To do: switch global variables to class variables.

    for key, value in globals().items():
        if value == room:
            return key


#print(load_room(START))

#print(name_room(START))

#x = globals()
#print(globals().get('central_corridor'))
#print(x)
