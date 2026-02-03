say "Building a House with Overhanging Roof - North Facing"

# 1. Clear the area and set foundation
fill ~-6 ~-1 ~-2 ~5 ~10 ~-12 air
fill ~-5 ~-1 ~-2 ~4 ~-1 ~-12 stone

# 2. Structure (Hollow Box)
fill ~-5 ~0 ~-2 ~4 ~3 ~-12 white_glazed_terracotta
fill ~-4 ~0 ~-3 ~3 ~3 ~-11 air
# West side
fill ~-5 ~4 ~-3 ~-5 ~4 ~-11 white_glazed_terracotta
fill ~-5 ~5 ~-4 ~-5 ~5 ~-10 white_glazed_terracotta
fill ~-5 ~6 ~-5 ~-5 ~6 ~-9 white_glazed_terracotta
# East side
fill ~4 ~4 ~-3 ~4 ~4 ~-11 white_glazed_terracotta
fill ~4 ~5 ~-4 ~4 ~5 ~-10 white_glazed_terracotta
fill ~4 ~6 ~-5 ~4 ~6 ~-9 white_glazed_terracotta

# 3. Windows (Glass Panes)
fill ~-5 ~1 ~-4 ~-5 ~2 ~-10 glass_pane
fill ~4 ~1 ~-4 ~4 ~2 ~-10 glass_pane

# 4. The Roof (Overhanging and Flipped)
# Row 1 (Lowest) - Extra wide on X
fill ~-6 ~3 ~-2 ~5 ~3 ~-2 stone_stairs[facing=north]
fill ~-6 ~3 ~-12 ~5 ~3 ~-12 stone_stairs[facing=south]

# Row 2
fill ~-6 ~4 ~-3 ~5 ~4 ~-3 stone_stairs[facing=north]
fill ~-6 ~4 ~-11 ~5 ~4 ~-11 stone_stairs[facing=south]

# Row 3
fill ~-6 ~5 ~-4 ~5 ~5 ~-4 stone_stairs[facing=north]
fill ~-6 ~5 ~-10 ~5 ~5 ~-10 stone_stairs[facing=south]

# Row 4 
fill ~-6 ~6 ~-5 ~5 ~6 ~-5 stone_stairs[facing=north]
fill ~-6 ~6 ~-9 ~5 ~6 ~-9 stone_stairs[facing=south]

# Row 5 (The Peak) - Using Stone Blocks to bridge the final gap
fill ~-6 ~7 ~-6 ~5 ~7 ~-8 stone


# 5. Lighting (Ceiling at Y=3)
setblock ~-4 ~2 ~-4 lantern[hanging=true]
setblock ~-4 ~3 ~-4 iron_chain
setblock ~-4 ~4 ~-4 iron_chain
setblock ~-4 ~2 ~-10 lantern[hanging=true]
setblock ~-4 ~3 ~-10 iron_chain
setblock ~-4 ~4 ~-10 iron_chain
setblock ~3 ~2 ~-4 lantern[hanging=true]
setblock ~3 ~3 ~-4 iron_chain
setblock ~3 ~4 ~-4 iron_chain
setblock ~3 ~2 ~-10 lantern[hanging=true]
setblock ~3 ~3 ~-10 iron_chain
setblock ~3 ~4 ~-10 iron_chain

# 6. Doors (South)
setblock ~-1 ~0 ~-2 oak_door[facing=south,half=lower,hinge=right]
setblock ~-1 ~1 ~-2 oak_door[facing=south,half=upper,hinge=right]
setblock ~0 ~0 ~-2 oak_door[facing=south,half=lower,hinge=left]
setblock ~0 ~1 ~-2 oak_door[facing=south,half=upper,hinge=left]
setblock ~-1 ~0 ~-3 stone_pressure_plate
setblock ~0 ~0 ~-3 stone_pressure_plate

# 7. Doors (North)
setblock ~-1 ~0 ~-12 oak_door[facing=north,half=lower,hinge=left]
setblock ~-1 ~1 ~-12 oak_door[facing=north,half=upper,hinge=left]
setblock ~0 ~0 ~-12 oak_door[facing=north,half=lower,hinge=right]
setblock ~0 ~1 ~-12 oak_door[facing=north,half=upper,hinge=right]
setblock ~-1 ~0 ~-11 stone_pressure_plate
setblock ~0 ~0 ~-11 stone_pressure_plate

# 8. Beds (West)
setblock ~-4 ~0 ~-3 white_bed[facing=west,part=head]
setblock ~-3 ~0 ~-3 white_bed[facing=west,part=foot]
setblock ~-4 ~0 ~-5 white_bed[facing=west,part=head]
setblock ~-3 ~0 ~-5 white_bed[facing=west,part=foot]
setblock ~-4 ~0 ~-7 white_bed[facing=west,part=head]
setblock ~-3 ~0 ~-7 white_bed[facing=west,part=foot]
setblock ~-4 ~0 ~-9 white_bed[facing=west,part=head]
setblock ~-3 ~0 ~-9 white_bed[facing=west,part=foot]
setblock ~-4 ~0 ~-11 white_bed[facing=west,part=head]
setblock ~-3 ~0 ~-11 white_bed[facing=west,part=foot]

# 9. Beds (East)
setblock ~3 ~0 ~-3 white_bed[facing=east,part=head]
setblock ~2 ~0 ~-3 white_bed[facing=east,part=foot]
setblock ~3 ~0 ~-5 white_bed[facing=east,part=head]
setblock ~2 ~0 ~-5 white_bed[facing=east,part=foot]
setblock ~3 ~0 ~-7 white_bed[facing=east,part=head]
setblock ~2 ~0 ~-7 white_bed[facing=east,part=foot]
setblock ~3 ~0 ~-9 white_bed[facing=east,part=head]
setblock ~2 ~0 ~-9 white_bed[facing=east,part=foot]
setblock ~3 ~0 ~-11 white_bed[facing=east,part=head]
setblock ~2 ~0 ~-11 white_bed[facing=east,part=foot]