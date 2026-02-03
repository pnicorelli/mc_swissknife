"""
Attributes Tab - Display and edit player attributes
"""
import tkinter as tk
from tkinter import ttk
from config.settings import Config


class AttributesTab:
    """Tab for viewing and editing player attributes"""
    
    def __init__(self, parent, on_save_callback):
        self.on_save = on_save_callback
        self.attr_entries = {}
        
        # Create main frame
        self.frame = tk.Frame(parent, bg=Config.COLOR_BG_WHITE)
        
        # Scrollable container setup
        self._create_scrollable_container()
        
        # Save button at bottom
        self._create_save_button()
    
    def _create_scrollable_container(self):
        """Create scrollable container for attribute entries"""
        # Container with scrollbar
        self.scroll_container = tk.Frame(self.frame, bg=Config.COLOR_BG_WHITE)
        self.scroll_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas for scrolling
        self.canvas = tk.Canvas(
            self.scroll_container,
            bg=Config.COLOR_BG_WHITE,
            highlightthickness=0
        )
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.scroll_container,
            orient="vertical",
            command=self.canvas.yview
        )
        
        # Frame that will hold the attribute rows
        self.dynamic_frame = tk.Frame(self.canvas, bg=Config.COLOR_BG_WHITE)
        
        # Create window in canvas
        self.canvas.create_window((0, 0), window=self.dynamic_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.scrollbar.pack(side="right", fill="y")
        
        # Update scroll region when frame size changes
        self.dynamic_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
    
    def _create_save_button(self):
        """Create the save button at the bottom"""
        btn_frame = tk.Frame(self.frame, bg=Config.COLOR_BG_LIGHT)
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        tk.Button(
            btn_frame,
            text="Save Attributes",
            bg=Config.COLOR_SUCCESS,
            fg=Config.COLOR_TEXT_WHITE,
            font=Config.FONT_HEADING,
            command=self._on_save_clicked
        ).pack(pady=10, padx=10, side=tk.RIGHT)
    
    def update_data(self, attributes_data):
        """Update the attributes display with new data"""
        # Clear existing entries
        self._clear_entries()
        
        if attributes_data:
            for i, (attr_name, value) in enumerate(attributes_data.items()):
                self._create_attribute_row(i, attr_name, value)
        else:
            tk.Label(
                self.dynamic_frame,
                text="No attributes found.",
                bg=Config.COLOR_BG_WHITE
            ).pack()
    
    def _clear_entries(self):
        """Clear all existing attribute entries"""
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()
        self.attr_entries.clear()
    
    def _create_attribute_row(self, row_index, attr_name, value):
        """Create a single attribute entry row"""
        # Label
        label = tk.Label(
            self.dynamic_frame,
            text=f"{attr_name}:",
            bg=Config.COLOR_BG_WHITE,
            font=Config.FONT_SMALL
        )
        label.grid(row=row_index, column=0, sticky="w", padx=5, pady=5)
        
        # Entry
        entry = tk.Entry(self.dynamic_frame, width=30)
        entry.insert(0, str(value))
        entry.grid(row=row_index, column=1, padx=10, pady=5)
        
        # Store reference
        self.attr_entries[attr_name] = entry
    
    def _on_save_clicked(self):
        """Handle save button click"""
        # Collect all attribute values
        attributes_data = {}
        for attr_name, entry in self.attr_entries.items():
            attributes_data[attr_name] = entry.get().strip()
        
        # Call the callback with collected data
        self.on_save(attributes_data)
    
    def clear(self):
        """Clear all attributes"""
        self._clear_entries()
