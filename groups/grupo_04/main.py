"""
PhotoCensus - Group 04 
"""
import os
import sys

# Lets this file find black_box.py in /kit (do not remove these lines)
GROUP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(GROUP_DIR, "..", "..", "kit"))
from black_box import *  # noqa: E402,F401,F403


def main():
    print("PhotoCensus - Group 04")

#Main variables
    min_confidence = 0.5
    start_variable = -1
    total_objects_folder = 0
    empty_photos_folder = 0
    max_objects = 0
    min_objects = 0
    max_photo = ""
    min_photo = ""
    photos_with_class = 0
    total_class_count = 0

#Input clause
    while start_variable != 0:

#Main input
        print("\n--- Program start ---")
        start_variable = int(input("Type 1 to start the program. Type 0 to end it: "))

#Error handler
        while start_variable != 1 and start_variable != 0:
            print("ERROR. Type either 1 or 0.")
            start_variable = int(input("Type 1 to start the program. Type 0 to end it: "))

#Program end
        if start_variable == 0:
            exit()

#Program start
        else:
            print("\nWelcome. Choose between one of these options.")
            print("1- View available folders, and how many images.")
            print("2- Select folder, and image number.")
            print("3- View a detailed folder's report")
            print("4- Set the system's trust configuration")

#Path selection
            print("\n")
            option_variable = int(input("Choose your option: "))
            
#Error handler
            while option_variable < 1 or option_variable > 4:
                print("ERROR. Input a number from 1 to 4")
                option_variable = int(input("Choose your option: "))

#Path 1
            if option_variable == 1:
                print("\nAvailable folders below")
                folders = ["animals", "kitchen", "living_room", "office", "sports", "street"]
                for f in folders:
                    quantity = total_photos(f)
                    print(f"Folder: {f}. Photo quantity: {quantity}")

#Path 2
            elif option_variable == 2:
                print("\nChoose the folder's name and image")
                folder_name = str(input("Type the folder's name: "))

#Error handler                
                while not folder_exists(folder_name):
                    print("\nERROR. Input a valid folder name")
                    print("If you are unsure of the names for each folder, input 'y' on the following prompt")
                    print("If you mistyped, type 'n' on the following prompt")

#Option to see folders
                    back_prompt = str(input("Type 'y' or 'n'. More information above this prompt: ")).strip().lower()
                    while back_prompt != "y" and back_prompt != "n":
                        print("ERROR. Type either y or n")
                        back_prompt = str(input("Type 'y' or 'n' to continue: ")).strip().lower()
                    if back_prompt == 'y': 
                        print("\nHere are the available folders:")
                        show_folders()

#Continuation into the image's number
                    folder_name = str(input("Type the folder's name: "))
                print("\nNow select the image's number.")
                image_number = int(input(f"Type the desired image from the folder {folder_name}: "))

#Error handler                
                while image_number < 1 or image_number > 8:
                    print("\nERROR. Please input a number from 1 to 8.")
                    image_number = int(input(f"Type the desired image from the folder {folder_name}: "))

#Image analysis
                image_path = photo_name(folder_name, image_number)
                total_objects = count_objects(image_path, min_confidence)
                main_obj = main_object(image_path)                
                max_conf = max_confidence(image_path) * 100

#Image report
                print("\n--- Image report: ---")
                print(f"Image path: {image_path}")
                print(f"Total objects detected: {total_objects}")
                print(f"Main object: {main_obj}. Confidence: {max_conf:.1f}%")

#Specific search
                print("\nWould you like to search for a specific object?")
                specific_search = str(input("Type 'y' or 'n' to continue: ")).strip().lower()

#Error handler                
                while specific_search != "y" and specific_search != "n":
                    print("\nERROR. Type either y or n")
                    specific_search = str(input("Type 'y' or 'n' to continue: ")).strip().lower()

#Continuation of the search                    
                if specific_search == 'y':
                    show_classes()   
                    class_name = str(input("\nFrom the selection above, select your desired object: "))
                    class_quantity = count_class(image_path, class_name, min_confidence)
                    print(f"The search found {class_quantity} objects from the {class_name} classification in this image.")

    
#Path 3 
            elif option_variable == 3:
                print("\nType the folder's name to generate the full analysis.")
                folder_name = str(input("Type the folder's name: "))

#Error handler              
                while not folder_exists(folder_name):
                    print("\nERROR. Input a valid folder name")
                    print("If you are unsure of the names for each folder, input 'y' on the following prompt")
                    print("If you mistyped, type 'n' on the following prompt")

#Option to see folders
                    back_prompt = str(input("Type 'y' or 'n'. More information above this prompt: ")).strip().lower()
                    while back_prompt != "y" and back_prompt != "n":
                        print("ERROR. Type either y or n")
                        back_prompt = str(input("Type 'y' or 'n' to continue: ")).strip().lower()
                    if back_prompt == 'y': 
                        print("Here are the available folders:")
                        show_folders()
                    folder_name = str(input("Type the folder's name: "))

#Analysis begins; Desired class selection
                total_p = total_photos(folder_name)
                show_classes()
                class_name = str(input("Select your desired object class from above: "))
                print("\n--- Analysing the folder's images: ---")

#Main 'for' operation; Printing image information
                for i in range(1, total_p + 1):
                    photo_path = photo_name(folder_name, i)
                    count = count_objects(photo_path, min_confidence)
                    total_objects_folder += count
                    if count == 0:
                        empty_photos_folder += 1
                    print(f"Photo {i} ({os.path.basename(photo_path)}): {count} object(s) detected")

#Highest and lowest object count
                    if i == 1:
                        max_objects = count
                        min_objects = count
                        max_photo = photo_path
                        min_photo = photo_path
                    else:
                        if count > max_objects:
                            max_objects = count
                            max_photo = photo_path
                        if count < min_objects:
                            min_objects = count
                            min_photo = photo_path

#Class' appearence on folder
                    c_count = count_class(photo_path, class_name, min_confidence)
                    total_class_count += c_count
                    if c_count > 0:
                        photos_with_class += 1

#Full information report
                average_objects = total_objects_folder / total_p
                print("\n--- Full information report ---")
                print(f"Full object total: {total_objects_folder}")
                print(f"Average objects per photo: {average_objects:.2f}")
                print(f"Photos without any objects: {empty_photos_folder}")
                print(f"Photo with the most objects: {max_photo} with {max_objects} objects")
                print(f"Photo with the least objects: {min_photo} with {min_objects} objets")
                percentage_class = (photos_with_class / total_p) * 100
                print(f"The class '{class_name}' appears in {photos_with_class} of {total_p} photos ({percentage_class:.1f}%).")
                print(f"Times the class '{class_name}' was found: {total_class_count} time(s)")

#Bar graph report
                print("\n--- Bar graph report ---")
                for i in range(1, total_p + 1):
                    photo_path = photo_name(folder_name, i)
                    count = count_objects(photo_path, min_confidence)   
                    bar = ""
                    for j in range(count):  
                        bar += "#"
                    photo_label = f"{folder_name}_{i:02d}"
                    print(f"{photo_label} | {bar} ({count})")  

#Path 4
            else:                  
                print("Now select the desired confidence for the system's recognition.")
                min_confidence = float(input("Input a number from 0.0 to 1.0: "))

#Error handler                
                while min_confidence < 0.0 or min_confidence > 1.0:
                    print("ERROR. Please input a number from 0.0 to 1.0")
                    min_confidence = float(input("Input a number from 0.0 to 1.0: "))
             


if __name__ == "__main__":
    main() 
