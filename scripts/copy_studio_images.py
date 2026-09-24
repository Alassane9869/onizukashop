import os
import shutil

ARTIFACT_DIR = r"C:\Users\a\.gemini\antigravity-ide\brain\ae1a582c-2bf0-4e09-8b46-bac4cae90a35"
MEDIA_DIR = r"c:\Censure\OnizoukShop\media\products"

files_to_copy = [
    ("studio_coffee_machine_1790146718784.jpg", "studio_espresso_coffee.jpg"),
    ("studio_microwave_black_mirror_1790146740162.jpg", "studio_microwave_inverter.jpg"),
    ("studio_food_processor_1790146761504.jpg", "studio_food_processor.jpg"),
    ("fridge_studio_samsung_1790116051075.jpg", "samsung_flagship_fridge.jpg"),
    ("ac_studio_midea_1790116068754.jpg", "midea_flagship_ac.jpg"),
]

for src_name, dest_name in files_to_copy:
    src_path = os.path.join(ARTIFACT_DIR, src_name)
    dest_path = os.path.join(MEDIA_DIR, dest_name)
    if os.path.exists(src_path):
        shutil.copyfile(src_path, dest_path)
        print(f"Copied {src_name} -> {dest_name} ({os.path.getsize(dest_path)} bytes)")
    else:
        print(f"Not found: {src_path}")
