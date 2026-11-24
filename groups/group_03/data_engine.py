import os
from black_box import *


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

        if target_folder == "" or folder_name == target_folder:
            for class_name, _ in filter_detections(detecions, min_conf):
                if class_name in inventory:
                    inventory[class_name] += 1
                else:
                    inventory[class_name] = 1

    return inventory


# ==========================================
#    RANKING TOP N (MANUAL SELECTION SORT)
# ==========================================

def build_ranking(invetory):
    """Convert inventory dict into [(class_name, amount), ...] sorted descending."""
    ranking = []
    for class_name, amount in invetory.items():
        ranking.append((class_name, amount))

    total_items = len(ranking)
    for i in range(total_items):
        max_index = i
        for j in range(i + 1, total_items):
            if ranking[j][1] > ranking[max_index][1]:
                max_index = j

        if max_index != i:
            temp = ranking[i]
            ranking[i] = ranking[max_index]
            ranking[max_index] = temp

    return ranking


# ==========================================
#    REVERSE INDEX & FOLDER SEARCH
# ==========================================

def build_reverse_index(results, min_conf):
    """
    Build a {class_name: [photos]} dictionary filtered by min_conf, with no duplicate photos.
    """

    reverse_index = {}  

    for photo, detections in results.items():
        for class_name, _ in filter_detections(detections, min_conf):
            if class_name in reverse_index:
                if photo not in reverse_index[class_name]:
                    reverse_index[class_name].append(photo)

            else:
                reverse_index[class_name] = [photo]

    return reverse_index


def get_reverse_search_details(results, reverse_index, target_class, min_conf):
    """Return [(photo_path, count_in_photo), ...] for a class across the dataset."""
    photos = reverse_index.get(target_class, [])
    details = []

    for photo in photos:
        count = 0
        for class_name, _ in filter_detections(results[photo], min_conf):
            if class_name == target_class:
                count += 1

        details.append((photo, count))

    return details


# ==========================================
#      FOLDER COMPARISON WITH SETS
# ==========================================

def get_folder_classes_set(results, target_folder, min_conf):
    """Return a set of distinct class names detected in a specific folder."""
    classes_set = set()

    for photo, detections in results.items():
        folder_name = os.path.basename(os.path.dirname(photo))

        if folder_name == target_folder:
            for class_name, _ in filter_detections(detections, min_conf):
                classes_set.add(class_name)

    return classes_set


def compare_folder_sets(set_a, set_b):
    """Return common (&), exclusive to A (-), exclusive to B (-), and union (|)."""
    return (set_a & set_b), (set_a - set_b), (set_b - set_a), (set_a | set_b)


# ==========================================
#       FOLDER x CLASS MATRIX
# ==========================================

def build_folder_class_matrix(results, min_conf):
    """
    Build 2D matrix (rows = folders, cols = distinct classes),
    row totals, column totals, and the (folder, class, max_val) peak.
    """
    folders = list_folders()
    classes = list(build_inventory(results, min_conf).keys())
    matrix = []
    row_totals = []
    col_totals = [0] * len(classes)
    max_val, max_folder, max_class = -1, "", ""

    for folder in folders:
        folder_inv = build_inventory(results, min_conf, folder)
        row, row_sum = [], 0

        for j in range(len(classes)):
            val = folder_inv.get(classes[j], 0)
            row.append(val)
            row_sum += val
            col_totals[j] += val

            if val > max_val:
                max_val, max_folder, max_class = val, folder, classes[j]

        matrix.append(row)
        row_totals.append(row_sum)

    return folders, classes, matrix, row_totals, col_totals, (max_folder, max_class, max_val)