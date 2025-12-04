import nbtlib
import argparse
import os
# Import specific NBT tags for clarity, though not strictly required for this logic
from nbtlib.tag import Compound, List, Int, Byte, String 

def read_player_inventory(file_path):
    """Reads the player data file and prints the inventory contents."""
    
    # 1. Check if the file exists
    if not os.path.exists(file_path):
        print(f"❌ ERROR: The player data file was not found: {file_path}")
        return

    print(f"📖 Reading player data file: {file_path}")
    
    try:
        # Load the NBT file (player data is usually uncompressed)
        nbt_file = nbtlib.load(file_path)
        player_data = nbt_file['Data']['Player']
        # Access the Inventory list. It should be a List[Compound]
        inventory = player_data.get('Inventory')
        
        if inventory is None or not isinstance(inventory, List) or not inventory:
            print("ℹ️ INFO: Could not find any items in the 'Inventory' tag.")
            return

        items_by_slot = {}
        
        for item_tag in inventory:
            # Explicitly cast NBT tag objects to standard Python types for safety
            try:
                # Use .real to get the underlying Python value (int for Byte/Int)
                slot = item_tag['Slot'].real
                count = item_tag['count'].real
                # Ensure it's treated as a string
                item_id = str(item_tag['id']) 
                
                # We only process items that have the required tags
                if slot is not None and count is not None and item_id:
                    items_by_slot[slot] = {
                        "id": item_id.split(':')[-1], # Strip 'minecraft:'
                        "count": count
                    }
                
            except KeyError as e:
                # Catch items missing 'Slot', 'Count', or 'id'
                print(f"⚠️ Warning: Skipped item missing required tag {e}: {item_tag}")
            except Exception as e:
                # Catch any unexpected error during item processing
                print(f"❌ Error processing item tag {item_tag}: {e}")

        # --- Print the Results ---
        print("\n--- 🎒 Player Inventory Contents ---")
        
        if not items_by_slot:
            print("No valid inventory items found after processing.")
            return

        # Print the items ordered by slot
        for slot in sorted(items_by_slot.keys()):
            item = items_by_slot[slot]
            
            # Categorize the slot for human readability
            if 0 <= slot <= 8:
                area = "Hotbar"
                index = slot
            elif 9 <= slot <= 35:
                area = "Main"
                index = slot - 9
            elif slot == -106:
                 area = "Offhand"
                 index = "-"
            elif -103 <= slot <= -100:
                area = "Armor"
                # Slot -100 is Helmet, -101 Chestplate, -102 Leggings, -103 Boots
                index = str(-100 - slot).replace('0', 'H').replace('1', 'C').replace('2', 'L').replace('3', 'B')
            else:
                area = "Other"
                index = slot

            print(f"[Slot {slot:03d} | {area: <8} {index:>2}]: {item['count']:02d}x {item['id']}")
            
        print("---------------------------------")
        return items_by_slot
        
    except nbtlib.exceptions.LoadError as e:
        print(f"❌ ERROR: Failed to load NBT data. Is the file corrupted or not a valid NBT format? ({e})")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Setup ArgumentParser
    parser = argparse.ArgumentParser(
        description="Reads and displays the inventory from a Minecraft player data (.dat) file.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # Add the required positional argument for the file path
    parser.add_argument(
        "file_path", 
        type=str,
        help="The full path to the player's data file (UUID.dat) in the world's folder.\n"
             "Example: /home/willy/.minecraft/saves/nov25/level.dat"
    )
    
    # Parse the arguments from the command line
    args = parser.parse_args()
    
    # Call the main function with the argument received from the command line
    read_player_inventory(args.file_path)