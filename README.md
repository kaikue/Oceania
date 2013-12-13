Oceania
==
A procedurally generated 2D sandbox game set underwater.
Written in Pygame and uses JSON and pickle.
Created by Kai Kuehner, 2013.

BUGS
--
 - Pickling is slow- multithread?

NEEDED FEATURES
--
 - World generation
     - Caves
         - Lava tubes
     - Spawn midpoint displacement
     - Biomes
         - Ores
         - Structures (over multiple chunks)
             - Temple
             - Volcanic pipe- kimberlite, diamond
 - Entities
     - Enemies, friendlies
 - Player
     - Inventory
 - Crafting
 - Menus
     - Get input from user to name world
 - Combat
 - Move player coordinate to center of image
 - Sound
 - Block placement & destruction
     - Make block breaking take time
     - Shorten raycast to nearest block
     - Center target image
     - Make target only show when pointing at block within range???
         - could remove target entirely, highlight selected block/space?