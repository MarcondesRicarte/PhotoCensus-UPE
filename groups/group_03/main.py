import os
import sys

GROUP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(GROUP_DIR, "..", "..", "kit"))

from black_box import *
from ui_utils import *
from module1_ops import *



def main():
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

        else:
            print("❌ Invalid option! Please try again.")


if __name__ == "__main__":
    main()