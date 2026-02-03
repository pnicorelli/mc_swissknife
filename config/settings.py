"""
Application Configuration
"""
import os


class Config:
    """Application configuration constants"""
    
    # Window settings
    WINDOW_TITLE = "Minecraft Swiss Knife"
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 700
    
    # Paths
    DEFAULT_MINECRAFT_PATH = os.path.expanduser("~/.minecraft/saves/")
    
    # UI Settings
    SIDEBAR_WIDTH = 250
    
    # Fonts
    FONT_HEADING = ('Arial', 10, 'bold')
    FONT_NORMAL = ("Segoe UI", 10)
    FONT_MONOSPACE = ("Courier", 10)
    FONT_SMALL = ("Segoe UI", 9)
    
    # Colors
    COLOR_BG_WHITE = "white"
    COLOR_BG_LIGHT = "#f0f0f0"
    COLOR_SUCCESS = "#2ecc71"
    COLOR_TEXT_WHITE = "white"
    
    # Tab names
    TAB_INVENTORY = " Inventory "
    TAB_ATTRIBUTES = " Attributes "
    TAB_DATAPACKS = " Datapacks "
    
    # Datapack symbols
    SYMBOL_CHECKED = "☑"
    SYMBOL_UNCHECKED = "☐"
