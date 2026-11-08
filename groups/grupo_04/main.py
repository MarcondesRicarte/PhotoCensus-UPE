"""
PhotoCensus - Group 04 (TEMPLATE)

Copy this folder to /groups/group_XX/ (XX = your group number)
and write your project here. Do not modify anything in /kit.
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

#Input clause
    while start_variable != 0:

#Main input
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
            print("Welcome. Choose one of these 2 options.")
            print("1- View available folders, and how many images.")
            print("2- Select folder, and image number.")

#Path selection
            option_variable = int(input("Choose your option: "))

#Error handler
            while option_variable != 1 and option_variable != 2:
                print("ERROR. Input 1 to view options. Input 2 to select options.")
                option_variable = int(input("Choose your option: "))

#Path 1
            if option_variable == 1:
                print("Available folders below")
                folders = ["animals", "kitchen", "living_room", "office", "sports", "street"]
                for f in folders:
                    quantity = total_photos(f)
                    print(f"Folder: {f}. Photo quantity: {quantity}")

#Path 2
            else:
                print("Type the folder's name, and desired image, as a number, from 1 to 8.")
                folder_name = str(input("Type the folder's name: "))

#Error handler                
                while not folder_exists(folder_name):
                    print("ERROR. Input a valid folder name")
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

#Continuation into the image's number
                    folder_name = str(input("Type the folder's name: "))
                image_number = int(input(f"Type the desired image from the folder {folder_name}: "))

#Error handler                
                while image_number < 1 or image_number > 8:
                    print("ERROR. Please input a number from 1 to 8.")
                    image_number = int(input(f"Type the desired image from the folder {folder_name}: "))

#Confidence configuration                    
                print("Right. Now select the desired confidence for the A.I's recognition.")
                min_confidence = float(input("Input a number from 0.0 to 1.0: "))

#Error handler                
                while min_confidence < 0.0 or min_confidence > 1.0:
                    print("ERROR. Please input a number from 0.0 to 1.0")
                    min_confidence = float(input("Input a number from 0.0 to 1.0: "))

#Image analysis
                image_path = photo_name(folder_name, image_number)
                total_objects = count_objects(image_path, min_confidence)
                main_obj = main_object(image_path)                
                max_conf = max_confidence(image_path) * 100

#Image report
                print("Image report:")
                print(f"Image path: {image_path}")
                print(f"Total objects detected: {total_objects}")
                print(f"Main object: {main_obj}. Confidence: {max_conf:.1f}%")

#Specific search
                print("Would you like to search for a specific object?")
                specific_search = str(input("Type 'y' or 'n' to continue: ")).strip().lower()
#Error handler                
                while specific_search != "y" and specific_search != "n":
                    print("ERROR. Type either y or n")
                    specific_search = str(input("Type 'y' or 'n' to continue: ")).strip().lower()
#Continuation of the search                    
                if specific_search == 'y':
                    show_classes()   
                    class_name = str(input("From the selection above, select your desired object: "))
                    class_quantity = count_class(image_path, class_name, min_confidence)
                    print(f"The search found {class_quantity} objects from the {class_name} classification in this image.")

        

if __name__ == "__main__":
    main()
    
   
