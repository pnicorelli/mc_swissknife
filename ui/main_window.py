"""
Main Window - Application Controller
Coordinates between UI components and business logic
"""
import tkinter as tk
from tkinter import messagebox
import os

from config.settings import Config
from ui.components.top_panel import TopPanel
from ui.components.sidebar import Sidebar
from ui.components.content_area import ContentArea
from core.world_manager import WorldManager


class MainWindow:
    """Main application window controller"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(Config.WINDOW_TITLE)
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        
        # Initialize world manager
        self.world_manager = WorldManager()
        
        # Create UI components
        self._create_ui()
        
        # Initial world scan
        self.refresh_worlds()
    
    def _create_ui(self):
        """Create all UI components"""
        # Top configuration panel
        self.top_panel = TopPanel(self.root, self.on_refresh_worlds)
        
        # Main container
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Sidebar with world list
        self.sidebar = Sidebar(main_container, self.on_world_select)
        
        # Content area with tabs
        self.content_area = ContentArea(
            main_container,
            on_fill=self.on_fill,
            on_save_attributes=self.on_save_attributes,
            on_datapack_toggle=self.on_datapack_toggle
        )
    
    def refresh_worlds(self):
        """Scan for Minecraft worlds"""
        path = self.top_panel.get_path()
        worlds = self.world_manager.scan_worlds(path)
        self.sidebar.update_world_list(worlds)
    
    def on_refresh_worlds(self):
        """Handler for refresh button"""
        self.refresh_worlds()
    
    def on_world_select(self, world_name):
        """Handler for world selection"""
        world_path = self.world_manager.get_world_path(world_name)
        if world_path:
            try:
                # Load world data
                world_data = self.world_manager.load_world_data(world_path)
                
                # Update all tabs
                self.content_area.update_inventory(world_data['inventory'])
                self.content_area.update_attributes(world_data['attributes'])
                self.content_area.update_datapacks(
                    world_path,
                    world_data['datapacks']
                )
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load world data: {e}")
    
    def on_fill(self):
        """Handler for force fill inventory"""
        world_path = self.world_manager.get_current_world_path()
        if world_path:
            try:
                self.world_manager.force_fill_inventory(world_path)
                # Refresh the current world view
                world_name = self.world_manager.current_world_name
                if world_name:
                    self.on_world_select(world_name)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to fill inventory: {e}")
    
    def on_save_attributes(self, attributes_data):
        """Handler for saving player attributes"""
        world_path = self.world_manager.get_current_world_path()
        if world_path:
            try:
                self.world_manager.save_attributes(world_path, attributes_data)
                messagebox.showinfo("Success", "Attributes saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save attributes: {e}")
    
    def on_datapack_toggle(self, datapack_index, is_installed):
        """Handler for datapack toggle"""
        world_path = self.world_manager.get_current_world_path()
        if world_path:
            try:
                if is_installed:
                    self.world_manager.remove_datapack(world_path, datapack_index)
                else:
                    self.world_manager.add_datapack(world_path, datapack_index)
            except Exception as e:
                messagebox.showerror("Datapack error", str(e))
