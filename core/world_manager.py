"""
World Manager - Business logic for managing Minecraft worlds
Handles both legacy (pre-breaking change) and new player data formats
"""
import os
from pathlib import Path
from utils.NBTFile import NBTFile
from core.mc_player import read_player_inventory, read_player_attributes, write_player_attributes
from core.mc_forcefill import forcefill_file
from core.mc_datapacks import MC_DATAPACKS


class WorldInfo:
    """
    Represents information about a Minecraft world
    
    Attributes:
        name: World directory name
        path: Full path to the world directory
        is_singleplayer: True if single-player, False if multiplayer
        player_data_path: Path to the player's .dat file
    """
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.is_singleplayer = None
        self.player_data_path = None
        self._player_uuid = None
    
    def detect_player_data_location(self):
        """
        Detect where the player data is stored for this world.
        Handles both old format (player data in level.dat) and new format (separate player files).
        
        Returns:
            bool: True if detection successful, False otherwise
        """
        level_dat_path = os.path.join(self.path, "level.dat")
        
        if not os.path.exists(level_dat_path):
            return False
        
        try:
            nbt = NBTFile(level_dat_path)
            level_data = nbt.openfile()
            data = level_data.get("Data", {})
            print(data)
            # Check for new format: singleplayer_uuid field
            player_uuid = data.get("singleplayer_uuid")
            
            if player_uuid is not None:
                # New format: player data in separate file
                self.is_singleplayer = True
                self._player_uuid = player_uuid
                uuid_str = self._format_uuid(player_uuid)
                self.player_data_path = os.path.join(
                    self.path, 
                    "players/data", 
                    f"{uuid_str}.dat"
                )
            else:
                # Check if Player data exists in level.dat (old format)
                if "Player" in data:
                    self.is_singleplayer = True
                    self.player_data_path = level_dat_path
                else:
                    # Multiplayer world or no player data
                    self.is_singleplayer = False
                    # For multiplayer, we'd need to know which player to load
                    # This would require additional UI for player selection
                    self.player_data_path = None

            return True
            
        except Exception as e:
            print(f"Error detecting player data location: {e}")
            return False
    
    @staticmethod
    def _format_uuid(uuid_ints):
        """
        Convert UUID integer array to standard UUID string format
        
        Args:
            uuid_ints: List of 4 integers representing the UUID
            
        Returns:
            str: UUID in format "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        """
        # Convert each int to an 8-character hex string
        hex_parts = [format(i & 0xFFFFFFFF, '08x') for i in uuid_ints]
        
        # Combine them into one string
        full_hex = "".join(hex_parts)
        
        # Format with dashes (8-4-4-4-12)
        uuid_str = f"{full_hex[:8]}-{full_hex[8:12]}-{full_hex[12:16]}-{full_hex[16:20]}-{full_hex[20:]}"
        
        return uuid_str
    
    def get_player_data(self):
        """
        Load and return the player data NBT
        
        Returns:
            dict: Player data from NBT file, or None if unavailable
        """
        if not self.player_data_path or not os.path.exists(self.player_data_path):
            return None
        
        try:
            nbt = NBTFile(self.player_data_path)
            player_data = nbt.openfile()
            
            # If player data is in level.dat, extract the Player section
            if self.player_data_path.endswith("level.dat"):
                data = player_data.get("Data", {})
                return data.get("Player", {})
            else:
                # Player data is in its own file
                return player_data
                
        except Exception as e:
            print(f"Error loading player data: {e}")
            return None
    
    def save_player_data(self, player_data):
        """
        Save player data back to the appropriate file
        
        Args:
            player_data: Player data dictionary to save
            
        Returns:
            bool: True if save successful, False otherwise
        """
        if not self.player_data_path:
            return False
        
        try:
            nbt = NBTFile(self.player_data_path)
            
            # If player data is in level.dat, we need to update the Player section
            if self.player_data_path.endswith("level.dat"):
                full_data = nbt.openfile()
                if "Data" not in full_data:
                    full_data["Data"] = {}
                full_data["Data"]["Player"] = player_data
                nbt.savefile(full_data)
            else:
                # Player data is in its own file, save directly
                nbt.openfile()
                nbt.savefile(player_data)
            
            return True
            
        except Exception as e:
            print(f"Error saving player data: {e}")
            return False


