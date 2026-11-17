"""
PhotoCensus - Grupo 06
Módulo 1: sistema em console
"""
import os
import sys

# ---------------------------------------------------------------
# POR QUE USAMOS CAMINHOS DE PASTA AQUI?
# O black_box.py (as funções prontas do professor) fica na pasta "kit".
# O nosso main.py fica em outra pasta: "groups/group_06".
# Quando escrevemos "from black_box import *", o Python só procura o black_box.py
# em algumas pastas conhecidas (a lista chamada sys.path), e a pasta "kit" NÃO está nela.
# Sem as linhas abaixo dá erro: ModuleNotFoundError: No module named 'black_box'.
# Elas descobrem onde está este arquivo e ensinam ao Python o caminho da pasta "kit".
# ---------------------------------------------------------------

# Permite que este arquivo encontre o black_box.py na pasta /kit

# __file__ = caminho deste arquivo (main.py); o Python preenche sozinho
# os.path.abspath(...) = transforma em caminho COMPLETO (ex.: /content/PhotoCensus-UPE/groups/group_06/main.py)
# os.path.dirname(...) = fica só com a PASTA do arquivo (tira o "main.py") -> .../groups/group_06
GROUP_DIR = os.path.dirname(os.path.abspath(__file__))

# os.path.join(...) = junta pedaços de caminho (usa "/" ou "\" conforme o sistema: Linux ou Windows)
# ".." = "subir uma pasta":  groups/group_06  ->  groups  ->  raiz do projeto
# Então GROUP_DIR + ".." + ".." + "kit" aponta para a pasta kit, na raiz do projeto:
#   .../groups/group_06/../../kit   é o mesmo que   .../kit
# sys.path.append(...) = acrescenta essa pasta na lista onde o Python procura arquivos
# Usando o __file__, o caminho é calculado a partir do próprio arquivo e funciona de qualquer pasta.
sys.path.append(os.path.join(GROUP_DIR, "..", "..", "kit"))

# from black_box import * = traz todas as funções do black_box.py (folder_exists, count_objects...)
#   quer dizer "não avise sobre estes itens nesta linha":
from black_box import *  # noqa: E402,F401,F403



def show_menu(min_confidence):

    print("\n===== PHOTOCENSUS - GROUP 06 =====")

    print(f"Current minimum confidence: {min_confidence}")

    print("1 - Set minimum confidence")
    print("2 - Analyze a photo")
    print("3 - Count a class in a photo")
    print("4 - Folder report")
    print("5 - Fullest and emptiest photo")
    print("6 - Search a class in a folder")
    print("7 - Text bar chart")
    print("0 - Exit")
    print("====================================")


    # Função: listar pastas
    # 1: definir nivel mínimo de confiança
    # 2: analisar uma foto
    # 3: contar uma classe
    # 4: relatório da pasta
    # 5: encontrar foto com mais e menos objetos
    # 6: busca uma classe na pasta
    # 7: gráfico de barras texual
    # 0: sair

def ask_folder():
    # Pergunta até o usuário digitar uma pasta que existe (usa folder_exists do kit)
    # while not folder_exists = entra no laço quando a pasta não é encontrada

    show_folders()
    folder = input("Folder name: ").strip().lower()
    # .strip() remove espaços das pontas; .lower() deixa tudo em minúsculas

    while not folder_exists(folder):
        print("Folder not found! Try again.")
        folder = input("Folder name: ").strip().lower()

    return folder
    # retorna a pasta


def ask_photo_number(folder):

    # Pergunta qual foto deseja analisar (o número estar entre 1 e o total de fotos da pasta)

    total = total_photos(folder)
    print(f"Total photos: {total}")

    # input() devolve sempre TEXTO (str), mesmo que o usuário digite 3
    photo_analysis = input(f"Photo number (1 to {total}): ").strip()

    # .isdigit() = método de texto: devolve True se o texto tiver SÓ números (0 a 9)
    #   "3".isdigit()   -> True
    #   "abc".isdigit() -> False  (tem letra)
    #   "".isdigit()    -> False  (vazio)
    # Por que testar antes? Porque int("abc") dá erro e fecha o programa.
    #
    # A condição do while é lida da esquerda para a direita:
    # O int() só é executado se o texto já passou pelo isdigit() .

    while not photo_analysis.isdigit() or int(photo_analysis) < 1 or int(photo_analysis) > total:
        print("Invalid number! Try again.")
        photo_analysis = input(f"Photo number (1 to {total}): ").strip()

    return int(photo_analysis)  # converte o texto "3" no número 3


