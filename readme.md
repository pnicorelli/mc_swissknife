## 👋 Note for Visitors: This is a teaching repository for young learners, not a unicorn project!

# 🎮 Minecraft Swiss Knife

A graphical tool to manage Minecraft save game inventories!

![Screenshot](./assets/screenshot.png)

## 📋 What This Program Does

This program opens a window where you can:
- See all your Minecraft save games
- View the inventory of each save game
- Fill your inventory with items (already working! ✅)
- Empty your inventory (not implemented yet - **your task!** 🚀)
- Apply special equipment (function exists in `mc_best_equipment.py` - **your task to connect it!** 🚀)

## 🎯 Your Mission

There are **two functions you need to complete**:

### 1. Empty Function (Missing)
The `on_empty()` function is ready, but it needs the actual empty function!
- **What it should do**: Remove all items from the player's inventory
- **Where to add it**: You need to create a new function (maybe in `read.py`?)
- **Hint**: Look at how `fill` works and do the opposite!

### 2. Special Function (Partially Done)
The `on_special()` function exists, but it's not connected!
- **What it should do**: Give the player the best equipment
- **The function already exists** in the file `mc_best_equipment.py`
- **Your task**: Import it and connect it to the button (like we did with `fill`)

## 🛠️ Installation Instructions

### Step 1: Install Git

**What is Git?** Git is a tool that helps programmers save different versions of their code and work together.

#### On Windows:
1. Download Git from: https://git-scm.com/download/win
2. Run the installer
3. Keep clicking "Next" with default options
4. Done!

#### On Mac:
1. Open Terminal (search for "Terminal" in Spotlight)
2. Type: `git --version` and press Enter
3. If not installed, it will ask you to install it. Click "Install"

#### On Linux:
Open Terminal and type:
```bash
sudo apt-get install git
```

### Step 2: Download This Project

Open Terminal (or Command Prompt on Windows) and type:

```bash
# Go to your Documents folder
cd Documents

# Download the project
git clone https://github.com/pnicorelli/mc_swissknife.git

# Enter the project folder
cd mc_swissknife
```

**What does this do?** `git clone` downloads the entire project to your computer!

### Step 3: Install Python

**What is Python?** Python is the programming language we use to write this program.

#### On Windows:
1. Go to: https://www.python.org/downloads/
2. Download Python (version 3.8 or newer)
3. **IMPORTANT**: When installing, check the box "Add Python to PATH"
4. Click "Install Now"

#### On Linux/Mac:
Probably is already there :P
If not, on Mac `brew install python`
On Linux `sudo apt install python`

To check if Python is installed, open Terminal and type:
```bash
python --version
```

You should see something like: `Python 3.12.0`

### Step 4: Create a Virtual Environment

**What is a virtual environment?** It's like a separate box for your project where you install libraries. This way, different projects don't mix up their libraries!

In Terminal, inside your project folder, type:

```bash
# Create the virtual environment
python -m venv mc_env

# Activate it (Windows)
mc_env\Scripts\activate

# Activate it (Mac/Linux)
source mc_env/bin/activate
```

**How to know it's activated?** You'll see `(mc_env)` at the beginning of your terminal line!

### Step 5: Install Required Libraries

**What are libraries?** They are pieces of code that other people wrote, so we don't have to write everything from scratch!

```bash
# Make sure mc_env is activated (you should see (mc_env) in terminal)
pip install -r requirements.txt
```

**What does this do?** It installs all the libraries listed in `requirements.txt` (like `nbtlib` for reading Minecraft files and `tkinter` for the window).

### Step 6: Run the Program!

```bash
python mc_ui.py
```
A window should open! 🎉


**Finding Your Minecraft Saves:**

On Linux, Minecraft saves your worlds in `/home/{myuser}/.minecraft/saves/`. You can change this location in the UI or directly in the code. Linux and Mac have `~` as shortcut for `/home/{myuser}/`

**⚠️ IMPORTANT: Player Data Location**

The player data file is in different places depending on how you play:

- **Single-player games**: `/saves/{worldname}/level.dat`
- **Multiplayer/LAN games**: `/saves/{worldname}/playerdata/{UUID}.dat`

