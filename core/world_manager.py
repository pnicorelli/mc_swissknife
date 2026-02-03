"""
World Manager - Business logic for managing Minecraft worlds
"""
import os
from pathlib import Path
from utils.NBTFile import NBTFile
from core.mc_player import read_player_inventory, read_player_attributes, write_player_attributes
from core.mc_forcefill import forcefill_file
from core.mc_datapacks import MC_DATAPACKS


class WorldManager:
    """Manages Minecraft world data and operations"""
    
    def __init__(self):
        self.worlds = {}
        self.current_world_name = None
    
    def scan_worlds(self, minecraft_path):
        """
        Scan for Minecraft worlds in the given path
        
        Args:
            minecraft_path: Path to Minecraft saves directory
            
        Returns:
            Dictionary of world names to paths
        """
        path = os.path.expanduser(minecraft_path)
        
        if not os.path.exists(path):
            return {}
        
        self.worlds.clear()
        
        for directory in sorted(os.listdir(path)):
            full_path = os.path.join(path, directory)
            if os.path.isdir(full_path):
                self.worlds[directory] = full_path
        
        return self.worlds.copy()
    
    def get_world_path(self, world_name):
        """Get the path for a specific world"""
        return self.worlds.get(world_name)
    
    def get_current_world_path(self):
        """Get the path of the currently selected world"""
        if self.current_world_name:
            return self.worlds.get(self.current_world_name)
        return None
    
    def load_world_data(self, world_path):
        """
        Load all data for a world
        
        Args:
            world_path: Path to the world directory
            
        Returns:
            Dictionary containing inventory, attributes, and datapacks data
        """
        # Store current world
        for name, path in self.worlds.items():
            if path == world_path:
                self.current_world_name = name
                break
        
        filepath = os.path.join(world_path, "level.dat")
        nbt = NBTFile(filepath)
        player_data = nbt.openfile()
        
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
        player_file = os.path.join(world_path, "level.dat")
        forcefill_file(player_file)
    
    def save_attributes(self, world_path, attributes_data):
        """
        Save player attributes to the world
        
        Args:
            world_path: Path to the world directory
            attributes_data: Dictionary of attribute names to values
        """
        filepath = os.path.join(world_path, "level.dat")
        nbt = NBTFile(filepath)
        player_data = nbt.openfile()
        
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
        
        # Save the file
        nbt.savefile(player_data)
    
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
