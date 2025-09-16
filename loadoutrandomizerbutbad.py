import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

# This is for the classes in the game
CLASSES = {
    "Soldat": {"base_weight": 3, "auto_equip": []},
    "Rook": {"base_weight": 2, "auto_equip": []},
    "Mortician": {"base_weight": 2, "auto_equip": []},
    "Officer": {"base_weight": 2, "auto_equip": []},
    "Lancer": {"base_weight": 2, "auto_equip": ["Heavy Lance"]},
    "Vanguard": {"base_weight": 2, "auto_equip": ["Shield"]},
}

# All the perks you can get
PERKS = [
    "Survivalist", 
    "Greyhound", 
    "Hippocratic", 
    "Apparition",
    "Butcher", 
    "Chemist", 
    "Tunnel Rat", 
    "Ambidextrous", 
    "Leatherneck",
    "Marksman", 
    "Snake Eyes", 
    "Devil Dog", 
    "Veteran", 
    "Black Hand",
]

# Big guns
PRIMARY_WEAPONS = {
    "Prince": 2, 
    "Adjudicator": 2, 
    "Kingslayer": 2, 
    "Whisper": 2,
    "Flyboy Whisper": 2, 
    "Volk": 2, 
    "Frontline Volk": 2, 
    "Judgement": 2,
    "Incendiary Judgement": 2, 
    "Equine": 2, 
    "Sawn-Off Equine": 2,
    "Crestfall": 2, 
    "Ranger Crestfall": 2, 
    "Hellion": 2, 
    "Heavy Hellion": 2,
    "Jesse": 2, 
    "Precision Jesse": 2, 
    "Stocked Union": 2, 
    "Cavalry Talon": 2,
    "Heavy Lance": 2,
}

# Small guns
SECONDARY_WEAPONS = {
    "Grace": 1, 
    "Honour": 1, 
    "Talon": 1, 
    "Cavalry Sword": 1, 
    "Negotiator": 1,
    "Knell": 1, 
    "Bandit Knell": 1, 
    "Hope": 1, 
    "Union": 1, 
    "Auclair": 1, 
    "Shield": 1,
}

