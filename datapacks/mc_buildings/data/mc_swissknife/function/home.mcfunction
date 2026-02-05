say "Building a home"

# Clear the area
fill ~-8 ~ ~ ~8 ~12 ~-15 air
fill ~-8 ~-8 ~ ~8 ~-3 ~-15 stone
fill ~-8 ~-2 ~ ~8 ~-1 ~-15 grass_block

# Skelethon
fill ~-6 ~-4 ~-2 ~6 ~8 ~-13 stone
fill ~-5 ~-3 ~-3 ~5 ~-1 ~-12 air
fill ~-5 ~1 ~-3 ~5 ~3 ~-12 air
fill ~-5 ~5 ~-3 ~5 ~7 ~-12 air

# Roof
fill ~-6 ~9 ~-2 ~6 ~9 ~-13 stone_bricks

fill ~-7 ~8 ~-1 ~-7 ~8 ~-14 stone_brick_stairs[half=top,facing=east]
fill ~-7 ~8 ~-1 ~7 ~8 ~-1 stone_brick_stairs[half=top,facing=north]
fill ~7 ~8 ~-14 ~-7 ~8 ~-14 stone_brick_stairs[half=top,facing=south]
fill ~7 ~8 ~-14 ~7 ~8 ~-2 stone_brick_stairs[half=top,facing=west]

fill ~-7 ~9 ~-1 ~-7 ~9 ~-14 stone_brick_stairs[half=bottom,facing=east]
fill ~-7 ~9 ~-1 ~7 ~9 ~-1 stone_brick_stairs[half=bottom,facing=north]
fill ~7 ~9 ~-14 ~-7 ~9 ~-14 stone_brick_stairs[half=bottom,facing=south]
fill ~7 ~9 ~-14 ~7 ~9 ~-2 stone_brick_stairs[half=bottom,facing=west]

# Lights
setblock ~-5 ~-1 ~-3 lantern[hanging=true]
setblock ~-5 ~-1 ~-12 lantern[hanging=true]
setblock ~5 ~-1 ~-3 lantern[hanging=true]
setblock ~5 ~-1 ~-12 lantern[hanging=true]
setblock ~ ~-1 ~-7 lantern[hanging=true]

setblock ~-5 ~3 ~-3 lantern[hanging=true]
setblock ~-5 ~3 ~-12 lantern[hanging=true]
setblock ~5 ~3 ~-3 lantern[hanging=true]
setblock ~5 ~3 ~-12 lantern[hanging=true]
setblock ~ ~3 ~-7 lantern[hanging=true]

setblock ~-5 ~7 ~-3 lantern[hanging=true]
setblock ~-5 ~7 ~-12 lantern[hanging=true]
setblock ~5 ~7 ~-3 lantern[hanging=true]
setblock ~5 ~7 ~-12 lantern[hanging=true]
setblock ~ ~7 ~-7 lantern[hanging=true]

# Windows
fill ~-6 ~2 ~-2 ~-6 ~3 ~-13 glass_pane
fill ~-6 ~2 ~-2 ~6 ~3 ~-2 glass_pane
fill ~6 ~2 ~-13 ~-6 ~3 ~-13 glass_pane
fill ~6 ~2 ~-13 ~6 ~3 ~-2 glass_pane

fill ~-6 ~5 ~-2 ~-6 ~7 ~-13 glass_pane
fill ~-6 ~5 ~-2 ~6 ~7 ~-2 glass_pane
fill ~6 ~5 ~-13 ~-6 ~7 ~-13 glass_pane
fill ~6 ~5 ~-13 ~6 ~7 ~-2 glass_pane

# Entrance
fill ~-2 ~ ~-2 ~2 ~4 ~-4 stone
fill ~-1 ~ ~-2 ~1 ~3 ~-2 air
fill ~ ~1 ~-2 ~ ~2 ~-4 air
fill ~-1 ~ ~-2 ~1 ~ ~-2 stone_stairs
fill ~-1 ~3 ~-2 ~1 ~3 ~-2 stone_stairs[half=top]
setblock ~ ~1 ~-3 dark_oak_door[facing=south,half=lower,hinge=right]
setblock ~ ~2 ~-3 dark_oak_door[facing=south,half=upper,hinge=right]
setblock ~ ~1 ~-4 stone_pressure_plate

