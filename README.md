Oceania
==
A procedurally generated 2D sandbox game set underwater.
Written in Pygame.
Created by Kai Kuehner, 2013-2017.
![Screenshot](http://i.imgur.com/yOTYumw.png)

TODO
--
- All TODOs in code
- Button does not function correctly when run from Game.py
    - problem with global variables- make designated launcher class
- Structures can only be in one chunk (and overwrite each other all the time)
	- also messes up entity generation
	- structures across multiple chunks with perlin noise?
- Pause screen (can just be a GUI)
- Finish magic staff
- Player animation
- Block breaking particles
- Block preview visualization is a bit off- probably due to use of outline
- Possibly render foreground water as semitransparent (so it goes over block breaking image)
- Make sharpened flint more effective on kelp
- Chests
    - remove * rendering (after entity generation is fixed)
    - Stack with same data, or not at all
- Inventory
    - Armor
- Texture improvements:
	- Font
	- Basalt
	- Game icon
	- Block breaking animation
		- crop to CTM
	- Dark colored borders
- Mod support (additional classes & jsons in mod folder)
- Make image loading only happen once ever (for itemdrops especially)
	- Don't render giant blocks in player's hand- use BlockDrop versions
- Shift click on inventory transfer buttons to smart transfer?
- WAILA
- Player:44 throws exception when collecting dropped itemstack? (dropping itemstack in wrong chunk?)
- Esc to pause or close GUI
- Sliding puzzle lock
	- 3x3 version
	- test solution checking
- Raycast block breaking and mine closest one instead
- Pipes
	- Transfer items- how?
	- CTM variations: solid, sametype
- Move basic item attributes (attack damage, break speed, harvest level) to JSON with defaults
- Move JSON parsing to separate module, it doesn't belong in World

NEEDED FEATURES
--
- World generation
    - Caves
    	- Perlin Worms
        - Lava tubes
        - Air pockets?
    - Hydrothermal vents
    - Spawn midpoint displacement
    - Biomes
    - Rock types
        - Basalt
        - Chalk (makes quicklime in lime kiln- limelight)
        - Gabbro
    - Ores
        - Manganese nodules-  manganese (27-30%), iron (6%), nickel (1.4%), copper (1-1.3%), cobalt (0.25%)
        - Chromite (chromium- used for Vitallum, steel, tanned leather)
        - Cobalt (used for Vitallum, steel drill, )
            - Cobalt crusts- cobalt, manganese, iron layer on seamounts
    - More structures
        - Improve temple
        - Volcanic pipe- kimberlite, diamond
        - Treasures- "starter packs" of blocks, tool improvement items, anything that will prompt further gameplay
        - Backgrounds in structures- hidden secrets behind some tiles
		- Sliding puzzle lock
- GUI work
    - Inventory
- Entities
    - Enemies, friendlies
- Player
    - Animation
    - Customization- name, colors, hair
- Crafting
    - Larger crafting tables- 2x2 (from some item in world), 3x3, 4x4, 5x5, 9x9
    - Slot for crafting tool- hammer for metal work, etc.
    - Generate blockentity when crafting chests etc.
- Ore processing
    - https://i.imgur.com/jYvaxQ1.jpg
    - T0: Flint
    - T1: Cold forging- shape metal into basic tools with a stone hammer (copper)
    - T2: Hot forging- up to 750°, melt metals in forge, basic alloys, cast into molds (tin, lead, zinc, brass, bronze)
        - Craft molds with sand + clay, imprint with some natural material for type (e.g. narwhal horn for sword blade)
        - Melt sand into glass, pour into empty mold
    - T3: Iron, steel, mangalloy
    - T4: advanced alloys
    - Place crucible over hydrothermal vent, place ore into crucible, inject into mold for whatever part (like sword blade)
- Menus
    - Get input from user to name world
    - Pause, save & quit, options
- Combat
    - Armor
    - Weapons
    	- Different attack types
    		- spears jab, swords sweep
    	- Right click for special move
    		- spears throw, swords full sweep, picks place block
- Sound
    - freesound.org
- Multiblocks- have special multiblock interface that checks specific blocks
    - Hammer cycles through block variations
- Lighting
  - decreases with greater depth
    - set brightness per tile? use circlecollector style gradient hacks?
- Energy
    - http://iopscience.iop.org/0964-1726/23/8/085023
    - http://ieeexplore.ieee.org/xpl/articleDetails.jsp?reload=true&arnumber=6220721
- Titans
    - drop automation materials
- Automation
    - ore processing
    - crafting
- Spellcasting
	- Shoot bolt of energy from wand
	- Basic elements
		- Heat- large wave instead of projectile
		- Earth- pass through enemies to attack others behind
		- Electric- sends bolt of lightning between nearby enemies on hit
	- Combine spell components to modify bolt
		- Splitting (bolt splits into 4 after a bit)
		- Homing
		- Orbit (revolves around player)
- Waves
- Way to get any random item (like instability orbs)
- Water suit + island
    - Reverse Atmospheric Diving Suit (Vitallum)
    - https://i.imgur.com/jgcLPXi.jpg
- DEEPEST LORE

Progression:

    - Spawn in world
    - Dig dirt, pick up flint (does this drop from dirt or spawn separately?)
    - Right click flint with it several times to make Sharpened Flint
    - Right click Sharpened Flint on bone (from killing something or skeleton in world) to make basic pick
    - Collect ?
    - Cold forging (copper)
    - Crucible
    