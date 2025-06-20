import os
import sys
import random

# === Helper: Get absolute path to bundled or local asset ===
def get_asset_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# === Load all sprite image paths into a dictionary ===
def load_sprite_variants():
    sprite_folder = get_asset_path("assets/sprites")
    sprite_dict = {}

    for filename in os.listdir(sprite_folder):
        if filename.endswith((".png", ".gif", ".jpg")):
            sprite_name = os.path.splitext(filename)[0]
            sprite_path = os.path.join(sprite_folder, filename)
            sprite_dict[sprite_name] = sprite_path

    return sprite_dict

# === Return a sprite path based on detected mood ===
def get_sprite_for_mood(mood, sprite_dict):
    matching_sprites = [
        path for name, path in sprite_dict.items()
        if name.startswith(mood)
    ]

    if matching_sprites:
        return random.choice(matching_sprites)
    else:
        return get_asset_path("assets/sprites/error.png")