Make sure you're pointing to the correct file type for your game!


## 📚 Learning Git - Basic Commands

You can use Git from many different apps, I prefer the terminal because I was born thousands of years ago.

Here are the most important Git commands you'll use:

### See What Changed
```bash
git status
```
This shows you which files you modified.

### Save Your Changes

```bash
# Step 1: Add files you want to save
git add .

# Step 2: Save them with a message
git commit -m "I added the empty function!"

# Step 3: Upload to GitHub
git push
```

**What's happening?**
- `git add .` = "I want to save ALL the files I changed"
- `git commit` = "Save these changes with a description"
- `git push` = "Upload my changes to GitHub so others can see"

### Download New Changes
```bash
git pull
```
This downloads changes that others made!

### Create Your Own Version (Branch)
```bash
# Create a new branch
git checkout -b my-new-feature

# Work on your code...

# When done, go back to main
git checkout main
```

**Why branches?** You can experiment without breaking the working code!

## 🐍 Understanding Python Basics

### Files in This Project

- **`mc_gui.py`** - The main file with the window
- **`mc_read.py`** - Functions to read Minecraft save files
- **`mc_forcefill.py`** - Functions to fill Inventory
- **`mc_best_equipment.py`** - Function for special equipment
- **`requirements.txt`** - List of libraries we need

### How to Read Python Code

```python
# This is a comment - Python ignores it

# This is a function - it does something
def my_function(parameter):
    result = parameter + 10
    return result

# This calls the function
answer = my_function(5)  # answer will be 15
```

### Important Concepts

**Variables** - Boxes that store values:
```python
player_name = "Steve"
health = 20
```

**Functions** - Recipes that do something:
```python
def add_numbers(a, b):
    return a + b

result = add_numbers(5, 3)  # result is 8
```

**Importing** - Using code from other files:
```python
from read import read_player_inventory
```

## 🎓 Tips for Learning

1. **Don't be afraid to break things!** That's how you learn. You can always use `git` to go back.
2. **Read error messages carefully** - They tell you what's wrong!
3. **Google is your friend** - Programmers Google things ALL THE TIME
4. **Ask questions** - There are no stupid questions in programming
5. **Start small** - Try changing just one thing at a time

## 🚀 Your First Tasks

Here's what you can try:

### Easy Tasks:
1. Change the window title to something fun
2. Change the button colors
3. Add a new button (even if it does nothing yet)

### Medium Tasks:
1. Implement the `empty` function
2. Connect the `special` function from `mc_best_equipment.py`
3. Add a status message at the bottom of the window

### Hard Tasks:
1. Add a search box to filter inventory items
2. Add the ability to add/remove specific items
3. Create a backup before making changes

## 📖 Useful Resources

- **Python Tutorial**: https://www.w3schools.com/python/
- **Git Tutorial**: https://www.atlassian.com/git/tutorials
- **Tkinter (GUI) Tutorial**: https://realpython.com/python-gui-tkinter/
- **Minecraft NBT Format**: https://minecraft.wiki/w/NBT_format

## 🤝 Contributing

When you add a new feature:

1. Create a branch: `git checkout -b my-feature`
2. Write your code
3. Test it!
4. Commit: `git commit -m "Added my feature"`
5. Push: `git push origin my-feature`

## ❓ Common Problems

**Problem**: "python command not found"
- **Solution**: Make sure you checked "Add to PATH" when installing Python

**Problem**: "No module named 'nbtlib'"
- **Solution**: Activate mc_env and run `pip install -r requirements.txt`

**Problem**: "Permission denied"
- **Solution**: On Mac/Linux, you might need to use `python3` instead of `python`

**Problem**: The window doesn't open
- **Solution**: Make sure you're in the right folder and mc_env is activated

## 🎉 Have Fun!

Programming is like solving puzzles. Sometimes it's frustrating, but when it works, it feels amazing!

**Remember #1**: Every programmer was a beginner once. You can do this! 💪

**Remember #2**: Programmers write code in English - variable names, comments, everything! It's the universal language of code, so let's practice it here together. 🌍

---

**Questions?** If you have an accout here open an "Issue" or ask me somewhere in someway! 😊