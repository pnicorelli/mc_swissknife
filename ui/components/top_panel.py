"""
Top Panel Component - Configuration controls
"""
import tkinter as tk
from config.settings import Config


class TopPanel:
    """Top configuration panel with Minecraft path and refresh button"""
    
    def __init__(self, parent, on_refresh_callback):
        self.on_refresh = on_refresh_callback
        
        # Create frame
        self.frame = tk.LabelFrame(
            parent,
            text=" Configuration ",
            padx=10,
            pady=10
        )
        self.frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        # Path label
        tk.Label(self.frame, text="Minecraft Path:").grid(
            row=0, column=0, sticky="w"
        )
        
        # Path entry
        self.path_var = tk.StringVar(value=Config.DEFAULT_MINECRAFT_PATH)
        self.path_entry = tk.Entry(
            self.frame,
            textvariable=self.path_var,
            width=50
        )
        self.path_entry.grid(row=0, column=1, padx=10, sticky="ew")
        
        # Refresh button
        self.refresh_btn = tk.Button(
            self.frame,
            text="Scan Worlds",
            command=self.on_refresh
        )
        self.refresh_btn.grid(row=0, column=4, padx=10)
        
        # Configure column weight for resizing
        self.frame.columnconfigure(1, weight=1)
    
    def get_path(self):
        """Get the current Minecraft path"""
        return self.path_var.get()
    
    def set_path(self, path):
        """Set the Minecraft path"""
        self.path_var.set(path)
