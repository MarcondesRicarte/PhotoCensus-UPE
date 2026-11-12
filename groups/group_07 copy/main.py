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
from black_box import *  # noqa: E402,F401,F403


def perguntar_pasta():
    show_folders() 
    pasta_valida = False
    nome_pasta = ""
    while not pasta_valida:
        nome_pasta = input("digite a pasta desejada(ex:animals,sports,streets): ").strip()
        if nome_pasta =="":
            print("Pasta não pode ser vazia. Tente novamente.")
        elif not folder_exists(nome_pasta):
            print(f"Pasta '{nome_pasta}' não existe. Tente novamente.")
        elif total_photos(nome_pasta) == 0:
            print(f"Pasta '{nome_pasta}' não contém fotos. Tente novamente.")
        else:
            pasta_valida = True
    return nome_pasta




def perguntar_foto():
    diretorio = ask_folder()
    quantidade_imagens = total_photos(diretorio)
    print(f"Total de imagens disponiveis em {diretorio}: {quantidade_imagens}")
    indice_valido = False
    indice_escolhido = 0
    while not indice_valido:
        entrada = input(f"Escolha um índice de 1 a {quantidade_imagens}: ").strip()
        try:
            indice_escolhido = int(entrada)
            if 1 <= indice_escolhido <= quantidade_imagens:
                indice_valido = True
            else:
                print(f"Índice inválido. Digite um número entre 1 e {quantidade_imagens}.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")
    return photo_name(diretorio, indice_escolhido)




def main():
    print("PhotoCensus - Group 07")

    print ("tudo inicou aqui!")
    

    confidence_pad_level =0.5
    
    
    
    while True:
        print("Escolha uma opção:")
        print("""
        1- Configurar confiança minima
        2- Analisar fotos
        3- Contar uma classe de fotos
        4- Relatorio da pasta
        5- Foto mais cheia e mais vazia
        6- Procurar classe na pasta
        7- Grafico de barras em texto
        0- Sair""")

        decision = input('Escolha uma opção: ').strip()

        if decision == "0":
            break

        elif decision == "1":
            print("\n--Escolha a confiança minima:")
            print(f"Confiança atual: {confidence_pad_level}")

            while True:
                try:
                    confidence_pad_level = float(input("Digite um valor entre 0.0 e 1.0: "))
                    if 0 <= confidence_pad_level <= 1:
                        print(f"Confiança minima atualizada para: {confidence_pad_level}")
                        break
                    else:
                        print("Valor inválido. Digite um número entre 0.0 e 1.0.")
                except ValueError:
                        print("Valor inválido. Digite um número entre 0.0 e 1.0.")

        elif decision == "2":
            print("\n--Analisar fotos:")
            nome_pasta = perguntar_pasta()
            analisar_fotos(nome_pasta, confidence_pad_level)
















if __name__ == "__main__":
    main()
