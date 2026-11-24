from black_box import *

# ==========================================
#    OPTION 2: ANALYZE SINGLE PHOTO
# ==========================================

def get_photo_stats(folder, num, min_conf):
    """Fetch object count, main object, and max confidence for a photo."""
    photo = photo_name(folder, num)
    total_objs = count_objects(photo, min_conf)
    main_obj = main_object(photo)
    highest_conf = max_confidence(photo)
    return photo, total_objs, main_obj, highest_conf


# ==========================================
#        OPTION 4: FOLDER REPORT
# ==========================================

def compute_folder_report(folder, min_conf):
    """Calculate total objects, empty photos, and average per photo."""
    total = total_photos(folder)
    total_objects = 0
    empty_photos = 0

    print(f"\n--- Folder Report: '{folder}' (min confidence: {min_conf:.2f}) ---")

    for number in range(1, total + 1):
        photo = photo_name(folder, number)
        qtd = count_objects(photo, min_conf)

        print(f"Photo {number} ({photo}): {qtd} object(s)")

        total_objects += qtd

        if qtd == 0:
            empty_photos += 1

    average = (total_objects / total) if total > 0 else 0.0
    return total_objects, average, empty_photos


# ==========================================
#    OPTION 5: MOST & LEAST POPULATED
# ==========================================

def find_population_extremes(folder, min_conf):
    """Find photo numbers and object counts for most and least populated photos."""
    total = total_photos(folder)
    first_qtd = count_objects(photo_name(folder, 1), min_conf)

    most_num, most_qtd = 1, first_qtd
    least_num, least_qtd = 1, first_qtd

    for number in range(2, total + 1):
        qtd = count_objects(photo_name(folder, number), min_conf)

        if qtd > most_qtd:
            most_qtd, most_num = qtd, number

        if qtd < least_qtd:
            least_qtd, least_num = qtd, number

    return most_num, most_qtd, least_num, least_qtd


# ==========================================
#     OPTION 6: SEARCH CLASS IN FOLDER
# ==========================================

def search_class_stats(folder, class_name, min_conf):
    """Count total class appearances, matching photos, and appearance percentage."""
    total_phts = total_photos(folder)
    photos_with_class = 0
    total_appearances = 0

    for number in range(1, total_phts + 1):
        found = count_class(photo_name(folder, number), class_name, min_conf)

        if found > 0:
            photos_with_class += 1

        total_appearances += found

    percentage = (photos_with_class / total_phts) * 100 if total_phts > 0 else 0.0
    return total_appearances, photos_with_class, percentage
