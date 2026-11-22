import os
from black_box import *

# ==========================================
#       INPUT & VALIDATION HELPERS
# ==========================================

def ask_folder():
    """Ask for a valid folder name."""
    show_folders()
    print()

    folder = input("Enter the name of the desired folder: ").strip().lower()

    while not folder_exists(folder):
        print("❌ Folder not found! Check the name you entered and try again.\n")
        show_folders()

        folder = input("Enter the name of the desired folder: ").strip().lower()

    return folder


def ask_photo_number(folder):
    """Ask for a valid photo number within the folder range."""
    total = total_photos(folder)
    num = 0
    valid = False

    while not valid:
        raw = input(f"Enter the photo number (1 to {total}): ").strip()

        try:
            num = int(raw)

            if 1 <= num <= total:
                valid = True

            else:
                print(f"❌ Number out of range! Choose between 1 and {total}.")

        except ValueError:
            print("❌ ERROR! Enter a numeric value!")

    return num


def ask_class_name():
    """Display classes and ask for a non-empty class name."""
    print()
    show_classes()

    class_name = input("Enter class name (e.g., car, person): ").strip().lower()

    while class_name == "":
        print("❌ Class name cannot be empty!")
        class_name = input("Enter class name (e.g., car, person): ").strip().lower()

    return class_name


# ==========================================
#      OPTION 1: CONFIDENCE THRESHOLD
# ==========================================

def change_minimum_confidence():
    """Validate and return a new confidence threshold (0.0 to 1.0)."""
    new_conf = 0.5
    valid = False

    while not valid:
        raw = input("Enter new confidence (0.0 to 1.0): ").strip()

        try:
            new_conf = float(raw)

            if 0.0 <= new_conf <= 1.0:
                valid = True

            else:
                print("❌ Invalid confidence! Value must be between 0.0 and 1.0.")

        except ValueError:
            print("❌ Invalid confidence! Enter a numeric value between 0.0 and 1.0.")

    print(f"✅ Minimum confidence updated to {new_conf:.2f}")
    return new_conf


# ==========================================
#    OPTION 2: ANALYZE SINGLE PHOTO
# ==========================================

def print_photo_analysis(photo, total_objs, main_obj, highest_conf):
    """Display formatted analysis of a single photo."""
    print("\n--- Photo Analysis ---")
    print(f"Path: {photo}")
    print(f"Total objects: {total_objs}")
    print(f"Main object: {main_obj if main_obj else 'None'}")
    print(f"Highest confidence: {highest_conf * 100:.1f}%")


# ==========================================
#     OPTION 3: COUNT CLASS IN PHOTO
# ==========================================

def print_class_in_photo(photo, class_name, total_class, min_conf):
    """Display class count result for a single photo."""
    print("\n--- Class Count ---")
    print(f"Photo: {photo}")
    print(f"Class '{class_name}': {total_class} object(s) found (min_confidence: {min_conf:.2f})")


# ==========================================
#        OPTION 4: FOLDER REPORT
# ==========================================

def print_folder_summary(total_objects, average, empty_photos):
    """Display summary totals for the folder report."""
    print("-" * 40)
    print(f"Total objects in folder: {total_objects}")
    print(f"Average objects per photo: {average:.2f}")
    print(f"Photos with no objects: {empty_photos}")


# ==========================================
#    OPTION 5: MOST & LEAST POPULATED
# ==========================================

def print_population_extremes(folder, min_conf, most_num, most_qtd, least_num, least_qtd):
    """Display most and least populated photo results."""
    print(f"\n--- Most and least populated photo: '{folder}' (min confidence: {min_conf:.2f}) ---")
    print("-" * 40)
    print(f"Most populated: photo {most_num} ({photo_name(folder, most_num)}) with {most_qtd} object(s)")
    print(f"Least populated: photo {least_num} ({photo_name(folder, least_num)}) with {least_qtd} object(s)")


# ==========================================
#     OPTION 6: SEARCH CLASS IN FOLDER
# ==========================================

def print_class_search(folder, class_name, total_appearances, photos_with_class, percentage):
    """Display class search statistics for a folder."""
    print("-" * 40)
    print(f"Total number of times {class_name} appeared in folder {folder}: {total_appearances}")
    print(f"Number of photos where {class_name} appeared: {photos_with_class}")
    print(f"Percentage of appearance of {class_name} in folder {folder}: {percentage:.2f}%")


# ==========================================
#           OPTION 7: BAR CHART
# ==========================================

def build_bar(qtd):
    """Build a '#' bar string using a loop."""
    bar = ""

    for _ in range(qtd):
        bar += "#"

    return bar


def print_bar_chart(folder, min_conf):
    """Display text-based bar chart for all photos in a folder."""
    total = total_photos(folder)
    print(f"\n--- Bar Chart: '{folder}' (min confidence: {min_conf:.2f}) ---")

    for num in range(1, total + 1):
        photo = photo_name(folder, num)
        qtd = count_objects(photo, min_conf)
        label = os.path.basename(photo).replace(".jpg", "")

        print(f"{label:<15} | {build_bar(qtd)} ({qtd})")


# ==========================================
#                  MENU
# ==========================================

def show_menu(min_conf):
    """Display the main CLI menu."""
    print("\n" + "=" * 40)
    print(f"{'PHOTOCENSUS - MENU':^40} Group 03")
    print("=" * 40)
    print(f"Current minimum confidence: {min_conf:.2f}")
    print("-" * 40)
    print("[ 1 ] - Change minimum confidence")
    print("[ 2 ] - Analyze a photo")
    print("[ 3 ] - Count class in a photo")
    print("[ 4 ] - Folder report")
    print("[ 5 ] - Most and least populated photo")
    print("[ 6 ] - Search class in folder")
    print("[ 7 ] - Bar chart (text)")
    print("[ 0 ] - Exit")
    print("=" * 40)


