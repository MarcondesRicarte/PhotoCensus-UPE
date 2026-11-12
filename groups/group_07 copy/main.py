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


def perguntar_folders():
    show_folders() 
    folder = input("Escolha uma pasta: ").strip()







def main():
    print("PhotoCensus - Group 07")

    print ("tudo inicou aqui!")
    

    confidence_pad_level:0.5
    
    
    
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

        decision = int(input('Escolha uma opção: '))

        if decision == "0":
         break
        elif decision == "1":
            print("\n--Escolha a confiança minima:")
            print(f"Confiança atual: {confidence_pad_level}")

        while True:
            try:
                confidence_pad_level = float(input("Digite a confiança minima (0.0 a 1.0): "))
                if 0.0 <= confidence_pad_level <= 1.0:
                    print(f"Confiança minima atualizada para: {confidence_pad_level}")
                    break
                else:
                    print("Por favor, digite um valor entre 0.0 e 1.0.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")
     
















if __name__ == "__main__":
    main()
