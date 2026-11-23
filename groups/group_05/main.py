"""
PhotoCensus - Group 00 (TEMPLATE)

Copy this folder to /groups/group_XX/ (XX = your group number)
and write your project here. Do not modify anything in /kit.
"""
import os
import sys

# Lets this file find black_box.py in /kit (do not remove these lines)
GROUP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(GROUP_DIR, "..", "..", "kit"))
from black_box import *   # noqa: E402,F401,F403


MSG_INVALID = "Digite um valor válido!"

confidence = 0.5

#Entradas
def choose_folder():
    #Verifica se a pasta escolhida existe
    show_folders()
        
    folder = input("Escolha uma pasta: ")

    #repete se a entrada estiver vazia ou nao existir
    while not folder_exists(folder): 
        print(MSG_INVALID)
        show_folders()
        folder = input("Escolha uma pasta: ")
    return folder

def choose_photo(folder):
    #Pede o número da foto até estar entre 1 e o total da pasta;
    # retorna o caminhno da foto.
    total = total_photos(folder)
    while True:
        try:
            number = int(input(f"Escolha uma foto (de 1 a {total}): "))
            if 1 <= number <= total:
                break
            print(MSG_INVALID)
        except ValueError:
            print(MSG_INVALID)

    photo = photo_name(folder, number)
    return photo

def set_minimal_confidence():
    #Define a confiança mínima entre 0.0 e 1.0
    global confidence
    while True:
        try:
            new = float(input("Defina a nova confiança mínima: "))
            if 0 <= new <= 1:
                break
            else:
                print("Defina um valor entre 0.0 e 1.0")
        except ValueError:
            print("Defina um valor entre 0.0 e 1.0")
       
    confidence = new

#Opções do menu
def show_photo_summary(photo, confidence): #requisito 4
    # Mostra as principais informações detectadas na foto.
    print(f"Caminho: {photo}")
    print(f"Objetos detectados: {count_objects(photo,confidence)}")
    print(f"Objeto de maior confiança: {main_object(photo)}")
    print(f"Maior confiança: {max_confidence(photo) *100:.0f}%")

def count_photo_class(confidence, photo): #requisito 5
    #imprime a quantidade de objetos com a mesma classe na foto
    show_classes()
    class_name = input("Digite uma classe para buscar objetos: ")

    print(f"Há {count_class(photo, class_name, confidence)} objetos com a classe {class_name}")

def report_folder(folder, confidence): #requisito 6
    #percorre todas as fotos da pasta e conta os objetos
    photos = total_photos(folder)
    empty = 0                       #fotos sem objetos
    total = 0                       #total de objetos
    
    for photo_number in range(1,photos+1):
        photo = photo_name(folder, photo_number)
        objects = count_objects(photo, confidence)
        #recebe e imprime os objetos da foto iterada
        print(f"foto {photo_number}: {objects}")

        #incrementa o total de objetos e as fotos vazias
        total += objects
        if objects == 0: 
            empty += 1 

    print(f"Total geral: {total}")
    print(f"Média de objetos por foto: {total / photos}")
    print(f"Fotos sem nenhum objeto: {empty}")

def find_fullest_emptiest(folder,confidence): #requisito 7
    #percorre a pasta comparando a qtd. de objetos das fotos
    total = total_photos(folder)

    #caminho e quantidade de objetos da foto mais cheia
    fullest_photo = photo_name(folder,1) #retorna o caminho da primeira foto
    fullest_objects = count_objects(fullest_photo, confidence) 

    #define que a 1ª foto é o valor inicial de ambos
    emptiest_photo = fullest_photo
    emptiest_objects = fullest_objects

    for photo_number in range(2, total+1):
        photo = photo_name(folder, photo_number)
        objects = count_objects(photo,confidence)

        #compara e atualiza as variaveis
        if objects > fullest_objects:
            fullest_objects = objects
            fullest_photo = photo

        if objects < emptiest_objects:
            emptiest_objects = objects
            emptiest_photo = photo

    print(f"Foto com mais objetos: {fullest_photo}\nTotal: {fullest_objects}")
    print(f"Foto com menos objetos: {emptiest_photo}\nTotal: {emptiest_objects}")

