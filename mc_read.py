import nbtlib
import argparse
from pathlib import Path
from utils.NBTFile import NBTFile
from nbtlib.tag import List

def read_player_inventory(player_data):
    """Opens the NBT file and returns a dictionary of inventory items."""
    try:
        inventory = player_data.get('Inventory')
        if not inventory or not isinstance(inventory, List):
            return {}

        items_by_slot = {}
        for item_tag in inventory:
            try:
                slot = int(item_tag['Slot'])
                count = int(item_tag['count'])
                item_id = str(item_tag['id']).split(':')[-1]
                items_by_slot[slot] = {"id": item_id, "count": count}
            except KeyError:
                continue
        return items_by_slot
            
    except Exception as e:
        print(f"❌ Error reading inventory: {e}")
        return {}

def read_player_attributes(player_data):
    """Opens the NBT file and returns a dictionary of formatted attributes."""
    try:
        attributes_list = player_data.get('attributes') or player_data.get('Attributes')

        attr_dict = {}
        for attr in attributes_list:
            try:
                # Map internal IDs to UI labels
                name = str(attr['id']).split('.')[-1] # generic.max_health -> max_health
                value = float(attr['base'])
                attr_dict[name] = value
            except KeyError:
                continue
        return attr_dict

    except Exception as e:
        print(f"❌ Error reading attributes: {e}")
        return {}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Reads Minecraft player data (.dat) files.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument("file_path", type=str, help="Path to the UUID.dat file.")
    
    # Added argument to choose what to display
    parser.add_argument(
        "--mode", 
        choices=['inventory', 'attributes', 'all'], 
        default='all',
        help="Choose what data to display (default: all)"
    )
    
    args = parser.parse_args()
    filepath = Path(args.file_path)

    if not filepath.exists():
        print(f"❌ File not found: {args.file_path}")
        exit(1)

    try:
        # Load the NBT data once
        nbt = NBTFile(filepath)
        player_data = nbt.openfile()

        if args.mode in ['inventory', 'all']:
            inv = read_player_inventory(player_data)
            print("\n--- Player Inventory ---")
            for slot in sorted(inv.keys()):
                item = inv[slot]
                print(f"[Slot {slot:03d}]: {item['count']:02d}x {item['id']}")
        
        if args.mode in ['attributes', 'all']:
            attr = read_player_attributes(player_data)
            print("\n--- Player Attributes ---")
            for name in sorted(attr.keys()):
                value = attr[name]
                # Access the value directly and format it as a float
                print(f"{name:<40} | {value:<10.2f}")
        
    except Exception as e:
        print(f"❌ Failed to process file: {e}")    