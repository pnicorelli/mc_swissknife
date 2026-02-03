# --- Market Arcade: East Side (Heavy Industry) ---

# 0. Clear everything from the ground up to 10 blocks high and make the floor
fill ~-7 ~0 ~-7 ~7 ~10 ~-21 air
fill ~-7 ~-1 ~-7 ~7 ~-1 ~-21 chiseled_quartz_block

# 1. Build the Stone Walls/Divisions
fill ~6 ~0 ~-9 ~6 ~2 ~-17 quartz_bricks
# Create 3-block wide stalls with dividers
fill ~4 ~0 ~-9 ~6 ~2 ~-9 quartz_bricks
fill ~4 ~0 ~-13 ~6 ~2 ~-13 quartz_bricks
fill ~4 ~0 ~-17 ~6 ~2 ~-17 quartz_bricks

# 2. Add Workstations (Placed into the walls)
setblock ~5 ~0 ~-10 stonecutter[facing=west]
setblock ~5 ~0 ~-12 smithing_table
setblock ~5 ~0 ~-14 blast_furnace[facing=west]
setblock ~5 ~0 ~-16 grindstone[face=floor]

# 3. Add the Countertops
fill ~4 ~2 ~-10 ~4 ~2 ~-12 smooth_quartz_slab[type=top]
fill ~4 ~2 ~-14 ~4 ~2 ~-16 smooth_quartz_slab[type=top]

# 4. Colorful Awnings (Yellow and Orange)
fill ~4 ~3 ~-9 ~6 ~3 ~-17 yellow_stained_glass
fill ~4 ~3 ~-10 ~4 ~3 ~-12 orange_wool
fill ~4 ~3 ~-14 ~4 ~3 ~-16 orange_wool

# --- Market Arcade: West Side (Crafts & Knowledge) ---

# 1. Build the Walls
fill ~-6 ~0 ~-9 ~-6 ~2 ~-17 quartz_bricks
fill ~-4 ~0 ~-9 ~-6 ~2 ~-9 quartz_bricks
fill ~-4 ~0 ~-13 ~-6 ~2 ~-13 quartz_bricks
fill ~-4 ~0 ~-17 ~-6 ~2 ~-17 quartz_bricks

# 2. Add Workstations
setblock ~-5 ~0 ~-10 lectern[facing=east]
setblock ~-5 ~0 ~-12 fletching_table
setblock ~-5 ~0 ~-14 cartography_table
setblock ~-5 ~0 ~-16 brewing_stand

# 3. Add the Countertops
fill ~-4 ~2 ~-10 ~-4 ~2 ~-12 smooth_quartz_slab[type=top]
fill ~-4 ~2 ~-14 ~-4 ~2 ~-16 smooth_quartz_slab[type=top]

# 4. Colorful Awnings (Blue and White)
fill ~-4 ~3 ~-9 ~-6 ~3 ~-17 light_blue_stained_glass
fill ~-4 ~3 ~-10 ~-4 ~3 ~-12 white_wool
fill ~-4 ~3 ~-14 ~-4 ~3 ~-16 white_wool