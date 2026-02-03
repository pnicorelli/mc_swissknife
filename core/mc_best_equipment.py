#!/usr/bin/env python3
"""
mc_best_equipment.py – Give player full enchanted golden armor + diamond tools
with max enchantments, plus useful items (cooked beef, torches, spyglass).

Usage:
    python mc_best_equipment.py level.dat                    # singleplayer
    python mc_best_equipment.py playerdata/<uuid>.dat        # multiplayer
"""

import sys
import shutil
from pathlib import Path
from utils.NBTFile import NBTFile
try:
    import nbtlib
    from nbtlib.tag import Compound, List, String, Byte, Short, Int
except ImportError:
    print("Error: nbtlib is required. Install it with: pip install nbtlib")
    sys.exit(1)


def create_golden_helmet():
    """Golden helmet with all protective enchantments"""
    return Compound({
        'id': String('minecraft:golden_helmet'),
        'count': Byte(1),
        'components': Compound({
            'minecraft:enchantments': Compound({
                'minecraft:protection': Int(5),
                'minecraft:respiration': Int(5),
                'minecraft:aqua_affinity': Int(1),
                'minecraft:unbreaking': Int(5),
                'minecraft:mending': Int(1)
            })
        })
    })


def create_golden_chestplate():
    """Golden chestplate with all protective enchantments"""
    return Compound({
        'id': String('minecraft:golden_chestplate'),
        'count': Byte(1),
        'components': Compound({
            'minecraft:enchantments': Compound({
                'minecraft:protection': Int(5),
                'minecraft:unbreaking': Int(5),
                'minecraft:mending': Int(1),
                'minecraft:thorns': Int(5)
            })
        })
    })


def create_golden_leggings():
    """Golden leggings with all protective enchantments"""
    return Compound({
        'id': String('minecraft:golden_leggings'),
        'count': Byte(1),
        'components': Compound({
            'minecraft:enchantments': Compound({
                'minecraft:protection': Int(5),
                'minecraft:unbreaking': Int(5),
                'minecraft:mending': Int(1),
                'minecraft:thorns': Int(5)
            })
        })
    })


def create_golden_boots():
    """Golden boots with all protective enchantments"""
    return Compound({
        'id': String('minecraft:golden_boots'),
        'count': Byte(1),
        'components': Compound({
            'minecraft:enchantments': Compound({
                'minecraft:protection': Int(5),
                'minecraft:feather_falling': Int(5),
                'minecraft:depth_strider': Int(5),
                'minecraft:unbreaking': Int(5),
                'minecraft:mending': Int(1),
                'minecraft:soul_speed': Int(5)
            })
        })
    })


def create_diamond_sword():
    """Diamond sword with best combat enchantments"""
    return Compound({
        'id': String('minecraft:diamond_sword'),
        'count': Byte(1),
        'components': Compound({
            'minecraft:enchantments': Compound({
                'minecraft:sharpness': Int(5),
                'minecraft:sweeping_edge': Int(5),
                'minecraft:looting': Int(5),
                'minecraft:unbreaking': Int(5),
                'minecraft:mending': Int(1),
                'minecraft:fire_aspect': Int(5),
                'minecraft:smite	': Int(5),
                'minecraft:fortune	': Int(5)
            })
        })
    })


def create_diamond_pickaxe():
    """Diamond pickaxe with best mining enchantments"""
    return Compound({
        'id': String('minecraft:diamond_pickaxe'),
        'count': Byte(1),
        'components': Compound({
            'minecraft:enchantments': Compound({
                'minecraft:efficiency': Int(5),
                'minecraft:fortune': Int(5),
                'minecraft:unbreaking': Int(5),
                'minecraft:mending': Int(1),
                'minecraft:fortune	': Int(5)
            })
        })
    })


def create_diamond_axe():
    """Diamond axe with best enchantments"""
    return Compound({
        'id': String('minecraft:diamond_axe'),
        'count': Byte(1),
        'components': Compound({
            'minecraft:enchantments': Compound({
                'minecraft:efficiency': Int(5),
                'minecraft:sharpness': Int(5),
                'minecraft:unbreaking': Int(5),
                'minecraft:fortune	': Int(5)
            })
        })
    })


