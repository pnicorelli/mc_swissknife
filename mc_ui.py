import tkinter as tk
from tkinter import ttk, messagebox
import os
from pathlib import Path
from mc_read import read_player_inventory
from mc_forcefill import forcefill_file

class MinecraftSaveManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft Swiss Knife")
        self.root.geometry("800x600")
        
        # Top frame for path and refresh
        self.top_frame = tk.Frame(root, padx=10, pady=10)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Path label and entry
        tk.Label(self.top_frame, text="Save Path:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.path_var = tk.StringVar(value="~/.minecraft/saves/")
        self.path_entry = tk.Entry(self.top_frame, textvariable=self.path_var, width=50)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Refresh button
        self.refresh_btn = tk.Button(self.top_frame, text="Refresh", command=self.refresh)
        self.refresh_btn.pack(side=tk.LEFT)
        
        # Notebook (tabs) for save directories
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Bottom frame for buttons
        self.bottom_frame = tk.Frame(root, padx=10, pady=10)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Action buttons
        self.empty_btn = tk.Button(self.bottom_frame, text="Empty", 
                                   command=self.on_empty, width=15)
        self.empty_btn.pack(side=tk.LEFT, padx=5)
        
        self.fill_btn = tk.Button(self.bottom_frame, text="Fill", 
                                  command=self.on_fill, width=15)
        self.fill_btn.pack(side=tk.LEFT, padx=5)
        
        self.special_btn = tk.Button(self.bottom_frame, text="Special", 
                                     command=self.on_special, width=15)
        self.special_btn.pack(side=tk.LEFT, padx=5)
        
        # Store tabs and their listboxes
        self.tabs = {}
        
        # Initial load
        self.refresh()
    
    def refresh(self):
        """Refresh the save directories and update tabs"""
        # Clear existing tabs
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)
        self.tabs.clear()
        
        # Get the path
        path = os.path.expanduser(self.path_var.get())
        
        # Check if path exists
        if not os.path.exists(path):
            messagebox.showerror("Error", f"Path does not exist: {path}")
            return
        
        # Get all directories in the save path
        try:
            dirs = [d for d in os.listdir(path) 
                   if os.path.isdir(os.path.join(path, d))]
            dirs.sort()
            
            if not dirs:
                messagebox.showinfo("Info", "No save directories found")
                return
            
            # Create a tab for each directory
            for dir_name in dirs:
                self.create_tab(dir_name, os.path.join(path, dir_name))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read directories: {str(e)}")
    
    def create_tab(self, name, full_path):
        """Create a tab for a save directory"""
        # Create frame for this tab
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text=name)
        
        # Create listbox with scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, 
                            font=("Courier", 10))
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Store the tab info
        self.tabs[name] = {
            'frame': frame,
            'listbox': listbox,
            'path': full_path
        }
        
        # Load inventory for this save
        self.load_inventory(name)
    
    def load_inventory(self, save_name):
        """Load inventory items into the listbox"""
        listbox = self.tabs[save_name]['listbox']
        save_path = self.tabs[save_name]['path']
        
        # Clear existing items
        listbox.delete(0, tk.END)
        
        try:
            # Call your existing function to get inventory
            # Replace this with your actual function call
            inventory_items = self.get_inventory(save_path)
            
            # Add items to listbox
            for item in inventory_items:
                listbox.insert(tk.END, item)
                
        except Exception as e:
            listbox.insert(tk.END, f"Error loading inventory: {str(e)}")
    
    def get_inventory(self, save_path):
        """
        Get inventory from the player data file
        """
        # Look for level.dat in the save directory
        player_file = os.path.join(save_path, "level.dat")
        
        if not os.path.exists(player_file):
            return [f"Error: level.dat not found in {save_path}"]
        
        try:
            # Call your existing function
            items_by_slot = read_player_inventory(player_file)
            
            if not items_by_slot:
                return ["No items in inventory"]
            
            # Format the items for display
            result = []
            for slot in sorted(items_by_slot.keys()):
                item = items_by_slot[slot]
                
                # Categorize the slot
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
                    index = str(-100 - slot).replace('0', 'H').replace('1', 'C').replace('2', 'L').replace('3', 'B')
                else:
                    area = "Other"
                    index = slot
                
                result.append(f"[Slot {slot:03d} | {area: <8} {index:>2}]: {item['count']:02d}x {item['id']}")
            
            return result
            
        except Exception as e:
            return [f"Error reading inventory: {str(e)}"]
    
    def get_current_tab(self):
        """Get the currently selected tab"""
        try:
            current_tab_id = self.notebook.select()
            current_tab_text = self.notebook.tab(current_tab_id, "text")
            return current_tab_text
        except:
            return None
    
    def on_empty(self):
        """Handle Empty button click"""
        current_tab = self.get_current_tab()
        if current_tab:
            save_path = self.tabs[current_tab]['path']
            # Call your existing empty function
            # empty_inventory(save_path)
            messagebox.showinfo("Empty", f"Empty function called for: {current_tab}\nNOT IMPLEMENTED")
            self.load_inventory(current_tab)  # Refresh the display
        else:
            messagebox.showwarning("Warning", "No save selected")
    
    def on_fill(self):
        """Handle Fill button click"""
        current_tab = self.get_current_tab()
        if current_tab:
            save_path = self.tabs[current_tab]['path']
            player_file = os.path.join(save_path, "level.dat")
            forcefill_file(player_file)
            # messagebox.showinfo("Fill", f"Fill function called for: {current_tab}")
            self.load_inventory(current_tab)  # Refresh the display
        else:
            messagebox.showwarning("Warning", "No save selected")
    
    def on_special(self):
        """Handle Special button click"""
        current_tab = self.get_current_tab()
        if current_tab:
            save_path = self.tabs[current_tab]['path']
            # Call your existing special function
            # special_action(save_path)
            messagebox.showinfo("Special", f"Special function called for: {current_tab}")
            self.load_inventory(current_tab)  # Refresh the display
        else:
            messagebox.showwarning("Warning", "No save selected")

def main():
    root = tk.Tk()
    app = MinecraftSaveManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()