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


def ask_top_n():
    """Ask for a positive integer N for Top N ranking."""
    n = 0
    valid = False
    while not valid:
        raw = input("Enter N for Top N classes: ").strip()
        try:
            n = int(raw)
            if n >= 1:
                valid = True
            else:
                print("❌ N must be at least 1.")
        except ValueError:
            print("❌ ERROR! Enter a valid integer.")
    return n


def ask_binary_choice(prompt_text):
    """Ask the user to choose strictly between '1' and '2'."""
    choice = input(prompt_text).strip()

    while choice != "1" and choice != "2":
        print("❌ Invalid choice! Please enter 1 or 2.")
        choice = input(prompt_text).strip()

    return choice


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
#       MODULE 1 OUTPUT FUNCTIONS (2-7)
# ==========================================

def print_photo_analysis(photo, total_objs, main_obj, highest_conf):
    """Display formatted analysis of a single photo."""
    print("\n--- Photo Analysis ---")
    print(f"Path: {photo}")
    print(f"Total objects: {total_objs}")
    print(f"Main object: {main_obj if main_obj else 'None'}")
    print(f"Highest confidence: {highest_conf * 100:.1f}%")


def print_class_in_photo(photo, class_name, total_class, min_conf):
    """Display class count result for a single photo."""
    print("\n--- Class Count ---")
    print(f"Photo: {photo}")
    print(f"Class '{class_name}': {total_class} object(s) found (min_confidence: {min_conf:.2f})")


def print_folder_summary(total_objects, average, empty_photos):
    """Display summary totals for the folder report."""
    print("-" * 40)
    print(f"Total objects in folder: {total_objects}")
    print(f"Average objects per photo: {average:.2f}")
    print(f"Photos with no objects: {empty_photos}")


def print_population_extremes(folder, min_conf, most_num, most_qtd, least_num, least_qtd):
    """Display most and least populated photo results."""
    print(f"\n--- Most and least populated photo: '{folder}' (min confidence: {min_conf:.2f}) ---")
    print("-" * 40)
    print(f"Most populated: photo {most_num} ({photo_name(folder, most_num)}) with {most_qtd} object(s)")
    print(f"Least populated: photo {least_num} ({photo_name(folder, least_num)}) with {least_qtd} object(s)")


def print_class_search(folder, class_name, total_appearances, photos_with_class, percentage):
    """Display class search statistics for a folder."""
    print("-" * 40)
    print(f"Total number of times {class_name} appeared in folder {folder}: {total_appearances}")
    print(f"Number of photos where {class_name} appeared: {photos_with_class}")
    print(f"Percentage of appearance of {class_name} in folder {folder}: {percentage:.2f}%")


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
#      MODULE 2 OUTPUT FUNCTIONS (8-14)
# ==========================================

def print_inventory(inventory, scope_label, min_conf):
    """Display object count dictionary for dataset or folder."""
    print(f"\n--- Inventory: {scope_label} (min confidence: {min_conf:.2f}) ---")
    if not inventory:
        print("No objects found.")
    for class_name, amount in inventory.items():
        print(f"- {class_name:<15}: {amount}")


def print_ranking(ranking, n, min_conf):
    """Display Top N classes from sorted ranking."""
    print(f"\n--- Top {n} Classes (min confidence: {min_conf:.2f}) ---")
    if not ranking:
        print("No detections found.")
        return

    limit = n if n < len(ranking) else len(ranking)
    for i in range(limit):
        class_name, amount  = ranking[i]
        print(f"{i + 1}°. {class_name:<15} -> {amount} detection(s)")


def print_reverse_search(target_class, details, min_conf):
    """Display reverse index search results."""
    print(f"\n--- Reverse Search: '{target_class}' (min conf: {min_conf:.2f}) ---")
    if not details:
        print(f"❌ Class '{target_class}' was not found in the dataset.")
    else:
        for photo, count in details:
            print(f"- {photo}: {count} occurrence(s)")


def format_set_items(items_set):
    """Format set contents cleanly without using sorted()."""
    return ", ".join(items_set) if items_set else "None"


