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

#Entrada
def choose_folder():
    #Verifica se a pasta escolhida existe
    show_folders()
        
    folder = input("Escolha uma pasta: ")
    
    while not folder_exists(folder): 
        print("Digite um valor válido!")
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
            print("Digite um valor válido!")
        except ValueError:
            print("Digite um valor válido!")

    photo = photo_name(folder, number)
    return photo

def show_menu(confidence):
    print('\n--- OPTIONS ---')
    print(f'-- Confiança Mínima atual {confidence}--\n')
    print('1 - configurar a confiança mínima')
    print('2 - Analisar uma foto')
    print('3 - Analisar uma pasta')
    print('0 - Sair')
    return input("Escolha uma opção: ")

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

#Processamento
def relatorio_pasta(folder):

    total = 0
    vazios = 0
    caminho = photo_name(folder, p)
    
    for p in range(1,total_photos(folder)+1):
        objetos = count_objects(caminho)
        print(f"foto {p}: {objetos}")
        if objetos == 0:
            vazios += 1
        else:
            total += objetos
        
    print(f"Total geral: {total}")
    print(f"Objetos por foto: {total/total_photos(folder)}")
    print(f"Fotos sem nenhum objeto: {vazios}")

def count_photo_class(confidence, photo): #classe da foto

    show_classes()
    class_name = input("Digite uma classe para buscar objetos: ")


    print(f"Há {count_class(photo, class_name, confidence)} objetos com a classe {class_name}")

def photo_analyze(confidence):#analise da foto
    folder = choose_folder()

    photo = choose_photo(folder)

    while True:
        print("\n1 - Análise geral")
        print("2 - Contar uma classe\n")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            show_photo_summary(photo,confidence)
            break

        elif opcao == "2":
            count_photo_class(confidence, photo)
            break 

        else:
            print("Digite um valor válido")

def show_photo_summary(photo, confidence):
    print(f"Caminho: {photo}")
    print(f"Objetos detectados: {count_objects(photo,confidence)}")
    print(f"Objeto de maior confiança: {main_object(photo)}")
    print(f"Maior confiança: {max_confidence(photo) *100:.0f}%")

def folder_analyze(folder):
    choose_folder()

    print("1 - Relatório da pasta")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        relatorio_pasta(folder)




def main():
    print("PhotoCensus - Group 05")
    show_folders()
    # Your menu (while loop) starts here...

    while True:
        opcao = show_menu(confidence)

        if opcao == "1":
            set_minimal_confidence(confidence)
        elif opcao == "2":
            photo_analyze(confidence)
        elif opcao == "3":
            folder_analyze()
        elif opcao == "0":
            break
        else:
            print("Digite um valor válido!")



if __name__ == "__main__":
    main()