# This class handles the pictures
class ImageManager:
    def __init__(self):
        self.images = {}
        self.icon_size = (24, 24)
        self.placeholder_image = None
        self.make_placeholder_image()
    
    def make_placeholder_image(self):
        # Makes a gray square if no image is found
        img = Image.new('RGBA', self.icon_size, (128, 128, 128, 255))
        self.placeholder_image = ImageTk.PhotoImage(img)
    
    def load_image(self, name):
        if name in self.images:
            return self.images[name]
        
        file_name = f"{name}.png"
        try:
            if os.path.exists(file_name):
                img = Image.open(file_name)
                img = img.resize(self.icon_size, Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.images[name] = photo
                return photo
            else:
                self.images[name] = self.placeholder_image
                return self.placeholder_image
        except Exception as e:
            print(f"Oops! Couldn't load image for {name}: {e}")
            self.images[name] = self.placeholder_image
            return self.placeholder_image

# This function makes a random loadout
def generate_random_loadout():
    # Pick a random class
    class_names = list(CLASSES.keys())
    chosen_class = random.choice(class_names)
    class_info = CLASSES[chosen_class]
    
    # Pick a random perk
    chosen_perk = random.choice(PERKS)
    
    # Figure out max weight
    max_weight = class_info["base_weight"]
    if chosen_perk == "Survivalist":
        max_weight = max_weight + 1
    
    # Start with auto equip items
    loadout = []
    weight_used = 0
    
    for item in class_info["auto_equip"]:
        loadout.append(item)
        if item in PRIMARY_WEAPONS:
            weight_used += PRIMARY_WEAPONS[item]
        elif item in SECONDARY_WEAPONS:
            weight_used += SECONDARY_WEAPONS[item]
    
    # Make lists of weapons we can choose from
    primaries = list(PRIMARY_WEAPONS.keys())
    secondaries = list(SECONDARY_WEAPONS.keys())
    
    # Remove weapons that are class-specific if not that class
    if chosen_class != "Lancer":
        if "Heavy Lance" in primaries:
            primaries.remove("Heavy Lance")
    
    if chosen_class != "Vanguard":
        if "Shield" in secondaries:
            secondaries.remove("Shield")
    
    # Remove weapons that are already auto-equipped
    for weapon in loadout:
        if weapon in primaries:
            primaries.remove(weapon)
        if weapon in secondaries:
            secondaries.remove(weapon)
    
    # Keep adding weapons until we have 2 or can't add more
    while len(loadout) < 2:
        weight_left = max_weight - weight_used
        
        # What can we add?
        choices = []
        if weight_left >= 2 and len(primaries) > 0:
            choices.append('primary')
        if weight_left >= 1 and len(secondaries) > 0:
            choices.append('secondary')
        
        if len(choices) == 0:
            break  # Can't add anything else
        
        # Randomly pick what type to add
        pick = random.choice(choices)
        
        if pick == 'primary':
            weapon = random.choice(primaries)
            loadout.append(weapon)
            weight_used += PRIMARY_WEAPONS[weapon]
            primaries.remove(weapon)
        elif pick == 'secondary':
            weapon = random.choice(secondaries)
            loadout.append(weapon)
            weight_used += SECONDARY_WEAPONS[weapon]
            secondaries.remove(weapon)
    
    # Return everything we figured out
    return {
        "class": chosen_class,
        "perk": chosen_perk,
        "max_weight": max_weight,
        "loadout": loadout,
        "total_weight": weight_used,
    }

# This is the main app window
class LoadoutRandomizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Loadout Randomizer")
        self.root.geometry("450x500")
        self.root.resizable(False, False)
        
        self.image_manager = ImageManager()

        # Make it look cool
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure("TFrame", background="#2e2e2e")
        style.configure("TLabel", background="#2e2e2e", foreground="#f0f0f0", font=("Segoe UI", 11))
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"))
        style.configure("TButton", font=("Segoe UI", 12, "bold"), padding=10)

        # Main frame that holds everything
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)

        # Title at the top
        title_label = ttk.Label(main_frame, text="Your Random Loadout", style="Title.TLabel")
        title_label.pack(pady=(0, 20))

        # Class display
        self.class_frame = ttk.Frame(main_frame)
        self.class_frame.pack(fill="x", pady=2)
        class_text = ttk.Label(self.class_frame, text="Class:", style="Header.TLabel")
        class_text.pack(side="left")
        self.class_icon_label = ttk.Label(self.class_frame)
        self.class_icon_label.pack(side="left", padx=(5, 2))
        self.class_text_label = ttk.Label(self.class_frame)
        self.class_text_label.pack(side="left", padx=3)

        # Perk display
        self.perk_frame = ttk.Frame(main_frame)
        self.perk_frame.pack(fill="x", pady=2)
        perk_text = ttk.Label(self.perk_frame, text="Perk:", style="Header.TLabel")
        perk_text.pack(side="left")
        self.perk_icon_label = ttk.Label(self.perk_frame)
        self.perk_icon_label.pack(side="left", padx=(5, 2))
        self.perk_text_label = ttk.Label(self.perk_frame)
        self.perk_text_label.pack(side="left", padx=3)
        
        # Max weight display
        self.max_weight_var = tk.StringVar()
        self.make_info_row(main_frame, "Max Weight:", self.max_weight_var)

        # A line to separate things
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill='x', pady=15)

        # Weapons title
        weapons_title = ttk.Label(main_frame, text="Weapons:", style="Header.TLabel")
        weapons_title.pack(anchor="w")
        
        # Frame for weapons
        self.weapons_frame = ttk.Frame(main_frame)
        self.weapons_frame.pack(fill="x", pady=(5, 15))

        # Total weight display
        self.total_weight_var = tk.StringVar()
        weight_label = ttk.Label(main_frame, textvariable=self.total_weight_var, font=("Segoe UI", 11, "italic"))
        weight_label.pack(pady=(10, 0))

        # The button to make a new loadout
        self.generate_button = ttk.Button(
            main_frame,
            text="Generate New Loadout",
            command=self.update_screen,
            style="TButton"
        )
        self.generate_button.pack(pady=20, fill="x")

        # Show the first loadout
        self.update_screen()

    def make_info_row(self, parent, label_text, string_var):
        row_frame = ttk.Frame(parent)
        row_frame.pack(fill="x", pady=2)
        label = ttk.Label(row_frame, text=label_text, style="Header.TLabel")
        label.pack(side="left")
        value_label = ttk.Label(row_frame, textvariable=string_var)
        value_label.pack(side="left", padx=5)

    def make_weapon_row(self, parent, weapon_name, weapon_type):
        weapon_frame = ttk.Frame(parent)
        weapon_frame.pack(fill="x", pady=1, anchor="w")
        
        text = f"- {weapon_name} ({weapon_type})"
        label = ttk.Label(weapon_frame, text=text)
        label.pack(side="left", padx=(10, 0))

    def update_screen(self):
        loadout = generate_random_loadout()

        # Update class
        class_name = loadout['class']
        class_pic = self.image_manager.load_image(class_name)
        self.class_icon_label.configure(image=class_pic)
        self.class_icon_label.image = class_pic
        self.class_text_label.configure(text=class_name)

        # Update perk
        perk_name = loadout['perk']
        perk_pic = self.image_manager.load_image(perk_name)
        self.perk_icon_label.configure(image=perk_pic)
        self.perk_icon_label.image = perk_pic
        self.perk_text_label.configure(text=perk_name)

        # Update weights
        self.max_weight_var.set(str(loadout['max_weight']))
        self.total_weight_var.set(f"Total Weight Used: {loadout['total_weight']} / {loadout['max_weight']}")

        # Clear old weapons
        for widget in self.weapons_frame.winfo_children():
            widget.destroy()

        # Add new weapons
        if len(loadout['loadout']) == 0:
            no_weapons = ttk.Label(self.weapons_frame, text="- None")
            no_weapons.pack(anchor="w", padx=10)
        else:
            for weapon in loadout['loadout']:
                if weapon in PRIMARY_WEAPONS:
                    weapon_type = "Primary"
                else:
                    weapon_type = "Secondary"
                self.make_weapon_row(self.weapons_frame, weapon, weapon_type)

# Start the program
if __name__ == "__main__":
    window = tk.Tk()
    app = LoadoutRandomizerApp(window)
    window.mainloop()