class WorldManager:
    """Manages Minecraft world data and operations"""
    
    def __init__(self):
        self.worlds = {}  # {world_name: WorldInfo}
        self.current_world_name = None
    
    def scan_worlds(self, minecraft_path):
        """
        Scan for Minecraft worlds in the given path
        
        Args:
            minecraft_path: Path to Minecraft saves directory
            
        Returns:
            Dictionary of world names to paths (for backward compatibility)
        """
        path = os.path.expanduser(minecraft_path)
        
        if not os.path.exists(path):
            return {}
        
        self.worlds.clear()
        
        for directory in sorted(os.listdir(path)):
            full_path = os.path.join(path, directory)
            if os.path.isdir(full_path):
                world_info = WorldInfo(directory, full_path)
                world_info.detect_player_data_location()
                self.worlds[directory] = world_info
        
        # Return simple dict for backward compatibility
        world = {name: info.path for name, info in self.worlds.items()}
        return world
    
    def get_world_path(self, world_name):
        """Get the path for a specific world"""
        world_info = self.worlds.get(world_name)
        return world_info.path if world_info else None
    
    def get_world_info(self, world_name):
        """
        Get the WorldInfo object for a specific world
        
        Args:
            world_name: Name of the world
            
        Returns:
            WorldInfo object or None
        """
        return self.worlds.get(world_name)
    
    def get_current_world_info(self):
        """Get the WorldInfo of the currently selected world"""
        if self.current_world_name:
            return self.worlds.get(self.current_world_name)
        return None
    
    def get_current_world_path(self):
        """Get the path of the currently selected world"""
        world_info = self.get_current_world_info()
        return world_info.path if world_info else None
    
    def load_world_data(self, world_path):
        """
        Load all data for a world
        
        Args:
            world_path: Path to the world directory
            
        Returns:
            Dictionary containing inventory, attributes, and datapacks data
            
        Raises:
            Exception: If world not found or player data unavailable
        """
        # Find the WorldInfo for this path
        world_info = None
        for name, info in self.worlds.items():
            if info.path == world_path:
                world_info = info
                self.current_world_name = name
                break
        
        if not world_info:
            raise Exception(f"World not found: {world_path}")
        
        # Ensure player data location is detected
        if world_info.player_data_path is None:
            world_info.detect_player_data_location()
        
        if world_info.player_data_path is None:
            raise Exception("Could not find player data for this world")
        
        if not world_info.is_singleplayer:
            raise Exception("Multiplayer worlds are not yet supported. Please select a single-player world.")
        
        # Load player data
        player_data = world_info.get_player_data()
        
        if not player_data:
            raise Exception("Failed to load player data")
        
        # Load inventory
        inventory = read_player_inventory(player_data)
        
        # Load attributes
        attributes = read_player_attributes(player_data)
        
        # Load datapacks status
        datapacks = MC_DATAPACKS.checkStatus(world_path)
        
        return {
            'inventory': inventory,
            'attributes': attributes,
            'datapacks': datapacks
        }
    
    def force_fill_inventory(self, world_path):
        """
        Force fill the player's inventory
        
        Args:
            world_path: Path to the world directory
        """
        world_info = self._get_world_info_by_path(world_path)
        
        if not world_info or not world_info.player_data_path:
            raise Exception("Cannot find player data file")
        
        # Force fill uses the player data file directly
        forcefill_file(world_info.player_data_path)
    
    def save_attributes(self, world_path, attributes_data):
        """
        Save player attributes to the world
        
        Args:
            world_path: Path to the world directory
            attributes_data: Dictionary of attribute names to values
        """
        world_info = self._get_world_info_by_path(world_path)
        
        if not world_info or not world_info.player_data_path:
            raise Exception("Cannot find player data file")
        
        # Load current player data
        player_data = world_info.get_player_data()
        
        if not player_data:
            raise Exception("Failed to load player data")
        
        # Separate minecraft attributes from other attributes
        minecraft_attributes = {
            k: v for k, v in attributes_data.items()
            if k.startswith("minecraft:")
        }
        
        # Write XpLevel if present
        if "XpLevel" in attributes_data:
            write_player_attributes(
                player_data,
                "XpLevel",
                int(attributes_data["XpLevel"])
            )
        
        # Write minecraft attributes
        if minecraft_attributes:
            write_player_attributes(
                player_data,
                "attributes",
                minecraft_attributes
            )
        
        # Save the modified player data
        if not world_info.save_player_data(player_data):
            raise Exception("Failed to save player data")
    
    def add_datapack(self, world_path, datapack_index):
        """
        Add a datapack to the world
        
        Args:
            world_path: Path to the world directory
            datapack_index: Index of the datapack to add
        """
        MC_DATAPACKS.add(world_path, datapack_index)
    
    def remove_datapack(self, world_path, datapack_index):
        """
        Remove a datapack from the world
        
        Args:
            world_path: Path to the world directory
            datapack_index: Index of the datapack to remove
        """
        MC_DATAPACKS.delete(world_path, datapack_index)
    
    def _get_world_info_by_path(self, world_path):
        """
        Helper method to get WorldInfo by path
        
        Args:
            world_path: Path to the world directory
            
        Returns:
            WorldInfo object or None
        """
        for world_info in self.worlds.values():
            if world_info.path == world_path:
                return world_info
        return None