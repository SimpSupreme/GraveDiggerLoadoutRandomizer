import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

CLASSES = {
    "Soldat": {"base_weight": 3, "auto_equip": []},
    "Rook": {"base_weight": 2, "auto_equip": []},
    "Mortician": {"base_weight": 2, "auto_equip": []},
    "Officer": {"base_weight": 2, "auto_equip": []},
    "Lancer": {"base_weight": 2, "auto_equip": ["Heavy Lance"]},
    "Vanguard": {"base_weight": 2, "auto_equip": ["Shield"]},
}

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

class ImageManager:
    def __init__(self):
        self.images = {}
        self.icon_size = (24, 24)
        self.placeholder_image = None
        self.create_placeholder()

    def create_placeholder(self):
        placeholder = Image.new('RGBA', self.icon_size, (128, 128, 128, 255))
        self.placeholder_image = ImageTk.PhotoImage(placeholder)

    def load_image(self, item_name):
        if item_name in self.images:
            return self.images[item_name]
        
        filename = f"{item_name}.png"
        try:
            if os.path.exists(filename):
                image = Image.open(filename)
                image = image.resize(self.icon_size, Image.Resampling.LANCZOS)
                photo_image = ImageTk.PhotoImage(image)
                self.images[item_name] = photo_image
                return photo_image
            else:
                self.images[item_name] = self.placeholder_image
                return self.placeholder_image
        except Exception as e:
            print(f"Error loading image for {item_name}: {e}")
            self.images[item_name] = self.placeholder_image
            return self.placeholder_image

def generate_random_loadout():
    chosen_class_name = random.choice(list(CLASSES.keys()))
    chosen_class_info = CLASSES[chosen_class_name]
    chosen_perk = random.choice(PERKS)

    max_weight = chosen_class_info["base_weight"]
    if chosen_perk == "Survivalist":
        max_weight += 1

    loadout = []
    current_weight = 0
    for item in chosen_class_info["auto_equip"]:
        loadout.append(item)
        if item in PRIMARY_WEAPONS:
            current_weight += PRIMARY_WEAPONS[item]
        elif item in SECONDARY_WEAPONS:
            current_weight += SECONDARY_WEAPONS[item]

    primaries_pool = list(PRIMARY_WEAPONS.keys())
    secondaries_pool = list(SECONDARY_WEAPONS.keys())

    if chosen_class_name != "Lancer":
        primaries_pool.remove("Heavy Lance")
    
    if chosen_class_name != "Vanguard":
        secondaries_pool.remove("Shield")

    available_primaries = [w for w in primaries_pool if w not in loadout]
    available_secondaries = [w for w in secondaries_pool if w not in loadout]
    
    while len(loadout) < 2:
        remaining_weight = max_weight - current_weight
        possible_choices = []
        
        if remaining_weight >= 2 and available_primaries:
            possible_choices.append('primary')
        if remaining_weight >= 1 and available_secondaries:
            possible_choices.append('secondary')
        
        if not possible_choices:
            break

        choice_type = random.choice(possible_choices)
        if choice_type == 'primary':
            weapon = random.choice(available_primaries)
            loadout.append(weapon)
            current_weight += PRIMARY_WEAPONS[weapon]
            available_primaries.remove(weapon)
        elif choice_type == 'secondary':
            weapon = random.choice(available_secondaries)
            loadout.append(weapon)
            current_weight += SECONDARY_WEAPONS[weapon]
            available_secondaries.remove(weapon)

    return {
        "class": chosen_class_name,
        "perk": chosen_perk,
        "max_weight": max_weight,
        "loadout": loadout,
        "total_weight": current_weight,
    }

class LoadoutRandomizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Loadout Randomizer")
        self.root.geometry("450x500")
        self.root.resizable(False, False)
        
        self.image_manager = ImageManager()

        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure("TFrame", background="#2e2e2e")
        style.configure("TLabel", background="#2e2e2e", foreground="#f0f0f0", font=("Segoe UI", 11))
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"))
        style.configure("TButton", font=("Segoe UI", 12, "bold"), padding=10)

        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Your Random Loadout", style="Title.TLabel").pack(pady=(0, 20))

        self.class_frame = ttk.Frame(main_frame)
        self.class_frame.pack(fill="x", pady=2)
        ttk.Label(self.class_frame, text="Class:", style="Header.TLabel").pack(side="left")
        self.class_icon_label = ttk.Label(self.class_frame)
        self.class_icon_label.pack(side="left", padx=(5, 2))
        self.class_text_label = ttk.Label(self.class_frame)
        self.class_text_label.pack(side="left", padx=3)

        self.perk_frame = ttk.Frame(main_frame)
        self.perk_frame.pack(fill="x", pady=2)
        ttk.Label(self.perk_frame, text="Perk:", style="Header.TLabel").pack(side="left")
        self.perk_icon_label = ttk.Label(self.perk_frame)
        self.perk_icon_label.pack(side="left", padx=(5, 2))
        self.perk_text_label = ttk.Label(self.perk_frame)
        self.perk_text_label.pack(side="left", padx=3)
        
        self.max_weight_var = tk.StringVar()
        self.create_info_row(main_frame, "Max Weight:", self.max_weight_var)

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=15)

        ttk.Label(main_frame, text="Weapons:", style="Header.TLabel").pack(anchor="w")
        
        self.weapons_frame = ttk.Frame(main_frame)
        self.weapons_frame.pack(fill="x", pady=(5, 15))

        self.total_weight_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.total_weight_var, font=("Segoe UI", 11, "italic")).pack(pady=(10, 0))

        self.generate_button = ttk.Button(
            main_frame,
            text="Generate New Loadout",
            command=self.update_loadout_display,
            style="TButton"
        )
        self.generate_button.pack(pady=20, fill="x")

        self.update_loadout_display()

    def create_info_row(self, parent, label_text, string_var):
        row_frame = ttk.Frame(parent)
        row_frame.pack(fill="x", pady=2)
        ttk.Label(row_frame, text=label_text, style="Header.TLabel").pack(side="left")
        ttk.Label(row_frame, textvariable=string_var).pack(side="left", padx=5)

    def create_weapon_row(self, parent, weapon_name, weapon_type):
        weapon_frame = ttk.Frame(parent)
        weapon_frame.pack(fill="x", pady=1, anchor="w")
        
        weapon_text = f"- {weapon_name} ({weapon_type})"
        text_label = ttk.Label(weapon_frame, text=weapon_text)
        text_label.pack(side="left", padx=(10, 0))

    def update_loadout_display(self):
        loadout_data = generate_random_loadout()

        class_name = loadout_data['class']
        class_icon = self.image_manager.load_image(class_name)
        self.class_icon_label.configure(image=class_icon)
        self.class_icon_label.image = class_icon
        self.class_text_label.configure(text=class_name)

        perk_name = loadout_data['perk']
        perk_icon = self.image_manager.load_image(perk_name)
        self.perk_icon_label.configure(image=perk_icon)
        self.perk_icon_label.image = perk_icon
        self.perk_text_label.configure(text=perk_name)

        self.max_weight_var.set(str(loadout_data['max_weight']))
        self.total_weight_var.set(f"Total Weight Used: {loadout_data['total_weight']} / {loadout_data['max_weight']}")

        for widget in self.weapons_frame.winfo_children():
            widget.destroy()

        if not loadout_data['loadout']:
            ttk.Label(self.weapons_frame, text="- None").pack(anchor="w", padx=10)
        else:
            for weapon in loadout_data['loadout']:
                w_type = "Primary" if weapon in PRIMARY_WEAPONS else "Secondary"
                self.create_weapon_row(self.weapons_frame, weapon, w_type)

if __name__ == "__main__":
    app_root = tk.Tk()
    app = LoadoutRandomizerApp(app_root)
    app_root.mainloop()