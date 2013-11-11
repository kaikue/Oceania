Oceania
==
A procedurally generated 2D sandbox game set underwater.
Written in Pygame and uses JSON and pickle.
Created by Kai Kuehner, 2013.

BUGS
--
 - Pickling is slow- multithread?
 - Eclipse doesn't believe in function-defined global variables- make these objects or something?
 - Draw water under transparent blocks
     - check if transparent, somehow?
     - do this at image load

NEEDED FEATURES
--
 - World generation
     - Better terrain
     - Caves
         - Lava tubes
     - Spawn midpoint displacement
     - Structures (over multiple chunks)
         - Temple
         - Volcanic pipe- kimberlite, diamond
     - Biomes
 - Entities
     - Enemies, friendlies
     - Dropped blocks
 - Player
     - Inventory
 - Crafting
 - Menus
     - Get input from user to name world
 - Combat
 - Move player coordinate to center
 - Sound
 - Block placement & destruction
     - Make block breaking take time
     - Drop block item
     - Shorten raycast to nearest block
     - Center target image
     - Make target only show when pointing at block within range???
         - could remove target entirely, highlight selected block/space?