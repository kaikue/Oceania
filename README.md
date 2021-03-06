Oceania
==
A procedurally generated 2D sandbox game set underwater.
Written in Pygame.
Created by Kai Kuehner, 2013-2018.
![Screenshot](http://i.imgur.com/wUVoCkr.png)

TODO
--
- Port to Monogame
    - just try rendering 2 layers of tiles
- Worldgen
    - Biomes
        - Choose biome based on chunk
            - Multiple 1d Perlin noise functions
                - Since using just 1 will cause biomes to always be sandwiched between same partners
                - Temperature, liveliness?
            - Each biome has temp, life in JSON
            - Generate Voronoi diagram from biome placements (render this for debug)
            - When generating world, get x and y into biome diagram from a pair of 1d Perlin noise functions on world x
            - Get nearest two biomes- if almost halfway between them, lerp between them to get mixed biome
        - prescriptive (base height on biome)
            - Terrain scale
            - Surface material cutoffs
            - Gradients (done)
	    - Smooth transitions between biomes
            - vertically- heights
            - horizontally- mix blocks together?
            - transition minibiomes?
    - Decorations
        - seeded random(x) is within some range
        - Allow for multi-chunk structures
            - check if adjacent chunk would have a structure
    - Ores, etc.
        - 2d Perlin noise
    - What is at the center (bottom) of the world?
        - hot impassible water?
        - solid rock?
        - lava?
    - Vertical chunks
    - Multithreading
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
        - crop to CTM- pipes are really noticeable
    - Dark colored borders
- Favorite items so they don't get mass-transferred (or dropped?)
- Player:44 throws exception when collecting dropped itemstack? (dropping itemstack in wrong chunk?)
- Click outside of inventory or press R to drop item in world
- Sliding puzzle lock
    - 3x3 version
    - test solution checking
- Pipes
    - Transfer items- how?
    - CTM variations: solid, sametype
- Move basic item attributes (attack damage, break speed, harvest level) to JSON with defaults
- Move JSON parsing to separate module, it doesn't belong in World
- Structures with background- define characters to be pairs of foreground and background blocks
- Enemies drop healing hearts when killed
- When player is hurt, make the whole player image flash red
- Menus
    - Better text fields
        - show cursor
        - tab to go to next one
        - filter invalid keypresses (is this done already?)
        - arrow keys, shift, home/end, mouse click, etc. to change cursor
    - Scroll wheel scrolls world list
    - Validate name in world creation
    - More options
        - Key bindings
    - Delete world button (& confirm dialog)
- Player can spawn inside generated structure and get stuck
- CTM rendering is slow- figure out some solution for large contiguous masses
    - only update image when adjacent block changes?
- Keybinding (first in config, then in game menu)
    - Controller support
- DamageSourceStab and spear- hitbox around tip of spear
- Add reach attribute to items (just weapons)
- Render rotating attacks
    - arm- blit separate arm part onto item image? and don't render arm
    - Offset attack when swimming?
- Player jumps between swimming and stopped images while slowing down while hitting a block
- Scroll wheel click to pull out targeted block from inventory (or scroll to it if in hotbar)
- Bounding box issues
    - Just make player bounding box a constant small square in the middle
    - Moving right on the ground keeps standing anim
    - Player's head can clip into blocks on bottom or right corners
    - Keep swimming animation while key is held down (so player can slide into 1 block hole)?
    - Left and right animations for swimming up and down
- Press (or hold?) CTRL to switch to raycast-closest-hit mode (for mining a tunnel)
- Unpickling messes up inter-object references
    - DamageSourceSweep item and parent
- Clamp to grid issues
    - Player doesn't naturally align to grid against a horizontal block collision (can bump into block by holding down key)
    - Player can clip up/down into blocks
- Icon should load with main menu, not World
- Pixel scale
    - Add pixel scale to options menu
        - any problems when changing dynamically?
    - Make world load menu background work with any scale
    - Performance is awful with scale = 1
- CTM slowness
    - only change block image when updating adjacent in 8 sides?
    - also auto-generate CTM images from center, corners, edges, inside corners
- Cache large rendering chunks of world (whole vertical chunk?)

NEEDED FEATURES
--
- World generation
    - Caves
        - Lava tubes
        - Air pockets?
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
        - Hydrothermal vents
        - Treasures
            - bunch of building blocks
            - tool improvement items
            - anything that will prompt further gameplay
            - button to blow up structure
            - max health increasers
        - Backgrounds in structures- hidden secrets behind some tiles
        - Dungeons
            - Sliding puzzle lock
            - Monster chases you around hallways
            - 4 branches
            - Fire/demonic themed
            - Kelp forest themed- grow stuff
            - Maze
            - Creature's nest (crabs?)
            - Light/color
            - Should all have a reason to exist in world
            - Procedurally generate layout?
    - More stuff in the empty water- enemies, ???
    - Vertical chunks? caves could be extended indefinitely
- Entities
    - Enemies
        - Load from JSON
        - Spawn where no background (or specific based on background)
        - Item drops
        - Attacks
        - More pathfinding options
        - Fun AI
            - Sometimes attack each other
        - Mirror- steals your attack (can be abused with healing)
        - Mimic
        - Giant sunfish
    - Bosses
        - In structures and elsewhere
        - Drop weapons/armor based on abilities
        - Danmaku
        - Puzzle
    - Friendlies?
- Player animation- attack, transitions?
- Crafting
    - Larger crafting tables- 2x2 (from some item in world), 3x3, 4x4, 5x5, 9x9
    - Slot for crafting tool- hammer for metal work, etc.
    - Generate blockentity when crafting chests etc.
    - or possibly all in world?
- Ore processing
    - http://scholar.chem.nyu.edu/tekpages/Subjects.html
    - https://en.wikipedia.org/wiki/Roman_economy#Mining_and_metallurgy
    - https://i.imgur.com/jYvaxQ1.jpg
- Fruit farming and cooking
    - Life plants to make healing easier
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
- Biome backgrounds
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
- Minimap
- Keybindings
    - Defaults, can reset to them
    - Every option must have a keybinding
    - Left click, right click, scroll wheel up/down/click
    - Movement WASD/arrow keys
    - Background lshift/rshift
    - Hotbar first through tenth slots
- Allow player to change scale
    - test different scale values
- Item that extends attack reach and/or break distance
- WAILA
- Mod support (additional classes & jsons in mod folder)
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
    - Shells, eggshells, coral -heat-> quicklime + sand -> limestone
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