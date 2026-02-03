"""
Datapacks Tab - Manage Minecraft datapacks
"""
import tkinter as tk
from tkinter import ttk
from config.settings import Config


class DatapacksTab:
    """Tab for managing Minecraft datapacks"""
    
    def __init__(self, parent, on_toggle_callback):
        self.on_toggle = on_toggle_callback
        self.current_world_path = None
        
        # Create main frame
        self.frame = tk.Frame(parent, bg=Config.COLOR_BG_WHITE)
        
        # Create treeview for datapacks
        self._create_treeview()
    
    def _create_treeview(self):
        """Create the treeview widget for datapacks"""
        self.tree = ttk.Treeview(
            self.frame,
            columns=("installed",),
            show="tree headings",
            selectmode="none",
            height=8
        )
        
        # Configure columns
        self.tree.heading("#0", text="Datapack")
        self.tree.heading("installed", text="Installed")
        
        self.tree.column("#0", width=200, anchor="w")
        self.tree.column("installed", width=80, anchor="center")
        
        self.tree.pack(fill="both", expand=True)
        
        # Bind click event
        self.tree.bind("<Button-1>", self._on_tree_click)
    
    def update_data(self, world_path, datapacks_status):
        """Update the datapacks display"""
        self.current_world_path = world_path
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add datapacks
        for idx, datapack in enumerate(datapacks_status):
            checkbox = Config.SYMBOL_CHECKED if datapack["installed"] else Config.SYMBOL_UNCHECKED
            
            self.tree.insert(
                "",
                "end",
                iid=str(idx),
                text=datapack["label"],
                values=(checkbox,)
            )
    
    def _on_tree_click(self, event):
        """Handle click on treeview"""
        # Check if click is in a cell
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        
        # Check if click is in the installed column
        column = self.tree.identify_column(event.x)
        if column != "#1":  # #1 is the "installed" column
            return
        
        # Get clicked item
        item = self.tree.identify_row(event.y)
        if not item:
            return
        
        # Get current state
        index = int(item)
        current_state = self.tree.set(item, "installed")
        is_installed = (current_state == Config.SYMBOL_CHECKED)
        
        # Call toggle callback
        self.on_toggle(index, is_installed)
        
        # Update display
        new_symbol = Config.SYMBOL_UNCHECKED if is_installed else Config.SYMBOL_CHECKED
        self.tree.set(item, "installed", new_symbol)
    
    def clear(self):
        """Clear all datapacks"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.current_world_path = None
