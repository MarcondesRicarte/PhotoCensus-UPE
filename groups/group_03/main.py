import os
import sys 

GROUP_DIR = os.path.dirname(os.path.abspath(__file__)) 
sys.path.append(os.path.join(GROUP_DIR, "..", "..", "kit")) 

from ui_utils import *
from menu_router import *
from data_engine import *


def main():
    results, f_count, p_count, d_count = load_dataset()
    print(f"✅ Dataset loaded: {f_count} folders | {p_count} photos | {d_count} detections.")
    min_confidence_level = 0.5
    running = True

    while running:
        show_menu(min_confidence_level)
        option = input("Choose an option: ").strip()

        if option == "0":
            print("Exiting system. Goodbye!")
            running = False

        elif option == "1":
            min_confidence_level = change_minimum_confidence()

        elif option in ("2", "3", "4", "5", "6", "7"):
            folder = ask_folder()
            handle_folder_option(option, folder, min_confidence_level)

        elif option in ("8", "9", "10", "11", "12", "13", "14"):
            handle_module2_option(option, results, min_confidence_level)

        else:
            print("❌ Invalid option! Please try again.")


if __name__ == "__main__":
    main()