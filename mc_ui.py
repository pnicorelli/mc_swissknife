import tkinter as tk
from tkinter import ttk, messagebox
import os
from pathlib import Path

# Importing your custom logic
from mc_read import read_player_inventory
from mc_forcefill import forcefill_file

class MinecraftSwissKnife:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft Swiss Knife")
        self.root.geometry("1000x700")
        
        # Internal data storage
        self.worlds_data = {}  # Map: display_name -> full_path
        self.current_save_path = None

        self.setup_styles()
        self.create_top_panel()
        
        # Main Container (Sidebar + Content Area)
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.create_sidebar()
        self.create_content_area()

        # Initial world scan
        self.refresh_worlds()

    def setup_styles(self):
        """Configure UI styles for a modern look"""
        style = ttk.Style()
        style.configure("TNotebook", padding=2)
        style.configure("Sidebar.TFrame", background="#f0f0f0")

    def create_top_panel(self):
        """Top area for Path configuration and Connection Type"""
        top_frame = tk.LabelFrame(self.root, text=" Configuration ", padx=10, pady=10)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Minecraft Path Entry
        tk.Label(top_frame, text="Minecraft Path:").grid(row=0, column=0, sticky="w")
        default_path = os.path.expanduser("~/.minecraft/saves/")
        self.path_var = tk.StringVar(value=default_path)
        self.path_entry = tk.Entry(top_frame, textvariable=self.path_var, width=50)
        self.path_entry.grid(row=0, column=1, padx=10, sticky="ew")

        # Game Mode Selection (Local vs Multiplayer)
        tk.Label(top_frame, text="Mode:").grid(row=0, column=2, padx=(10, 5))
        self.mode_var = tk.StringVar(value="Local")
        self.mode_select = ttk.Combobox(top_frame, textvariable=self.mode_var, 
                                        values=["Local (Saves)", "Multiplayer (Server)"], 
                                        state="readonly", width=18)
        self.mode_select.grid(row=0, column=3, padx=5)

        # Refresh Button
        self.refresh_btn = tk.Button(top_frame, text="Scan Worlds", 
                                     command=self.refresh_worlds, bg="#e1e1e1")
        self.refresh_btn.grid(row=0, column=4, padx=10)
        
        top_frame.columnconfigure(1, weight=1)

    def create_sidebar(self):
        """Left sidebar displaying the list of detected worlds"""
        sidebar = tk.Frame(self.main_container, width=250, relief=tk.RIDGE, borderwidth=1)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        tk.Label(sidebar, text="World List", font=('Arial', 10, 'bold')).pack(pady=5)
        
        # Listbox with Scrollbar for world selection
        self.world_listbox = tk.Listbox(sidebar, font=("Segoe UI", 10), borderwidth=0)
        self.world_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.world_listbox.bind('<<ListboxSelect>>', self.on_world_select)
        
        sb = tk.Scrollbar(sidebar, orient=tk.VERTICAL, command=self.world_listbox.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.world_listbox.config(yscrollcommand=sb.set)

    def create_content_area(self):
        """Right area featuring tabs for Inventory and Attributes"""
        self.content_frame = tk.Frame(self.main_container)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # TAB 1: INVENTORY
        self.tab_inv = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_inv, text=" Inventory Management ")
        self.setup_inventory_tab()

        # TAB 2: ATTRIBUTES
        self.tab_attr = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_attr, text=" Player Attributes ")
        self.setup_attributes_tab()

    def setup_inventory_tab(self):
        """Internal layout for the Inventory Tab"""
        self.inv_listbox = tk.Listbox(self.tab_inv, font=("Courier", 10), borderwidth=0)
        self.inv_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Action Buttons
        btn_frame = tk.Frame(self.tab_inv, bg="white")
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
        
        tk.Button(btn_frame, text="Empty Inventory", width=15, command=self.on_empty).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Force Fill", width=15, command=self.on_fill).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Special Action", width=15, command=self.on_special).pack(side=tk.LEFT, padx=10)

    def setup_attributes_tab(self):
        """Internal layout for the Attributes Tab"""
        container = tk.Frame(self.tab_attr, bg="white", padx=20, pady=20)
        container.pack(fill=tk.BOTH, expand=True)

        # Attribute Input Fields
        self.attr_entries = {}
        fields = [("Health", "20"), ("Food Level", "20"), ("XP Level", "0"), ("Saturation", "5.0")]

        for i, (label_text, default_val) in enumerate(fields):
            tk.Label(container, text=f"{label_text}:", bg="white").grid(row=i, column=0, sticky="w", pady=8)
            entry = tk.Entry(container, width=25)
            entry.insert(0, default_val)
            entry.grid(row=i, column=1, padx=10, pady=8)
            self.attr_entries[label_text] = entry

        # Save Button for Attributes
        save_attr_btn = tk.Button(container, text="Save Attributes", bg="#2ecc71", fg="white", 
                                  font=('Arial', 10, 'bold'), command=self.on_save_attributes, padx=20)
        save_attr_btn.grid(row=len(fields), column=1, pady=30, sticky="e")

    # --- LOGIC METHODS ---

    def refresh_worlds(self):
        """Scans the directory for Minecraft saves"""
        path = os.path.expanduser(self.path_var.get())
        if not os.path.exists(path):
            messagebox.showerror("Error", f"Path not found: {path}")
            return

        self.world_listbox.delete(0, tk.END)
        self.worlds_data.clear()

        try:
            dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
            for d in sorted(dirs):
                self.world_listbox.insert(tk.END, d)
                self.worlds_data[d] = os.path.join(path, d)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to list worlds: {e}")

    def on_world_select(self, event):
        """Triggered when a world is clicked in the sidebar"""
        selection = self.world_listbox.curselection()
        if selection:
            world_name = self.world_listbox.get(selection[0])
            self.current_save_path = self.worlds_data[world_name]
            self.update_ui_for_world(world_name)

    def update_ui_for_world(self, world_name):
        """Update inventory and attributes when a world is selected"""
        self.inv_listbox.delete(0, tk.END)
        player_file = os.path.join(self.current_save_path, "level.dat")
        
        # Logic from your original script
        try:
            inventory = read_player_inventory(player_file)
            if inventory:
                for slot, data in sorted(inventory.items()):
                    self.inv_listbox.insert(tk.END, f"[Slot {slot:03d}] {data['count']}x {data['id']}")
            else:
                self.inv_listbox.insert(tk.END, "Inventory is empty.")
        except Exception as e:
            self.inv_listbox.insert(tk.END, f"Error reading data: {e}")

    def on_save_attributes(self):
        """Logic to save modified player attributes"""
        if not self.current_save_path:
            messagebox.showwarning("Warning", "Please select a world first!")
            return
        # Placeholder for NBT writing logic
        messagebox.showinfo("Actin", "Attributes saved to level.dat not implemented")

    def on_empty(self):
        """Action for Empty button"""
        if self.current_save_path:
            messagebox.showinfo("Action", "Emptying inventory...")
            self.update_ui_for_world("") # Refresh

    def on_fill(self):
        """Action for Fill button using forcefill_file logic"""
        if self.current_save_path:
            player_file = os.path.join(self.current_save_path, "level.dat")
            forcefill_file(player_file)
            self.update_ui_for_world("") # Refresh

    def on_special(self):
        """Action for Special button"""
        if self.current_save_path:
            messagebox.showinfo("Action", "Special routine triggered")

if __name__ == "__main__":
    root = tk.Tk()
    app = MinecraftSwissKnife(root)
    root.mainloop()