def ask_confidence():
    # Pergunta até o valor ser um número entre 0 e 1

    confidence_val = input("Minimum confidence (0 to 1): ").strip().replace(",", ".")
    # . replace("," , ".") = aceita "0,8" e "0.8" (troca a vírgula por ponto)

    # O texto pode ter um ponto decimal ("0.8"), mas para o isdigit() o ponto NÃO é número.
    # Então testamos uma cópia do texto sem o ponto:
    #   .replace(".", "", 1) = troca o PRIMEIRO "." por "" (apaga o ponto)
    #   o último valor (1) é quantas trocas fazer: só 1 ponto é aceito
    #   "0.8".replace(".", "", 1)   -> "08"   -> isdigit() True   (aceito)
    #   "0.8.5".replace(".", "", 1) -> "08.5" -> isdigit() False  (recusado)
    #   "abc", "-1" e ""            -> isdigit() False            (recusados)
    #
    # A condição do while é lida da esquerda para a direita:
    #   1) not ...isdigit()    -> não é número? então é inválido (o "or" já para aqui)
    #   2) float(confidence_val) > 1  -> é número, mas maior que 1
    # Não precisa testar "< 0": o sinal de menos já é recusado pelo isdigit().
    # O float() só é executado se o texto já passou pelo isdigit(), por isso nunca dá erro.

    while not confidence_val.replace(".", "", 1).isdigit() or float(confidence_val) > 1:
        print("Invalid value! Type a number between 0 and 1.")
        confidence_val = input("Minimum confidence (0 to 1): ").strip().replace(",", ".")

    return float(confidence_val)  # agora é seguro: converte o texto "0.8" no número 0.8


