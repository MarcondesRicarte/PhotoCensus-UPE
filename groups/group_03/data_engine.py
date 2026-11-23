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