def find_class_in_folder(folder,confidence): #requisito 8
    show_classes()
    class_name = input("Escolha uma classe: ")

    # Conta em quantas fotos a classe aparece e o total de objetos encontrados.
    total = total_photos(folder)
    photo_with_class = 0
    total_objects = 0

    for photo_number in range(1, total+1):
        photo = photo_name(folder, photo_number)
        class_count = count_class(photo, class_name, confidence)

        if class_count > 0:
            photo_with_class += 1
            total_objects += class_count

    print(f"A classe aparece em {photo_with_class} fotos")
    print(f"Total de objetos com a classe: {total_objects}")
    print(f"A classe está presente em {(photo_with_class / total) *100:.1f}% da pasta")

def show_bar_chart(folder, confidence): #requisito 9
    total = total_photos(folder)

    # Monta uma barra de # para cada objeto detectado em cada foto.
    for photo_number in range(1,total+1):
        photo = photo_name(folder, photo_number)
        total_objects = count_objects(photo, confidence)
        chart = ""

        for objects in range(total_objects):
            chart += "#" 

        print(f"{folder}_{photo_number} | {chart} ({total_objects})")

#modulo2 requisitos

def collection_results():  #requisito 1
    # detecções, armazenamento de resultados e resumo
    results = {}

    folders = list_folders()

    folder_count = 0
    photo_count = 0
    detection_count = 0

    for folder in folders:
        folder_count += 1

        photos = list_photos(folder)

        for photo in photos:
            photo_count += 1
            detections = detect(photo)
            results[photo] = detections
            detection_count += len(detections)

    print("\n--- ACERVO ---")
    print(f"Pastas: {folder_count}")
    print(f"Fotos: {photo_count}")
    print(f"Detecções: {detection_count}")

    return results

def filter_detections(detections, confidence):  #requisito 2
    #filtro de confiança, filtra os resultados de acordo com a confiança escolhida.
    filtered = []

    for class_name, score in detections:
        if score >= confidence:
            filtered.append((class_name, score))

    return filtered

#Menus
def show_menu(confidence): #menu principal
    print('\n--- OPTIONS ---')
    print(f'-- Confiança Mínima atual {confidence}--\n')
    print('1 - Configurar a confiança mínima')
    print('2 - Analisar uma foto')
    print('3 - Analisar uma pasta')
    print('0 - Sair')
    return input("Escolha uma opção: ")

def analyze_photo(confidence):

    folder = choose_folder()
    photo = choose_photo(folder)

    #Submenus
    while True:
        print("\n1 - Análise geral")
        print("2 - Contar uma classe\n")
        option = input("Escolha uma opção: ")

        if option == "1":
            show_photo_summary(photo,confidence)
            break
        elif option == "2":
            count_photo_class(confidence, photo)
            break 
        else:
            print("Digite um valor válido")

def analyze_folder(confidence):
    folder = choose_folder()

    # Repete o menu até uma das análises da pasta ser escolhida.
    while True:
        print("1 - Relatório da pasta")
        print("2 - Foto mais cheia e mais vazia")
        print("3 - Procurar uma classe na pasta")
        print("4 - Gráfico de barras em texto")

        option = input("Escolha uma opção: ")

        if option == "1":
            report_folder(folder, confidence)
            break
        elif option == "2":
            find_fullest_emptiest(folder,confidence)
            break
        elif option == "3":
            find_class_in_folder(folder,confidence)
            break
        elif option == "4":
            show_bar_chart(folder, confidence)
            break
        else:
            print(MSG_INVALID)



def main():
    print("PhotoCensus - Group 05")
    show_folders()

    while True:
        option = show_menu(confidence)

        if option == "1":
            set_minimal_confidence()
        elif option == "2":
            analyze_photo(confidence)
        elif option == "3":
            analyze_folder(confidence)
        elif option == "0":
            break
        else:
            print(MSG_INVALID)



if __name__ == "__main__":
    main()
