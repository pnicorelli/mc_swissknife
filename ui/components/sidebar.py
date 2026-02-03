"""
Sidebar Component - World selection list
"""
import tkinter as tk
from config.settings import Config


class Sidebar:
    """Sidebar with list of available Minecraft worlds"""
    
    def __init__(self, parent, on_select_callback):
        self.on_select = on_select_callback
        
        # Create sidebar frame
        self.frame = tk.Frame(
            parent,
            width=Config.SIDEBAR_WIDTH,
            relief=tk.RIDGE,
            borderwidth=1
        )
        self.frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Title
        tk.Label(
            self.frame,
            text="World List",
            font=Config.FONT_HEADING
        ).pack(pady=5)
        
        # Listbox with scrollbar
        self.world_listbox = tk.Listbox(
            self.frame,
            font=Config.FONT_NORMAL,
            borderwidth=0
        )
        self.world_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.world_listbox.bind('<<ListboxSelect>>', self._on_selection_change)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(self.frame, command=self.world_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.world_listbox.config(yscrollcommand=scrollbar.set)
        
        # Store world data
        self.worlds = {}
    
    def update_world_list(self, worlds_dict):
        """Update the list of worlds"""
        self.worlds = worlds_dict
        self.world_listbox.delete(0, tk.END)
        
        for world_name in sorted(worlds_dict.keys()):
            self.world_listbox.insert(tk.END, world_name)
    
    def _on_selection_change(self, event):
        """Handle world selection"""
        selection = self.world_listbox.curselection()
        if selection:
            world_name = self.world_listbox.get(selection[0])
            self.on_select(world_name)
    
    def get_selected_world(self):
        """Get currently selected world name"""
        selection = self.world_listbox.curselection()
        if selection:
            return self.world_listbox.get(selection[0])
        return None
