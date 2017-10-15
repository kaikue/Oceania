Oceania
==
A procedurally generated 2D sandbox game set underwater.
Written in Pygame.
Created by Kai Kuehner, 2013-2017.
![Screenshot](http://i.imgur.com/wUVoCkr.png)

TODO
--
- All TODOs in code
- Structures can only be in one chunk (and overwrite each other all the time)
	- also messes up entity generation
	- structures across multiple chunks with perlin noise?
- Block breaking particles
- Block preview visualization is a bit off- probably due to use of outline
- Possibly render foreground water as semitransparent (so it goes over block breaking image)
- Make sharpened flint more effective on kelp
- Chests
    - remove * rendering (after entity generation is fixed)
- Inventory
    - Armor
- Texture improvements:
	- Font
	- Basalt
	- Game icon
		- also make this load during startup, not world creation
	- Block breaking animation
		- crop to CTM
	- Dark colored borders
- Mod support (additional classes & jsons in mod folder)
- Make image loading only happen once ever (for itemdrops especially)
	- Don't render giant blocks in player's hand- use BlockDrop versions
- Favorite items so they don't get mass-transferred (or dropped?)
- WAILA
- Player:44 throws exception when collecting dropped itemstack? (dropping itemstack in wrong chunk?)
- Click outside of inventory or press R to drop item in world
- Sliding puzzle lock
	- 3x3 version
	- test solution checking
- Raycast block breaking and mine closest one instead
- Pipes
	- Transfer items- how?
	- CTM variations: solid, sametype
- Move basic item attributes (attack damage, break speed, harvest level) to JSON with defaults
- Move JSON parsing to separate module, it doesn't belong in World
- Structures with background- define characters to be pairs of foreground and background blocks
- Fix acceleration being preserved if releasing left and pressing right at the same time
- Properly show held item if facing right, swimming, etc.
- Enemies drop healing hearts
- When player is hurt, make the whole player image flash red
- Menus
	- Better text fields
	- Scroll wheel scrolls world list
    - Validate name in world creation
    - More options
    - Quit to main menu in pause menu
- Player can spawn inside generated structure and get stuck
- CTM rendering is slow- figure out some solution for large contiguous masses
- Keybinding (first in config, then in game menu)

NEEDED FEATURES
--
- World generation
    - Caves
    	- Perlin Worms
        - Lava tubes
        - Air pockets?
    - Hydrothermal vents
    - Redo worldgen to be Perlin noise based
		- AccidentalNoiseLib- https://stackoverflow.com/questions/145270/calling-c-c-from-python
    - Biomes
    	- Island
    	- Beach
    	- Rocky shore
    	- Mangrove forest
    	- Seagrass bed
    	- Kelp forest
    	- Choral reef
    	- Ice edge
        - Neritic zone
        - Seamounts- cobalt crusts
    	- Mid-ocean ridge
    - Rock types
        - Basalt
        - Chalk (makes quicklime in lime kiln- limelight)
        - Gabbro
    - Ores
    	- see spreadsheet
    - More structures
        - Improve temple
        - Volcanic pipe- kimberlite, diamond
        - Treasures
            - bunch of building blocks
            - tool improvement items
            - anything that will prompt further gameplay
            - button to blow up structure
            - max health increasers
        - Backgrounds in structures- hidden secrets behind some tiles
		- Sliding puzzle lock
- GUI work
    - Inventory
- Entities
    - Enemies
    	- Load from JSON
    	- Spawn where no background
    	- Item drops
    	- Attacks
    	- More pathfinding options
    - Bosses
	    - Drop weapons/armor based on abilities
	- Friendlies?
- Player animation- attack, transitions?
- Crafting
    - Larger crafting tables- 2x2 (from some item in world), 3x3, 4x4, 5x5, 9x9
    - Slot for crafting tool- hammer for metal work, etc.
    - Generate blockentity when crafting chests etc.
    - or possibly all in world?
- Ore processing
    - https://i.imgur.com/jYvaxQ1.jpg
- Fruit farming and cooking
- Combat
    - Armor
    - Weapons
    	- Different attack types
    		- spears jab, swords sweep
    	- Right click for special move
    		- spears throw, swords full sweep, picks place block
- Sound
    - freesound.org
    - Button press- stone sliding/click
    - Player hurt- female grunt (underwater?)
    - Player swim- underwater swoosh
    - Dig
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
- Fish breeding
- Water suit + island
    - Reverse Atmospheric Diving Suit (Vitallum)
    - https://i.imgur.com/jgcLPXi.jpg
	- Indonesia, Vietnam, New Zealand
- DEEPEST LORE

Progression:
--
- T0: Stone Age
    - Spawn in world
    - Pick up flint
    - Right click flint with it several times to make Sharpened Flint
    - Right click Sharpened Flint on bone (from killing something or skeleton in world) to make basic pick
- T1: Copper Age
    - Collect copper ore
    - Cold forging- heat? then hit with hammer? to make pick head or sword blade
    - Copper tools, armor
- T2: Bronze Age
	- Collect tin, lead, zinc ore
    - Crucible
			- Place crucible over hydrothermal vent, place ore into crucible, inject into mold for whatever part (like sword blade)
			- Up to 800°, melt metals in forge, basic alloys, cast into molds
        - Craft molds with sand + clay, imprint with some natural material for type (e.g. narwhal horn for sword blade)
        - Melt sand into glass, pour into empty mold
    - Alloys- brass, bronze
    - Machines
    - Alchemy?
- T3: Iron Age
	- Collect iron ore
	- Bloomery?
	- Steel
	- Mangalloy
    - Alchemy?
- T4: Final Age
	- Collect cobalt, chromium
	- Make vitallum
	- Make Reverse Atmospheric Diving Suit