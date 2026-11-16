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


def main():
    nivel_confianca = 0.5
    print("PhotoCensus - Group 01")
    show_folders()
    # Your menu (while loop) starts here...
    while True:
        print("=== PHOTOS CENSUS ===")
        print(" 1 - Configurar confiança.")
        print(" 2 - Anasilar uma foto.")
        print(" 3 - Contar uma classe.")
        print(" 4 - Relatório da pasta.")
        print(" 5 - Foto mais cheia e mais vazia. ")
        print(" 6 - Procurar uma classe. ")
        print(" 7 - Gráfico de barras. ")
        print(" 0 - Sair. ")

        def ler_inteiro(mensagem):
            while True:
                entrada = input(mensagem)
                if entrada.isdigit():
                    return int(entrada)
                print("Entrada inválida. Por favor digite um número inteiro.")
        
        
        option = input("Escolha uma opção: ")
        if option.isdigit():
            option = int(option)
        
        else:
            print("Opção inválida. Digite um número inteiro entre 0 e 7.")
            continue
        
        if option == 0:
            print("Programa encerrado!")
            break

        elif option == 1:
            print("Você escolheu configurar confianca")
            print("-" *30)
            confianca = input(" Digite o nível de confiança: ")

            if confianca.isdigit():
                confianca = float(confianca)
                
            else:
                confianca = float(input("Por favor. Digite um número entre 0 e 1."))

            while confianca < 0 or confianca > 1:
                print("Confiança inválida!")
                confianca = float(input("Digite novamente: "))
            nivel_confianca = confianca

        elif option == 2:
            print("Você escolheu analisar uma foto")
            print("-" * 30)
            pasta = input("Digite o nome da pasta: ")
            
            # Verificando se a pasta informada existe atraves do folder exists
            while not folder_exists(pasta):
                print("Pasta não encontrada!")
                pasta = input("Tente novamente: ")
            
            total = total_photos(pasta)
            numero = ler_inteiro("Digite o número da foto: ")
            
            # Validadando o número digitado
            while numero < 1 or numero > total:
                print("Número inválido!")
                numero = int(input("Digite novamente: "))

            # Guardando resultado (Caminho) na variavel foto
            foto = photo_name(pasta, numero)
            quantidade = count_objects(foto, nivel_confianca)

            principal = main_object(foto)
            maior_confianca = max_confidence(foto)
            porcentagem = maior_confianca * 100

            print(f"Caminho: {foto}")
            print(f"Quantidade de objetos: {quantidade}")
            print(f"Objeto principal: {principal}")
            print(f"Maior confiança: {porcentagem} %")
            

        elif option == 3:
            print("Você escolheu contar uma classe")
            print("-" * 30)
            
            folder = input("Digite o nome da pasta: ")
            
            while not folder_exists(folder):
                print("Pasta inválida!")
                folder = input("Digite novamente: ")
            
            total = total_photos(folder)

            number = ler_inteiro("Digite o número da foto: ")
            
            # Validando o número digitado 
            while number < 1 or number > total:
                print("Número inválido!")
                number = int(input("Digite novamente: "))

            photo = photo_name(folder, number)
            class_name = input("Digite a classe que deseja procurar: ")
            quantity = count_class(photo, class_name, nivel_confianca)

            print(f"Quantidade encontrada: {quantity}")
 
        elif option == 4:
            print("Você escolheu relatório da pasta")
            print("-" * 30)

            # choose folder  
            # Escolhendo a pasta validada com um while
            show_folders()
            folder = input('Digite o nome da pasta:').strip()
            while not folder_exists(folder):
                print('Pasta inválida! Tente novamente.')
                folder = input('Digite o nome da pasta:').strip()

            # total folder photos
            # total de fotos na pasta e contagem dos objetos com as fotos vazias
            total = total_photos(folder)
            total_objects = 0
            empty_photos = 0

            print(f'\nPasta: {folder} | Confiança mínima: {nivel_confianca}')
            print('-' * 30)

            # examination of the photos in the folders
            # examinação das fotos nas pastas ( iniciando em 1)
            number = 1 
            while number <= total:
                photo = photo_name(folder, number)
                amount = count_objects(photo, nivel_confianca)
                print(f'Foto {number}: {amount} objeto(s)')
                total_objects += amount 
                if amount == 0:
                    empty_photos = empty_photos + 1
                number += 1
            # average of objects per photo
            # média de objetos por foto 
            average = total_objects / total

            print('-' * 30)
            print('Total geral de objetos:', total_objects)
            print(f'Média de objetos por foto: {average:.2f}')
            print('Fotos sem nenhum objeto:', empty_photos)
            print('-' * 30)
            
            

        elif option == 5:
            print("Você escolheu foto mais cheia e mais vazia")
            print("-" * 30)

            show_folders()
            folder = input('Digite o nome da pasta: ').strip()
            while not folder_exists(folder):
                print('Pasta inválida! Tente novamente.')
                folder = input('Digite o nome da pasta:').strip()

            # total photos in the folder
            # total de fotos na pasta
            total = total_photos(folder)

            # starting with the data of photo one
            # começando com os dados da foto 1 (para não inventar valor)
            first_photo = photo_name(folder, 1)
            highest_amount = count_objects(first_photo, nivel_confianca)
            highest_number = 1
            lowest_amount = highest_amount
            lowest_number = 1

            # analyze the remaining photos (from 2 to total)
            # analisar o restante das fotos (da segunda ao total)
            number = 2
            while number <= total:
                photo = photo_name(folder, number)
                amount = count_objects(photo, nivel_confianca)

                # new highest? (strict > keeps the first photo in case of a tie)
                # novo recorde? (estrito > mantém a primeira foto em caso de empate)
                if amount > highest_amount:
                    highest_amount = amount
                    highest_number = number

                # new lowest? (strict < keeps the first photo in case of a tie)
                # novo menor valor? (estrito < mantém a primeira foto em caso de empate)
                if amount < lowest_amount:
                    lowest_amount = amount
                    lowest_number = number
                number += 1

            # final result 
            # resultado final fora do laço
            print(f'\nPasta: {folder} | Confiança mínima: {nivel_confianca}')
            print('------------------------------------')
            print(f'Foto mais cheia: nº {highest_number} com {highest_amount} objeto(s)')
            print('Caminho:', photo_name(folder, highest_number))
            print(f'Foto mais vazia: nº {lowest_number} com {lowest_amount} objeto(s)')
            print('Caminho:', photo_name(folder, lowest_number))
            print('------------------------------------')
             
            

        elif option == 6:
            print("Você escolheu procurar uma classe")
            print("-" * 30)
        #Receber as informaçoes
            folder = input("Digite o nome da pasta: ")  
            while not folder_exists(folder):
                print("Pasta inválida")
                folder = input("Digite o nome da pasta novamente: ")
            class_name = input("Digite a classe desejada: ")
        
            total_fotos = total_photos(folder)
        #inicia os cont
            fotos_com_classe = 0
            total_encontrado = 0
        # perrcorrer as fotos
            for numero in range(1, total_fotos +1):
                photo = photo_name(folder,numero)
                quantidade = count_class(photo,class_name)
                total_encontrado += quantidade
        #verificar se a classe apareceu
                if quantidade >0:
                    fotos_com_classe += 1
        #calcular a porcetagem
                porcentagem = (fotos_com_classe/total_fotos) * 100
        #resultados
            print(f"Total de fotos: {total_fotos}")
            print(f"Fotos com {class_name}: {fotos_com_classe}")
            print(f"Total de objetos encontrados: {total_encontrado}")
            print(f"Porcentagem: {porcentagem} %")

        elif option == 7:
            print("Você escolheu gráfico de barras")
            print("-"*30)
        #recebe a informação    
            folder = input("Digite o nome da pasta: ")
            while not folder_exists(folder):
                print("Pasta inválida")
                folder = input("Digite o nome da pasta novamente:  ")
        #processamento
            total = total_photos(folder)
        #percorrer o total das fotos    
            for numero in range(1,total + 1):
                foto = photo_name(folder,numero)
                quantidade = count_objects(foto,nivel_confianca)
                print(f"{os.path.basename(foto)} | ", end="")
            #imprimi um # para cada objeto
                for i in range(quantidade):
                    print("#", end=" ")
                print(f"A quantidade de objetos foi: {quantidade}")
            print("-"* 30)

        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()