def main():


    print("PhotoCensus - Group 06")

    # Confiança mínima usada em todas as opções (começa em 0.5)
    min_confidence = 0.5

    # Começa diferente de "0" para o laço rodar pelo menos uma vez
    option = ""

    # while = repete o bloco abaixo enquanto a condição for verdadeira
    while option != "0":

        show_menu(min_confidence)

        option = input("Choose an option: ").strip()

        # escolhe o que fazer conforme a opção digitada

        if option == "0":
            print("Goodbye!")
        elif option == "1":
            # Requisito 3: alterar a confiança mínima
            min_confidence = ask_confidence()
            print(f"Minimum confidence set to {min_confidence}")

        elif option == "2":

            # Requisito 4: analisar uma foto
            folder = ask_folder()
            number = ask_photo_number(folder)
            photo = photo_name(folder, number)
            total_objects = count_objects(photo, min_confidence)
            # Renomeados para evitar conflito com as funções importadas
            detected_main_object = main_object(photo)
            detected_max_confidence = max_confidence(photo)

            print(f"\nPhoto: {photo}")
            print(f"Total objects: {total_objects}")
            print(f"Main object: {detected_main_object}")
            # :.0f = mostra o número sem casas decimais (0.89 * 100 -> 89)
            print(f"Highest confidence: {detected_max_confidence * 100:.0f}%")

        elif option == "3":
            # Contar quantos objetos de uma classe ha na foto
            folder = ask_folder()   # escolhe a pasta
            number = ask_photo_number(folder)  # escolhe o numero da foto
            photo = photo_name(folder, number)  # monta o caminho da foto

            print(f"\nPhoto: {photo}")

            classe_name = input("Enter a classe: ").strip().lower()
            # count_class devolve quantos objetos dessa classe a foto tem
            found = count_class(photo, classe_name, min_confidence)
                                           # maior que 0 = a classe aparece
            if found > 0:
                print(f"Class {classe_name} found! Quantity: {found}")
            else:
                print(f"Class {classe_name} not found in this photo. ")

        elif option == "4":
            # relatorio da pasta (for + acumuladores)
            folder = ask_folder()
            amount = total_photos(folder)

            total_objects = 0  # acumulador: soma os objetos de todas as fotos
            empty_photos = 0   # contador: quantas fotos ficaram com 0 objetos

            print(f"\n--- Report of folder {folder} ---")

            # range(1, amount + 1) vai de 1 até amount (o ultimo é excluido)
            for number in range(1, amount + 1):
                photo = photo_name(folder, number)
                objects = count_objects(photo, min_confidence)
                print(f"Photo {number}: {objects} object(s)")

                total_objects += objects   # soma os objetos
                if objects == 0:
                    empty_photos += 1      # conta a foto vazia

            # Média = total / numero de fotos (só divide se a pasta tiver fotos, para não dividir por zero)
            if amount > 0:
                average = total_objects / amount
            else:
                average = 0
            print(f"Total objects: {total_objects}")
            print(f"Average per photo: {average:.2f}")
            print(f"Photos with no objects: {empty_photos}")

        elif option == "5":
            # foto mais cheia e mais vazia
            folder = ask_folder()
            amount = total_photos(folder)

            if amount > 0:
                # começamos supondo que a foto 1 é a mais cheia e a mais vazia
                first_photo = photo_name(folder, 1)
                first_count = count_objects(first_photo, min_confidence)
                fullest_number = 1
                fullest_count = first_count
                emptiest_number = 1
                emptiest_count = first_count

                # comparamos da foto 2 ate a ultima com os "campeões" atuais
                for number in range(2, amount + 1):
                    photo = photo_name(folder, number)
                    objects = count_objects(photo, min_confidence)

                    if objects > fullest_count:   # achou uma mais cheia
                        fullest_count = objects
                        fullest_number = number

                    if objects < emptiest_count:   # achou uma mais vazia
                        emptiest_count = objects
                        emptiest_number = number

                print(f"\n--- Folder {folder} ---")
                print(f"Fullest photo: {fullest_number} with {fullest_count} object(s)")
                print(f"Emptiest photo: {emptiest_number} with {emptiest_count} object(s)")
            else:
                print("No photos found in folder.")

        elif option == "6":
            # procurar uma classe na pasta
            folder = ask_folder()
            classe_name = input("Enter a class: ").strip().lower()
            amount = total_photos(folder)  # quantas fotos a pasta tem

            photos_with_class = 0    # contador: em quantas fotos a classe aparece
            total_found = 0          # acumulador: total de objetos dessa classe

            for number in range(1, amount + 1):
                photo = photo_name(folder, number)
                # quantos objetos da classe essa foto tem
                found = count_class(photo, classe_name, min_confidence)
                total_found += found   # soma no total geral

                if found > 0:          # a classe apareceu nessa foto
                    photos_with_class += 1   # conta mais uma foto

            print(f"\nClass '{classe_name}' found in {photos_with_class} photo(s). Total occurrences: {total_found}")

            # porcentagem de fotos da pasta em que a classe aparece
            percent = 0
            if amount > 0:
                percent = photos_with_class / amount * 100
            print(f"Percentage of photos with the class: {percent:.1f}%")

        elif option == "7":
            # grafico de barras em texto (laços aninhados)
            folder = ask_folder()
            amount = total_photos(folder)    # quantas fotos a pasta tem

            print(f"\n--- Bar chart of folder {folder} ---")
            for number in range(1, amount + 1):     # laço de fora: cada foto
                photo = photo_name(folder, number)
                objects = count_objects(photo, min_confidence)

                # nome da foto: pasta + "_" + numero com 2 digitos (ex: street_04)
                file_name = f"{folder}_{number:02d}"
                print(f"{file_name:<15}|", end="")   # começa a linha sem pular

                for i in range(objects):      # laço de dentro: 1 # por objeto
                    print("#", end="")
                print(f"({objects})")         # termina a linha com o total
        else:
            # Qualquer outro texto é uma opção inválida
            print("Invalid option! Try again.")


# Só executa main() quando o arquivo é rodado diretamente (não quando é importado)
if __name__ == "__main__":
    main()
