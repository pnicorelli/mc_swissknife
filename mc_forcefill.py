#!/usr/bin/env python3
"""
forcefill.py – Force every minecraft inventory slot to 64 (or 16) items,
Works with both level.dat (singleplayer) and player.dat (multiplayer).

Usage:
    python forcefill.py level.dat                  # singleplayer
    python forcefill.py playerdata/<uuid>.dat      # multiplayer
"""

import sys
import shutil
from pathlib import Path
try:
    import nbtlib
except ImportError:
    print("Error: nbtlib is required. Install it with: pip install nbtlib")
    sys.exit(1)


# Items that stack to 16 instead of 64
STACK_16_ITEMS = {
    'minecraft:snowball',
    'minecraft:egg',
    'minecraft:ender_pearl',
    'minecraft:sign',
    'minecraft:oak_sign',
    'minecraft:spruce_sign',
    'minecraft:birch_sign',
    'minecraft:jungle_sign',
    'minecraft:acacia_sign',
    'minecraft:dark_oak_sign',
    'minecraft:crimson_sign',
    'minecraft:warped_sign',
    'minecraft:mangrove_sign',
    'minecraft:bamboo_sign',
    'minecraft:cherry_sign',
    'minecraft:bucket',
    'minecraft:water_bucket',
    'minecraft:lava_bucket',
    'minecraft:milk_bucket',
    'minecraft:powder_snow_bucket',
    'minecraft:axolotl_bucket',
    'minecraft:tadpole_bucket',
    'minecraft:cod_bucket',
    'minecraft:salmon_bucket',
    'minecraft:pufferfish_bucket',
    'minecraft:tropical_fish_bucket',
}

# Item categories that stack to 1 (tools, armor, etc.)
NON_STACKABLE_KEYWORDS = [
    'sword', 'pickaxe', 'axe', 'shovel', 'hoe',
    'helmet', 'chestplate', 'leggings', 'boots',
    'bow', 'crossbow', 'trident', 'shield',
    'shears', 'flint_and_steel', 'fishing_rod',
    'carrot_on_a_stick', 'warped_fungus_on_a_stick',
    'elytra', 'saddle', 'horse_armor',
    'music_disc', 'potion', 'splash_potion',
    'lingering_potion', 'enchanted_book',
    'writable_book', 'written_book',
    'suspicious_stew', 'totem_of_undying'
]


def is_non_stackable(item_id):
    """Check if an item is non-stackable (tools, armor, etc.)"""
    item_lower = item_id.lower()
    return any(keyword in item_lower for keyword in NON_STACKABLE_KEYWORDS)


def get_max_stack_size(item_id):
    """Determine the maximum stack size for an item"""
    if is_non_stackable(item_id):
        return 1
    elif item_id in STACK_16_ITEMS:
        return 16
    else:
        return 64


def process_inventory_slot(slot):
    """Process a single inventory slot and set count to max stack size"""
    if 'id' in slot:
        item_id = str(slot['id'])
        max_stack = get_max_stack_size(item_id)
        
        # Get current count
        current_count = int(slot.get('count', 1))
        
        # Set to max stack size
        slot['count'] = nbtlib.Byte(max_stack)
        
        return item_id, current_count, max_stack
    return None, None, None


def process_player_data(player_data):
    """Process player inventory data (works for both level.dat Player and playerdata/*.dat)"""
    modified_count = 0
    
    # Process Inventory
    if 'Inventory' in player_data:
        print("\nProcessing Inventory:")
        for slot in player_data['Inventory']:
            item_id, old_count, new_count = process_inventory_slot(slot)
            if item_id and old_count != new_count:
                print(f"  {item_id}: {old_count} → {new_count}")
                modified_count += 1
    
    # Process Ender Chest
    if 'EnderItems' in player_data:
        print("\nProcessing Ender Chest:")
        for slot in player_data['EnderItems']:
            item_id, old_count, new_count = process_inventory_slot(slot)
            if item_id and old_count != new_count:
                print(f"  {item_id}: {old_count} → {new_count}")
                modified_count += 1
    
    return modified_count


def forcefill_file(filepath):
    """Process either level.dat (singleplayer) or player.dat (multiplayer)"""
    filepath = Path(filepath)
    
    if not filepath.exists():
        print(f"Error: File '{filepath}' not found")
        return False
    
    # Create backup
    backup_path = filepath.with_suffix(filepath.suffix + '.backup')
    print(f"Creating backup: {backup_path}")
    shutil.copy2(filepath, backup_path)
    
    try:
        # Load NBT data
        print(f"Loading {filepath}...")
        nbt_file = nbtlib.load(filepath)
        
        # Check if this is level.dat (has Data.Player) or player.dat (direct player data)
        if 'Data' in nbt_file and 'Player' in nbt_file['Data']:
            print("Detected: level.dat (singleplayer world)")
            player_data = nbt_file['Data']['Player']
        elif 'Inventory' in nbt_file or 'EnderItems' in nbt_file:
            print("Detected: player.dat (multiplayer)")
            player_data = nbt_file
        else:
            print("Error: Could not find player data in file")
            print("Make sure you're using level.dat (singleplayer) or playerdata/<uuid>.dat (multiplayer)")
            return False
        
        # Process the player data
        modified_count = process_player_data(player_data)
        
        # Save modified NBT
        if modified_count > 0:
            print(f"\nSaving changes to {filepath}...")
            nbt_file.save(filepath)
            print(f"✓ Successfully modified {modified_count} slot(s)")
        else:
            print("\n✓ No changes needed - all slots already at max stack size")
        
        return True
        
    except Exception as e:
        print(f"Error processing file: {e}")
        print(f"Restoring backup...")
        shutil.copy2(backup_path, filepath)
        return False


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        print("\nExamples:")
        print("  python forcefill.py level.dat                    # singleplayer")
        print("  python forcefill.py playerdata/abc-123.dat       # multiplayer")
        sys.exit(1)
    
    filepath = sys.argv[1]
    success = forcefill_file(filepath)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()