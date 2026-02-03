say "Constructing The Quartz Plaza..."

# 1. Clear the area (15x15)
fill ~-7 ~0 ~-7 ~7 ~5 ~-21 air

# 2. The Floor (Chiseled Quartz with a Quartz Brick Border)
# Outer Border
fill ~-7 ~-1 ~-7 ~7 ~-1 ~-21 quartz_bricks
# Inner Surface
fill ~-6 ~-1 ~-8 ~6 ~-1 ~-20 chiseled_quartz_block

# 3. The Fountain (Center at ~0 ~-14)
# Create a 5x5 solid base of Quartz Bricks
fill ~-2 ~0 ~-12 ~2 ~0 ~-16 quartz_bricks

# Hollow out the basin (leave the outer rim)
# This creates a 3x3 hole for the water to sit in
fill ~-1 ~0 ~-13 ~1 ~0 ~-15 air

# Fill the basin with still water
fill ~-1 ~0 ~-13 ~1 ~0 ~-15 water

# Central Pillar (placed in the very center)
setblock ~0 ~0 ~-14 chiseled_quartz_block
setblock ~0 ~1 ~-14 chiseled_quartz_block

# The Water Source (at the top of the pillar)
# It will flow down into the 3x3 basin and stay inside the rim
setblock ~0 ~2 ~-14 water

# 4. The Bell Pedestal (The Meeting Point)
# Villagers look for the Bell to start their "gathering" AI
setblock ~2 ~0 ~-9 quartz_pillar
setblock ~2 ~1 ~-9 bell[attachment=floor,facing=north]

# 5. Lampposts (Four corners)
# Corner 1
fill ~-5 ~0 ~-9 ~-5 ~2 ~-9 quartz_pillar
setblock ~-5 ~2 ~-9 lantern
# Corner 2
fill ~5 ~0 ~-9 ~5 ~2 ~-9 quartz_pillar
setblock ~5 ~2 ~-9 lantern
# Corner 3
fill ~-5 ~0 ~-19 ~-5 ~2 ~-19 quartz_pillar
setblock ~-5 ~2 ~-19 lantern
# Corner 4
fill ~5 ~0 ~-19 ~5 ~2 ~-19 quartz_pillar
setblock ~5 ~2 ~-19 lantern

# 6. Benches (Smooth Quartz Stairs)
setblock ~-3 ~0 ~-10 smooth_quartz_stairs[facing=south]
setblock ~-2 ~0 ~-10 smooth_quartz_stairs[facing=south]
setblock ~2 ~0 ~-18 smooth_quartz_stairs[facing=north]
setblock ~3 ~0 ~-18 smooth_quartz_stairs[facing=north]