def print_set_comparison(folder_a, folder_b, common, only_a, only_b, union_set):
    """Display set operations between two folders."""
    print(f"\n--- Set Comparison: '{folder_a}' vs '{folder_b}' ---")
    print(f"Common classes (&): {format_set_items(common)}")
    print(f"Only in '{folder_a}' (-): {format_set_items(only_a)}")
    print(f"Only in '{folder_b}' (-): {format_set_items(only_b)}")
    print(f"Union (|): {format_set_items(union_set)}")


def print_matrix_block(folders, classes_slice, matrix, col_totals_slice, start_idx, show_row_total, row_totals):
    """Print a subset of columns of the Folder x Class matrix so it fits cleanly in the terminal."""
    header = f"{'Folder':<12} | " + " ".join(f"{c[:6]:>6}" for c in classes_slice)
    if show_row_total:
        header += " | Total"
    print(header)
    print("-" * len(header))

    end_idx = start_idx + len(classes_slice)
    for i in range(len(folders)):
        row_vals = [matrix[i][j] for j in range(start_idx, end_idx)]
        row_str = f"{folders[i]:<12} | " + " ".join(f"{val:>6}" for val in row_vals)
        if show_row_total:
            row_str += f" | {row_totals[i]:>5}"
        print(row_str)

    print("-" * len(header))
    tot_str = f"{'Total':<12} | " + " ".join(f"{val:>6}" for val in col_totals_slice)
    if show_row_total:
        tot_str += " |"
    print(tot_str)
    print()


def print_matrix(folders, classes, matrix, row_totals, col_totals, peak_info):
    """Print aligned Folder x Class matrix split into clean 8-column blocks."""
    if not classes:
        print("\nNo detections available for matrix.")
        return

    print("\n--- Folder x Class Matrix ---")
    step = 8
    for start in range(0, len(classes), step):
        end = start + step
        is_last_block = end >= len(classes)
        print_matrix_block(
            folders,
            classes[start:end],
            matrix,
            col_totals[start:end],
            start,
            is_last_block,
            row_totals,
        )

    print(f"🏆 Highest combination: folder '{peak_info[0]}' + class '{peak_info[1]}' ({peak_info[2]} objects)")


def print_ranking_histogram(ranking, min_conf):
    """Display inventory as a text bar chart ordered by ranking."""
    print(f"\n--- Ordered Histogram (min conf: {min_conf:.2f}) ---")
    if not ranking:
        print("No detections found.")
    for cls_name, amount in ranking:
        print(f"{cls_name:<15} | {build_bar(amount)} ({amount})")


def save_report_file(filepath, inventory, ranking, min_conf):
    """Save inventory and ranking to report.txt using open()."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"PHOTOCENSUS REPORT (min confidence: {min_conf:.2f})\n")
        f.write("=" * 45 + "\n\nINVENTORY:\n")
        for cls_name, amount in inventory.items():
            f.write(f"- {cls_name}: {amount}\n")
        f.write("\nRANKING:\n")
        for i in range(len(ranking)):
            f.write(f"{i + 1}. {ranking[i][0]} ({ranking[i][1]})\n")
    print(f"✅ Report successfully saved to {filepath}")


def read_report_file(filepath):
    """Read and display report.txt if it exists."""
    if not os.path.exists(filepath):
        print("❌ report.txt not found! Save a report first.")
    else:
        print("\n--- Saved Report Content ---")
        with open(filepath, "r", encoding="utf-8") as f:
            print(f.read())


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
    print("[ 1 ]  - Change minimum confidence")
    print("[ 2 ]  - Analyze a photo")
    print("[ 3 ]  - Count class in a photo")
    print("[ 4 ]  - Folder report")
    print("[ 5 ]  - Most and least populated photo")
    print("[ 6 ]  - Search class in folder")
    print("[ 7 ]  - Bar chart (text)")
    print("-" * 45)
    print("[ 8 ]  - Inventory (dataset or folder)")
    print("[ 9 ]  - Ranking Top N")
    print("[ 10 ] - Reverse search (by class)")
    print("[ 11 ] - Compare folders (sets)")
    print("[ 12 ] - Folder X Class matrix")
    print("[ 13 ] - Ordered histogram")
    print("[ 14 ] - Save / Read report.txt")
    print("[ 0 ] - Exit")
    print("=" * 40)


