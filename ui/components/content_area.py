"""
Content Area Component - Main tabbed interface
"""
import tkinter as tk
from tkinter import ttk
from config.settings import Config
from ui.tabs.inventory_tab import InventoryTab
from ui.tabs.attributes_tab import AttributesTab
from ui.tabs.datapacks_tab import DatapacksTab


class ContentArea:
    """Main content area with tabbed interface"""
    
    def __init__(self, parent, on_fill, on_save_attributes, on_datapack_toggle):
        # Create content frame
        self.frame = tk.Frame(parent)
        self.frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Setup styles
        self._setup_styles()
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.inventory_tab = InventoryTab(self.notebook, on_fill)
        self.attributes_tab = AttributesTab(self.notebook, on_save_attributes)
        self.datapacks_tab = DatapacksTab(self.notebook, on_datapack_toggle)
        
        # Add tabs to notebook
        self.notebook.add(self.inventory_tab.frame, text=Config.TAB_INVENTORY)
        self.notebook.add(self.attributes_tab.frame, text=Config.TAB_ATTRIBUTES)
        self.notebook.add(self.datapacks_tab.frame, text=Config.TAB_DATAPACKS)
    
    def _setup_styles(self):
        """Configure notebook styles"""
        style = ttk.Style()
        style.configure("TNotebook", padding=2)
    
    def update_inventory(self, inventory_data):
        """Update inventory tab with new data"""
        self.inventory_tab.update_data(inventory_data)
    
    def update_attributes(self, attributes_data):
        """Update attributes tab with new data"""
        self.attributes_tab.update_data(attributes_data)
    
    def update_datapacks(self, world_path, datapacks_status):
        """Update datapacks tab with new data"""
        self.datapacks_tab.update_data(world_path, datapacks_status)