# Floors
fill ~-5 ~ ~-5 ~5 ~ ~-12 dark_oak_planks
fill ~-5 ~4 ~-5 ~5 ~4 ~-12 dark_oak_planks

# External Decorations
fill ~-6 ~ ~-2 ~-6 ~8 ~-2 dark_oak_wood
fill ~-6 ~ ~-13 ~-6 ~8 ~-13 dark_oak_wood
fill ~6 ~ ~-2 ~6 ~8 ~-2 dark_oak_wood
fill ~6 ~ ~-13 ~6 ~8 ~-13 dark_oak_wood
fill ~-2 ~ ~-2 ~-2 ~8 ~-2 dark_oak_wood
fill ~2 ~ ~-2 ~2 ~8 ~-2 dark_oak_wood

setblock ~-7 ~4 ~-2 dark_oak_fence
setblock ~-7 ~3 ~-2 lantern[hanging=true]
setblock ~-6 ~4 ~-1 dark_oak_fence
setblock ~-6 ~3 ~-1 lantern[hanging=true]

setblock ~-6 ~4 ~-14 dark_oak_fence
setblock ~-6 ~3 ~-14 lantern[hanging=true]
setblock ~-7 ~4 ~-13 dark_oak_fence
setblock ~-7 ~3 ~-13 lantern[hanging=true]

setblock ~6 ~4 ~-14 dark_oak_fence
setblock ~6 ~3 ~-14 lantern[hanging=true]
setblock ~7 ~4 ~-13 dark_oak_fence
setblock ~7 ~3 ~-13 lantern[hanging=true]

setblock ~6 ~4 ~-1 dark_oak_fence
setblock ~6 ~3 ~-1 lantern[hanging=true]
setblock ~7 ~4 ~-2 dark_oak_fence
setblock ~7 ~3 ~-2 lantern[hanging=true]

setblock ~-2 ~4 ~-1 dark_oak_fence
setblock ~-2 ~3 ~-1 lantern[hanging=true]
setblock ~2 ~4 ~-1 dark_oak_fence
setblock ~2 ~3 ~-1 lantern[hanging=true]

# Emerald Chest
setblock ~3 ~1 ~-4 chest[facing=east,type=left]
setblock ~3 ~1 ~-3 chest[facing=east,type=right]

item replace block ~3 ~1 ~-3 container.0 with emerald 64
item replace block ~3 ~1 ~-3 container.1 with emerald 64
item replace block ~3 ~1 ~-3 container.2 with emerald 64
item replace block ~3 ~1 ~-3 container.3 with emerald 64
item replace block ~3 ~1 ~-3 container.4 with emerald 64
item replace block ~3 ~1 ~-3 container.5 with emerald 64
item replace block ~3 ~1 ~-3 container.6 with emerald 64
item replace block ~3 ~1 ~-3 container.7 with emerald 64
item replace block ~3 ~1 ~-3 container.8 with emerald 64
item replace block ~3 ~1 ~-3 container.9 with diamond 64
item replace block ~3 ~1 ~-3 container.10 with diamond 64
item replace block ~3 ~1 ~-3 container.11 with diamond 64
item replace block ~3 ~1 ~-3 container.12 with diamond 64
item replace block ~3 ~1 ~-3 container.13 with diamond 64
item replace block ~3 ~1 ~-3 container.14 with diamond 64
item replace block ~3 ~1 ~-3 container.15 with diamond 64
item replace block ~3 ~1 ~-3 container.16 with diamond 64
item replace block ~3 ~1 ~-3 container.17 with diamond 64
summon glow_item_frame ~3 ~1 ~-4.5 {Facing:2,Item:{id:"minecraft:emerald",Count:1b}}