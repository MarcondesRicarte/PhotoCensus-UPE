import os
import sys

GROUP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(GROUP_DIR, "..", "..", "kit"))
from black_box import list_folders, list_photos, detect


# ==========================================
#    DATASET LOADING & CONFIDENCE FILTER
# ==========================================

def load_dataset():
    """
    Load all photos from all folders once at startup.
    Returns the results dictionary {photo_path: [(class_name, confidence), ...]}
    along with folder, photo, and raw detection counts.
    """
    results = {}
    folders = list_folders()
    total_photos_count = 0
    total_detections_count = 0

    for folder in folders:
        photos = list_photos(folder)

        for photo in photos:
            detections = detect(photo)
            results[photo] = detections
            total_photos_count += 1
            total_detections_count += len(detections)

    return results, len(folders), total_photos_count, total_detections_count


def filter_detections(detections, min_conf):
    """
    Return a new list with only (class_name, confidence) tuples >= min_conf.
    """
    filtered = []

    for class_name, confidence in detections:

        if confidence >= min_conf:
            filtered.append((class_name, confidence))

    return filtered


# ==========================================
#   INVENTORY (CLASS COUNT DICTIONARY)
# ==========================================

def build_inventory(results, min_conf, target_folder=""):
    """
    Build {class_name: amount} for the whole dataset or a specific folder.
    """
    inventory = {}

    for photo, detecions in results.items():
        folder_name = os.path.basename(os.path.dirname(photo))

        if target_folder != "" and folder_name != target_folder:
            pass

        else:
            filtered = filter_detections(detecions, min_conf)

            for class_name, _ in filtered:

                if class_name in inventory:
                    inventory[class_name] += 1

                else:
                    inventory[class_name] = 1

    return inventory
# ==========================================
#    REVERSE INDEX & FOLDER SEARCH
# ==========================================
def build_reverse_index(results, min_conf):
    """
    Build a {class_name: [photos]} dictionary filtered by min_conf, with no duplicate photos.
    """

    reverse_index = {}  

    for photo, detections in results.items():
        filtered = filter_detections(detections, min_conf)

        for class_name, _ in filtered:
    
            if class_name in reverse_index:
                if photo not in reverse_index[class_name]:
                    reverse_index[class_name] += [photo]
            
            else:
                reverse_index[class_name] = [photo]
    return reverse_index


def search_class_in_folder(folder, class_name, min_conf):
    results_class_in_folder = {}
    for photo in list_photos(folder):
        results_class_in_folder[photo] = detect(photo)

    reverse_index = build_reverse_index(results_class_in_folder, min_conf)
    photos = reverse_index.get(class_name, [])

    if photos:
        print(f"Photos with {class_name} in folder {folder}:")
        for photo in photos:
            print(f"- {photo}")
    else:
        print(f"No photos with {class_name} found in folder{folder}.")

