import tkinter as tk
from tkinter import ttk, messagebox
import os
from pathlib import Path
from utils.NBTFile import NBTFile

# Importing updated logic
from mc_player import read_player_inventory, read_player_attributes, write_player_attributes
from mc_forcefill import forcefill_file
from mc_datapacks import MC_DATAPACKS

class MinecraftSwissKnife:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft Swiss Knife")
        self.root.geometry("1000x700")
        
        self.worlds_data = {} 
        self.current_save_path = None

        self.setup_styles()
        self.create_top_panel()
        
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.create_sidebar()
        self.create_content_area()
        self.refresh_worlds()

    def setup_styles(self):
        style = ttk.Style()
        style.configure("TNotebook", padding=2)

    def create_top_panel(self):
        top_frame = tk.LabelFrame(self.root, text=" Configuration ", padx=10, pady=10)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        tk.Label(top_frame, text="Minecraft Path:").grid(row=0, column=0, sticky="w")
        default_path = os.path.expanduser("~/.minecraft/saves/")
        self.path_var = tk.StringVar(value=default_path)
        self.path_entry = tk.Entry(top_frame, textvariable=self.path_var, width=50)
        self.path_entry.grid(row=0, column=1, padx=10, sticky="ew")

        self.refresh_btn = tk.Button(top_frame, text="Scan Worlds", command=self.refresh_worlds)
        self.refresh_btn.grid(row=0, column=4, padx=10)
        top_frame.columnconfigure(1, weight=1)

    def create_sidebar(self):
        sidebar = tk.Frame(self.main_container, width=250, relief=tk.RIDGE, borderwidth=1)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        tk.Label(sidebar, text="World List", font=('Arial', 10, 'bold')).pack(pady=5)
        self.world_listbox = tk.Listbox(sidebar, font=("Segoe UI", 10), borderwidth=0)
        self.world_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.world_listbox.bind('<<ListboxSelect>>', self.on_world_select)
        
        sb = tk.Scrollbar(sidebar, command=self.world_listbox.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.world_listbox.config(yscrollcommand=sb.set)

    def create_content_area(self):
        self.content_frame = tk.Frame(self.main_container)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tabs
        self.tab_inv = tk.Frame(self.notebook, bg="white")
        self.tab_attr = tk.Frame(self.notebook, bg="white")
        self.tab_datapacks = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_inv, text=" Inventory ")
        self.notebook.add(self.tab_attr, text=" Attributes ")
        self.notebook.add(self.tab_datapacks, text=" Datapacks ")
        
        self.setup_inventory_tab()
        self.setup_attributes_tab()
        self.setup_datapacks_tab()

    def setup_datapacks_tab(self):
        self.datapack_tree = ttk.Treeview(
            self.tab_datapacks,
            columns=("installed",),
            show="tree headings",
            selectmode="none",
            height=8
        )

        self.datapack_tree.heading("#0", text="Datapack")
        self.datapack_tree.heading("installed", text="Installed")

        self.datapack_tree.column("#0", width=200, anchor="w")
        self.datapack_tree.column("installed", width=80, anchor="center")

        self.datapack_tree.pack(fill="both", expand=True)

        self.datapack_tree.bind("<Button-1>", self.on_datapack_click)


    def setup_inventory_tab(self):
        self.inv_listbox = tk.Listbox(self.tab_inv, font=("Courier", 10))
        self.inv_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        btn_frame = tk.Frame(self.tab_inv, bg="white")
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
        tk.Button(btn_frame, text="Force Fill", command=self.on_fill).pack(side=tk.LEFT, padx=10)

    def setup_attributes_tab(self):
        """Initializes the container for dynamic attribute rows"""
        # Main container with a scrollbar in case there are many attributes
        self.attr_scroll_container = tk.Frame(self.tab_attr, bg="white")
        self.attr_scroll_container.pack(fill=tk.BOTH, expand=True)

        self.attr_canvas = tk.Canvas(self.attr_scroll_container, bg="white", highlightthickness=0)
        self.attr_scrollbar = ttk.Scrollbar(self.attr_scroll_container, orient="vertical", command=self.attr_canvas.yview)
        
        # This frame will hold the actual rows
        self.attr_dynamic_frame = tk.Frame(self.attr_canvas, bg="white")
        
        self.attr_canvas.create_window((0, 0), window=self.attr_dynamic_frame, anchor="nw")
        self.attr_canvas.configure(yscrollcommand=self.attr_scrollbar.set)

        self.attr_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.attr_scrollbar.pack(side="right", fill="y")

        # Bind resizing to update scroll region
        self.attr_dynamic_frame.bind("<Configure>", lambda e: self.attr_canvas.configure(scrollregion=self.attr_canvas.bbox("all")))

        # Global Save Button at the bottom
        btn_frame = tk.Frame(self.tab_attr, bg="#f0f0f0")
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Button(btn_frame, text="Save Attributes", bg="#2ecc71", fg="white", 
                  font=('Arial', 10, 'bold'), command=self.on_save_attributes).pack(pady=10, padx=10, side=tk.RIGHT)

        self.attr_entries = {}

    def refresh_worlds(self):
        path = os.path.expanduser(self.path_var.get())
        if not os.path.exists(path): return
        self.world_listbox.delete(0, tk.END)
        self.worlds_data.clear()
        for d in sorted(os.listdir(path)):
            full_path = os.path.join(path, d)
            if os.path.isdir(full_path):
                self.world_listbox.insert(tk.END, d)
                self.worlds_data[d] = full_path

    def on_world_select(self, event):
        selection = self.world_listbox.curselection()
        if selection:
            world_name = self.world_listbox.get(selection[0])
            self.current_save_path = self.worlds_data[world_name]
            self.update_ui_for_world()

    def update_ui_for_world(self):
        """Refreshes both Inventory and builds dynamic Attribute rows"""
        if not self.current_save_path: return

        filepath = os.path.join(self.current_save_path, "level.dat")
        try:
            nbt = NBTFile(filepath)
            player_data = nbt.openfile()
            
            # 1. Update Inventory
            self.inv_listbox.delete(0, tk.END)
            inventory = read_player_inventory(player_data)
            if inventory:
                for slot, data in sorted(inventory.items()):
                    self.inv_listbox.insert(tk.END, f"[Slot {slot:03d}] {data['count']}x {data['id']}")
            else:
                self.inv_listbox.insert(tk.END, "No inventory data found.")

            # 2. Update Attributes (Dynamic UI Generation)
            # Clear existing rows
            for widget in self.attr_dynamic_frame.winfo_children():
                widget.destroy()
            self.attr_entries.clear()

            attributes = read_player_attributes(player_data)
            if attributes:
                for i, (attr_name, val) in enumerate(attributes.items()):
                    # Create Label
                    lbl = tk.Label(self.attr_dynamic_frame, text=f"{attr_name}:", bg="white", font=("Segoe UI", 9))
                    lbl.grid(row=i, column=0, sticky="w", padx=5, pady=5)
                    
                    # Create Entry
                    ent = tk.Entry(self.attr_dynamic_frame, width=30)
                    ent.insert(0, str(val))
                    ent.grid(row=i, column=1, padx=10, pady=5)
                    
                    # Store reference by the technical attribute name
                    self.attr_entries[attr_name] = ent
            else:
                tk.Label(self.attr_dynamic_frame, text="No attributes found.", bg="white").pack()

            # 3. Update Datapacks
            for item in self.datapack_tree.get_children():
                self.datapack_tree.delete(item)

            status = MC_DATAPACKS.checkStatus(self.current_save_path)

            for idx, dp in enumerate(status):
                checkbox = "☑" if dp["installed"] else "☐"

                self.datapack_tree.insert(
                    "",
                    "end",
                    iid=str(idx),
                    text=dp["label"],
                    values=(checkbox,)
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load world data: {e}")

    def on_fill(self):
        if self.current_save_path:
            player_file = os.path.join(self.current_save_path, "level.dat")
            forcefill_file(player_file)
            self.update_ui_for_world() # Refresh after change

    def on_save_attributes(self):
        if not self.current_save_path: return


        cleaned_data = {}
        for attr_name, entry in self.attr_entries.items():
            cleaned_data[attr_name] = entry.get().strip()
        minecraft_attributes = {k: v for k, v in cleaned_data.items() if k.startswith("minecraft:")}
        try:
            filepath = os.path.join(self.current_save_path, "level.dat")
            nbt = NBTFile(filepath)
            player_data = nbt.openfile()        
            write_player_attributes(player_data, "XpLevel", int(cleaned_data["XpLevel"]))
            write_player_attributes(player_data, "attributes", minecraft_attributes)
            nbt.savefile(player_data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load world data: {e}")

        # print(minecraft_attributes)
        # messagebox.showinfo("Note", "NBT Writing logic needs to be implemented in a separate function.")

    def on_datapack_click(self, event):
        region = self.datapack_tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        column = self.datapack_tree.identify_column(event.x)
        if column != "#1":
            return

        item = self.datapack_tree.identify_row(event.y)
        if not item:
            return

        index = int(item)
        current = self.datapack_tree.set(item, "installed")

        try:
            if current == "☐":
                MC_DATAPACKS.add(self.current_save_path, index)
                self.datapack_tree.set(item, "installed", "☑")
            else:
                MC_DATAPACKS.delete(self.current_save_path, index)
                self.datapack_tree.set(item, "installed", "☐")

        except Exception as e:
            tk.messagebox.showerror("Datapack error", str(e))
if __name__ == "__main__":
    root = tk.Tk()
    app = MinecraftSwissKnife(root)
    root.mainloop()