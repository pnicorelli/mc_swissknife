"""
Inventory Tab - Display and manage player inventory
"""
import tkinter as tk
from config.settings import Config


class InventoryTab:
    """Tab for viewing and managing player inventory"""
    
    def __init__(self, parent, on_fill_callback):
        self.on_fill = on_fill_callback
        
        # Create main frame
        self.frame = tk.Frame(parent, bg=Config.COLOR_BG_WHITE)
        
        # Inventory listbox
        self.inv_listbox = tk.Listbox(
            self.frame,
            font=Config.FONT_MONOSPACE
        )
        self.inv_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Button frame
        btn_frame = tk.Frame(self.frame, bg=Config.COLOR_BG_WHITE)
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
        
        # Force Fill button
        tk.Button(
            btn_frame,
            text="Force Fill",
            command=self.on_fill
        ).pack(side=tk.LEFT, padx=10)
    
    def update_data(self, inventory_data):
        """Update the inventory display"""
        self.inv_listbox.delete(0, tk.END)
        
        if inventory_data:
            for slot, data in sorted(inventory_data.items()):
                display_text = f"[Slot {slot:03d}] {data['count']}x {data['id']}"
                self.inv_listbox.insert(tk.END, display_text)
        else:
            self.inv_listbox.insert(tk.END, "No inventory data found.")
    
    def clear(self):
        """Clear the inventory display"""
        self.inv_listbox.delete(0, tk.END)
