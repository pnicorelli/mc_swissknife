"""
Docstring for utils.NBTFile

Handle NBT's file operations. 

Usage

nbt = NBTFile("level.dat")
player_data = nbt.openfile()

# --- your code to update stuff ---
# process_player_data(player_data)

nbt.savefile(player_data)
"""
import sys
import shutil
from pathlib import Path

try:
    import nbtlib
except ImportError:
    print("Error: nbtlib is required. Install it with: pip install nbtlib")
    sys.exit(1)


class NBTFile:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.nbt_file = None
        self.player_data = None
        self.is_level_dat = False

        if not self.filepath.exists():
            raise FileNotFoundError(f"File '{self.filepath}' not found")

    def openfile(self):
        """
        Loads the NBT file and returns player data.
        Supports:
        - level.dat (singleplayer)
        - playerdata/<uuid>.dat (multiplayer)
        """
        print(f"Loading {self.filepath}...")
        self.nbt_file = nbtlib.load(self.filepath)

        # Detect file type
        if 'Data' in self.nbt_file and 'Player' in self.nbt_file['Data']:
            print("Detected: level.dat (singleplayer world)")
            self.player_data = self.nbt_file['Data']['Player']
            self.is_level_dat = True

        elif 'Inventory' in self.nbt_file or 'EnderItems' in self.nbt_file:
            print("Detected: player.dat (multiplayer)")
            self.player_data = self.nbt_file
            self.is_level_dat = False
            
        elif 'Data' in self.nbt_file:
            print("Detected: level.dat (new version)")
            self.player_data = self.nbt_file
            self.is_level_dat = False

        else:
            raise ValueError(
                "Could not find player data in file. "
                "Use level.dat or playerdata/<uuid>.dat"
            )

        return self.player_data

    def savefile(self, player_data):
        """
        Saves updated player data back to file.
        Automatically creates a backup before saving.
        """
        if self.nbt_file is None:
            raise RuntimeError("File not opened. Call openfile() first.")

        # Update internal reference
        if self.is_level_dat:
            self.nbt_file['Data']['Player'] = player_data
        else:
            self.nbt_file = player_data

        # Create backup
        backup_path = self.filepath.with_suffix(self.filepath.suffix + '.backup')
        print(f"Creating backup: {backup_path}")
        shutil.copy2(self.filepath, backup_path)

        try:
            print(f"Saving changes to {self.filepath}...")
            self.nbt_file.save(self.filepath)
            print("✓ Save completed successfully")

        except Exception as e:
            print(f"Error saving file: {e}")
            print("Restoring backup...")
            shutil.copy2(backup_path, self.filepath)
            raise
