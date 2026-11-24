import os
import sys 

GROUP_DIR = os.path.dirname(os.path.abspath(__file__)) 
sys.path.append(os.path.join(GROUP_DIR, "..", "..", "kit")) 
from black_box import *
from ui_utils import *
from module1_ops import *


def ask_folder(): 
    """
    Ask for the folder name until the user enters a valid one
    """
    show_folders() 
    print()

    folder = input("Enter the name of the desired folder: ").strip().lower() 
    while not folder_exists(folder):
        print("❌ Folder not found! Check the name you entered and try again.\n")
        show_folders()
        folder = input("Enter the name of the desired folder: ").strip().lower()

    return folder


def ask_photo_number(folder):
    """
    Ask for the photo number and ensure it is between 1 and the total number of photos in the folder.
    """
    total = total_photos(folder) 
    num  = int(input(f"Enter the photo number (1 to {total}): ")) 

    while num < 1 or num > total:
        print(f"Number out of range! Choose a value between 1 and {total}.")

        num  = int(input(f"Enter the photo number (1 to {total}): "))

    return num

def main():
    min_confidence_level = 0.5
    running = True

    while running:
        show_menu(min_confidence_level)
        option = input("Choose an option: ").strip()

        if option == "1":
            # Configure minimum confidence threshold (must be between 0.0 and 1.0)
            new_conf = input("Enter new confidence (0.0 to 1.0): ").strip()

            # Validate that the input is a valid number AND within the 0.0 to 1.0 range
            while not new_conf.replace(".", "", 1).isdigit() or float(new_conf) < 0.0 or float(new_conf) > 1.0:
                print("❌ Invalid confidence! Enter a numeric value between 0.0 and 1.0.")
                new_conf = input("Enter new confidence (0.0 to 1.0): ").strip()

            # Update the active confidence level used across all other options
            min_confidence_level = float(new_conf)
            print(f"✅ Minimum confidence updated to {min_confidence_level:.2f}")


        elif option == "2":
            # Analyze a single photo
            folder = ask_folder() 
            num = ask_photo_number(folder)
            photo = photo_name(folder, num)

            # Retrieve object statistics from the black-box functions
            total_objs = count_objects(photo, min_confidence_level)
            main_obj = main_object(photo)
            highest_conf = max_confidence(photo) 

            # Display photo path, object count, main object, and highest confidence as a percentage
            print(f"\n--- Photo Analysis ---")
            print(f"Path: {photo}")
            print(f"Total objects: {total_objs}")
            if main_obj:
                print(f"Main object: {main_obj}")
            else:
                print("Main object: None")
            print(f"Highest confidence: {highest_conf * 100:.1f}%")



        elif option == "3":
            # Count occurrences of a specific class in a single photo
            folder = ask_folder()
            num = ask_photo_number(folder)
            photo = photo_name(folder, num)

            # Show available classes and ensure the user does not enter an empty string
            print()
            show_classes()
            class_name = input("Enter class name (e.g., car, person): ").strip().lower()

            while class_name == "":
                print("❌ Class name cannot be empty!")
                class_name = input("Enter class name (e.g., car, person): ").strip().lower()

            # Count how many objects of the specified class meet the minimum confidence
            total_class = count_class(photo, class_name, min_confidence_level)

            print("\n--- Class Count ---")
            print(f"Photo: {photo}")
            print(f"Class: '{class_name}': {total_class} object(s) found (min_confidence: {min_confidence_level:.2f})")


        elif option == "4":
            # Generate a complete summary report for a folder
            folder = ask_folder()
            total = total_photos(folder) 

            # Initialize accumulators for total objects and empty photos
            total_objects = 0 
            empty_photos = 0 

            print(f"--- Folder Report: '{folder}' (min confidence: {min_confidence_level:.2f}) ---")

            # Loop through every photo in the folder
            for number in range(1, total + 1):
                photo = photo_name(folder, number)
                qtd = count_objects(photo, min_confidence_level)

                print(f"Photo {number} ({photo}): {qtd} object(s)")
                total_objects += qtd

                # Track photos where no objects met the confidence
                if qtd == 0:
                    empty_photos += 1

            # Calculate average objects per photo manually (avoiding built-in functions)
            if total > 0:
                average = total_objects / total
            else:
                average = 0.0

            print("-" * 40)
            print(f"Total objects in folder: {total_objects}")
            print(f"Average objects per photo: {average:.2f}")
            print(f"Photos with no objects: {empty_photos}")


        elif option == "5":

            folder = ask_folder()
            total = total_photos(folder)

            # Start with photo 1 as both the most and the least populated
            first_photo = photo_name(folder, 1)
            first_qtd = count_objects(first_photo, min_confidence_level)

            most_number = 1
            most_qtd = first_qtd
            least_number = 1
            least_qtd = first_qtd

            print(f"--- Most and least populated photo: '{folder}' (min confidence: {min_confidence_level:.2f}) ---")

            # Compare the remaining photos (2 to total) against the current records
            for number in range(2, total + 1):
                photo = photo_name(folder, number)
                qtd = count_objects(photo, min_confidence_level)

                # New record for most populated
                if qtd > most_qtd:
                    most_qtd = qtd
                    most_number = number

                # New record for least populated
                if qtd < least_qtd:
                    least_qtd = qtd
                    least_number = number

            print("-" * 40)
            print(f"Most populated: photo {most_number} ({photo_name(folder, most_number)}) with {most_qtd} object(s)")
            print(f"Least populated: photo {least_number} ({photo_name(folder, least_number)}) with {least_qtd} object(s)")


        elif option == "6":

            #Show folders and get folder name
            folder=ask_folder()   
            print()

            #Store the total number of photos of the folder
            total_phts=total_photos(folder)

            #Show classes and get class name
            show_classes()
            class_name=input("Enter class name (e.g., car, person): ").strip().lower()
            while class_name == "":
                print("❌ Class name cannot be empty!")
                class_name = input("Enter class name (e.g., car, person): ").strip().lower()
            print()
            
            #Loop through each photo to count occurrences and track matching photos
            photos_with_class=0
            total_appearances=0

            for number in range (1,total_phts+1):
                photo=photo_name(folder, number)
                found=count_class(photo,class_name,min_confidence_level)

                if found >0:
                    photos_with_class+=1
                total_appearances+=found

            #Calculate appearance percentage
            percentage=(photos_with_class/total_phts)*100

            #Output final results
            print("-" * 40)
            print(f"Total number of times {class_name} appeared in folder {folder}: {total_appearances}")
            print(f"Number of photos where {class_name} appeared: {photos_with_class}")
            print(f"Percentage of appearance of {class_name} in folder {folder}: {percentage:.2f}%")


        elif option == "7":
            # Text-based bar chart using nested loops
            folder = ask_folder()
            total = total_photos(folder)

            print(f"\n--- Bar Chart: '{folder}' (min confidence: {min_confidence_level:.2f}) ---")

            # Outer loop: iterate through every photo in the folder
            for num in range(1, total + 1):
                photo = photo_name(folder, num)
                qtd = count_objects(photo, min_confidence_level)

                base_name = os.path.basename(photo)
                label = base_name.replace(".jpg", "")
                bar = ""

                # Inner loop: build the bar string with one '#' per detected object
                for _ in range(qtd):
                    bar += "#"

                # Print aligned row matching the format: street_04
                print(f"{label:<15} | {bar} ({qtd})")


        elif option == "0":
            print("Exiting system. Goodbye!")
            running = False

        elif option == "1":
            min_confidence_level = change_minimum_confidence()

        elif option in ("2", "3", "4", "5", "6", "7", "9"):
            folder = ask_folder()
            handle_folder_option(option, folder, min_confidence_level)

        else:
            print("❌ Invalid option! Please try again.")


if __name__ == "__main__":
    main()