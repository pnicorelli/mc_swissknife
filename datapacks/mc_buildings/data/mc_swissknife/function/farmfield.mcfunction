say "Building a Farmfield for 4 farmer"

# Clear the area
fill ~-7 ~ ~ ~7 ~8 ~-13 air
fill ~-7 ~-3 ~ ~7 ~-5 ~-13 stone
fill ~-7 ~-1 ~ ~7 ~-2 ~-13 grass_block
fill ~-4 ~-1 ~-3 ~4 ~-1 ~-11 farmland[moisture=7]

# Coltures
fill ~-4 ~ ~-3 ~-3 ~ ~-11 potatoes[age=7]
fill ~-2 ~ ~-3 ~ ~ ~-11 wheat[age=7]
fill ~1 ~ ~-3 ~2 ~ ~-11 carrots[age=7]
fill ~3 ~ ~-3 ~4 ~ ~-11 beetroots[age=3]

# Composter
setblock ~-2 ~-1 ~-5 composter 
setblock ~-2 ~-1 ~-9 composter
setblock ~2 ~-1 ~-5 composter
setblock ~2 ~-1 ~-9 composter

# Lights
setblock ~ ~-1 ~-7 oak_fence[waterlogged=true]
fill ~ ~ ~-7 ~ ~3 ~-7 oak_fence
fill ~-2 ~3 ~-7 ~2 ~3 ~-7 oak_fence
fill ~ ~3 ~-9 ~ ~3 ~-5 oak_fence
setblock ~-2 ~2 ~-7 lantern[hanging=true]
setblock ~2 ~2 ~-7 lantern[hanging=true]
setblock ~ ~2 ~-9 lantern[hanging=true]
setblock ~ ~2 ~-5 lantern[hanging=true]

