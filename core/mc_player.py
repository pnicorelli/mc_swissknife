import nbtlib
import argparse
from pathlib import Path
from utils.NBTFile import NBTFile
from nbtlib.tag import Compound, List, String, Int, Double, Float

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
        xp = player_data.get('XpLevel')
        attr_dict = {}
        attr_dict['XpLevel'] = int(xp)
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

def write_player_attributes(player_data, field_name, val_array):
    """
    Writes attributes to player_data NBT structure using nbtlib types.
    """
    try:
        # Case 1: Plain scalar field (e.g., 'XpLevel', 'Health')
        if field_name.lower() not in ('attributes'):
            value = val_array[0] if isinstance(val_array, (list, tuple)) else val_array
            
            # Cast to nbtlib types based on Python type
            if isinstance(value, int):
                player_data[field_name] = Int(value)
            elif isinstance(value, float):
                player_data[field_name] = Float(value)
            else:
                player_data[field_name] = String(str(value))
            return True

        # Case 2: Attributes list
        if not isinstance(val_array, dict):
            raise ValueError("Attributes must be provided as a list of dicts")

        # Minecraft attributes typically use 'Name' and 'Base' or 'id' and 'base' 
        # depending on the game version. Using 'id' and 'base' as per your logic.
        attr_list = []
        for attr_dict in val_array:
            
            # Minecraft Attributes usually expect Doubles for the 'base' value
            base_val = val_array[attr_dict]
            nbt_val = Double(base_val)
            # print(base_val, nbt_val)
            attr_list.append(Compound({
                'id': String(attr_dict),
                'base': nbt_val
            }))

        # In nbtlib, we must wrap the list in a List tag specifying the type
        player_data[field_name] = List[Compound](attr_list)
        print(f"✓ Successfully wrote {len(attr_list)} attributes to {field_name}")
        return True

    except Exception as e:
        print(f"❌ Error writing attributes: {e}")
        return False

    
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