def create_diamond_shovel():
    """Diamond shovel with best enchantments"""
    return Compound({
        'id': String('minecraft:diamond_shovel'),
        'count': Byte(1),
        'components': Compound({
            'minecraft:enchantments': Compound({
                'minecraft:efficiency': Int(5),
                'minecraft:unbreaking': Int(5),
                'minecraft:mending': Int(1),
                'minecraft:fortune	': Int(5)
            })
        })
    })


def create_diamond_hoe():
    """Diamond hoe with best enchantments"""
    return Compound({
        'id': String('minecraft:diamond_hoe'),
        'count': Byte(1),
        'components': Compound({
            'minecraft:enchantments': Compound({
                'minecraft:efficiency': Int(5),
                'minecraft:unbreaking': Int(5),
                'minecraft:mending': Int(1),
                'minecraft:fortune	': Int(5)
            })
        })
    })


def create_simple_item(item_id, count):
    """Create a simple item with count"""
    return Compound({
        'id': String(item_id),
        'count': Byte(count)
    })


def setup_best_equipment(player_data):
    """Setup armor slots and hotbar with best equipment"""
    
    print("\n=== Setting up equipment ===")
    
    # Ensure Inventory exists as proper List[Compound]
    if 'Inventory' not in player_data:
        player_data['Inventory'] = List[Compound]([])
    
    # Convert to list if needed
    inventory_list = list(player_data['Inventory'])
    
    # Remove existing hotbar and armor items
    inventory_list = [item for item in inventory_list if 
                     int(item.get('Slot', Byte(0))) not in 
                     list(range(9)) + [100, 101, 102, 103]]
    
    # Hotbar setup (slots 0-8)
    hotbar_items = [
        (0, create_diamond_sword(), "Diamond Sword (Sharpness V, Looting III, Mending)"),
        (1, create_diamond_pickaxe(), "Diamond Pickaxe (Efficiency V, Fortune III, Mending)"),
        (2, create_diamond_axe(), "Diamond Axe (Efficiency V, Sharpness V, Silk Touch)"),
        (3, create_diamond_shovel(), "Diamond Shovel (Efficiency V, Mending)"),
        (4, create_diamond_hoe(), "Diamond Hoe (Efficiency V, Mending)"),
        (5, create_simple_item('minecraft:spyglass', 1), "Spyglass"),
        (6, create_simple_item('minecraft:shears', 1), "Shears"),
        (7, create_simple_item('minecraft:cooked_beef', 64), "Cooked Beef x64"),
        (8, create_simple_item('minecraft:torch', 64), "Torches x64"),
    ]
    
    print("\n📦 Hotbar:")
    for slot, item, description in hotbar_items:
        item['Slot'] = Byte(slot)
        inventory_list.append(item)
        print(f"  Slot {slot}: {description}")
    
    # Armor setup (slots 100-103)
    armor_items = [
        (9, create_golden_boots(), "Golden Boots (Protection IV, Feather Falling IV, Depth Strider III)"),
        (10, create_golden_leggings(), "Golden Leggings (Protection IV, Thorns III)"),
        (11, create_golden_chestplate(), "Golden Chestplate (Protection IV, Thorns III)"),
        (12, create_golden_helmet(), "Golden Helmet (Protection IV, Respiration III, Aqua Affinity)"),
    ]
    
    print("\n🛡️  Armor:")
    for slot, item, description in armor_items:
        item['Slot'] = Byte(slot)
        inventory_list.append(item)
        print(f"  Slot {slot}:   {description}")
    
    # Replace inventory with new list
    player_data['Inventory'] = List[Compound](inventory_list)
    
    print("\n✓ Equipment setup complete!")
    return len(hotbar_items) + len(armor_items)


def process_file(filepath):
    filepath = Path(filepath)
    nbt = NBTFile(filepath)
    player_data = nbt.openfile()
    modified_count = setup_best_equipment(player_data)
        
    # Save modified NBT
    if modified_count > 0:
        print(f"\nSaving changes to {filepath}...")
        nbt.savefile(player_data)
        print(f"✓ Successfully modified {modified_count} slot(s)")
    else:
        print("\n✓ No changes needed - all slots already at max stack size")
    
    return True


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        print("\nExamples:")
        print("  python best_equipment.py level.dat                    # singleplayer")
        print("  python best_equipment.py playerdata/abc-123.dat       # multiplayer")
        sys.exit(1)
    
    filepath = sys.argv[1]
    success = process_file(filepath)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()