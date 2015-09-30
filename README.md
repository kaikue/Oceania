Oceania
==
A procedurally generated 2D sandbox game set underwater.
Written in Pygame.
Created by Kai Kuehner, 2013-2015.

TODO
--
- Button does not function correctly when run from Game.py
    - problem with global variables- make designated launcher class
- Structures can only be in one chunk (and overwrite each other all the time)
- Check for entity collisions in nearby chunks (all loaded?)
    - Pick up items across chunk border
- Pause game when opening GUIs
    - Pause game at all
- Figure out why spawn chunks don't save
- Block rendering
    - Redo according to Kenney's triangle system? or full CTM
    - Mask with solid magenta triangle(s), then set that as transparent
- Fix connected texture block drops rendering the whole image (just pick the center one) as well as in inventory
- Background tiles
    - Hold shift to interact with background
    - tiles are darkened and overlaid with water image
    - Can only place/break background tiles if there is no foreground tile there- otherwise shift interact does nothing
    - Backgrounds in structures- hidden secrets behind some tiles

NEEDED FEATURES
--
- World generation
    - Caves
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
- GUI work
    - Inventory
- Entities
    - Enemies, friendlies
- Player
    - Animation
- Crafting
    - Larger crafting tables- 2x2 (from some item in world), 3x3, 4x4, 5x5, 9x9
    - Slot for crafting tool- hammer for metal work, etc.
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
- Sound
    - freesound.org
- Block placement & destruction
    - Make block breaking take time
    - Make target only show when pointing at block within range???
        - could remove target entirely, highlight selected block/space?
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
- Water suit + island
    - Reverse Atmospheric Diving Suit (Vitallum)
    - https://i.imgur.com/jgcLPXi.jpg
- DEEPEST LORE

- Progression:
    - Spawn in world
    - Dig dirt, pick up flint