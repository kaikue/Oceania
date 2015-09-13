Oceania
==
A procedurally generated 2D sandbox game set underwater.
Written in Pygame and uses JSON and pickle.
Created by Kai Kuehner, 2013.

TODO
--
 - Button does not function correctly when run from Game.py
     - problem with global variables- make designated launcher class
 - Structures can only be in one chunk (and overwrite each other all the time)
 - Check for entity collisions in nearby chunks (all loaded?)
	 - Pick up items across chunk border
 - Pause game when opening GUIs
 - Shorten reach if cursor close
 - Flip rendering in inventory (across then down)

NEEDED FEATURES
--
 - World generation
     - Caves
         - Lava tubes
		 - Air pockets?
	 - Hydrothermal vents
     - Spawn midpoint displacement
     - Biomes
         - Ores
         - More structures
             - Improve temple
             - Volcanic pipe- kimberlite, diamond
 - GUI work
	 - Inventory
 - Entities
     - Enemies, friendlies
 - Player
     - Inventory
 - Crafting
     - Skill based weapon stats? (trace outline, accuracy determines stats)
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
 - Ore processing https://i.imgur.com/jYvaxQ1.jpg
 - Energy
	- http://iopscience.iop.org/0964-1726/23/8/085023
	- http://ieeexplore.ieee.org/xpl/articleDetails.jsp?reload=true&arnumber=6220721
 - Titans
	 - drop automation materials
 - Water suit + island
 - DEEPEST LORE