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

#Input

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
    # Pede o número da foto e verifica se está dentro do intervalo disponível.
    total = total_photos(folder)

    if total == 0:
        print("Essa pasta não possui fotos.")
        return None

    while True:
        try:
            number = int(input(f"Escolha uma foto (de 1 a {total}): "))
            if 1 <= number <= total:
                return photo_name(folder, number)
            print(MSG_INVALID)
        except ValueError:
            print(MSG_INVALID)


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


#Dados e filtro

def filter_detections(detections, confidence):
    # Mantém apenas as detecções que atingem a confiança mínima.
    filtered = []

    for class_name, score in detections:
        if score >= confidence:
            filtered.append((class_name, score))

    return filtered


def load_collection():
    # Carrega as detecções de todas as fotos uma única vez.
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

    print("\n=== ACERVO ===")
    print(f"Pastas: {folder_count}")
    print(f"Fotos: {photo_count}")
    print(f"Detecções: {detection_count}")

    return results


#Analise de foto e pasta (1)

def show_photo_summary(photo, confidence, results): #requisito 4
    # Mostra as principais informações detectadas na foto.
    detections = results[photo]
    filtered = filter_detections(detections, confidence)

    print(f"Caminho: {photo}")
    print(f"Objetos detectados: {len(filtered)}")

    if len(filtered) > 0:
      main_class = filtered[0][0]
      highest_score = filtered[0][1]

      for class_name, score in filtered:
        if score > highest_score:
          highest_score = score
          main_class = class_name
      
      print(f"Objeto de maior confiança: {main_class}")
      print(f"Maior confiança: {highest_score *100:.0f}%")
    
    else:
      print(f"Objeto de maior confiança: Nenhum")
      print("Maior confiança: 0%")


def count_photo_class(confidence, photo, results): #requisito 5
    #imprime a quantidade de objetos com a mesma classe na foto
    show_classes()
    class_name = input("Digite uma classe para buscar objetos: ")

    detections = results[photo]
    filtered = filter_detections(detections, confidence)

    amount = 0
    for detected_class, score in filtered:
      if detected_class == class_name:
        amount += 1
    print(f"Há {amount} objetos com a classe {class_name}")


def report_folder(folder, confidence, results):
    # Conta os objetos detectados em cada foto da pasta.
    photos = list_photos(folder)
    empty = 0
    total = 0

    for photo in photos:
        filtered = filter_detections(results[photo], confidence)
        objects = len(filtered)
        print(f"{photo}: {objects}")

        total += objects
        if objects == 0:
            empty += 1

    print(f"Total de objetos: {total}")
    print(f"Fotos sem nenhum objeto: {empty}")

    if len(photos) > 0:
        average = total / len(photos)
        print(f"Média de objetos por foto: {average:.2f}")


def find_fullest_emptiest(folder, confidence, results):
    # Compara a quantidade de objetos detectados em cada foto.
    photos = list_photos(folder)

    if len(photos) == 0:
        print("Essa pasta não possui fotos.")
        return

    fullest_photo = photos[0]
    emptiest_photo = photos[0]

    first_filtered = filter_detections(results[photos[0]], confidence)
    fullest_objects = len(first_filtered)
    emptiest_objects = len(first_filtered)

    for photo in photos[1:]:
        filtered = filter_detections(results[photo], confidence)
        objects = len(filtered)

        if objects > fullest_objects:
            fullest_objects = objects
            fullest_photo = photo

        if objects < emptiest_objects:
            emptiest_objects = objects
            emptiest_photo = photo

    print(f"Foto com mais objetos: {fullest_photo}\nTotal: {fullest_objects}")
    print(f"Foto com menos objetos: {emptiest_photo}\nTotal: {emptiest_objects}")


def find_class_in_folder(folder, confidence, results):
    show_classes()
    class_name = input("Escolha uma classe: ")
    photos = list_photos(folder)

    photo_with_class = 0
    total_objects = 0

    for photo in photos:
        filtered = filter_detections(results[photo], confidence)
        class_count = 0

        for detected_class, score in filtered:
            if detected_class == class_name:
                class_count += 1

        if class_count > 0:
            photo_with_class += 1
            total_objects += class_count

    print(f"A classe aparece em {photo_with_class} fotos")
    print(f"Total de objetos com a classe: {total_objects}")

    if len(photos) > 0:
        percentage = (photo_with_class / len(photos)) * 100
        print(f"A classe está presente em {percentage:.1f}% da pasta")


def show_bar_chart(folder, confidence, results): #requisito 9
    photos = list_photos(folder)

    # Monta uma barra de # para cada objeto detectado em cada foto.
    for photo in photos:
        detections = results[photo]
        filtered = filter_detections(detections,confidence)

        total_objects = len(filtered)
        chart = "#" * total_objects

        print(f"{photo} | {chart} ({total_objects})")


#Inventario

def create_inventory(results, confidence, folder = None):
  inventory = {}

  for photo, detections in results.items():

    if folder is None or os.path.basename(os.path.dirname(photo)) == folder:
      filtered = filter_detections(detections, confidence)
      for class_name, score in filtered:
        if class_name in inventory: 
          inventory[class_name] += 1
        else:
          inventory[class_name] = 1

  return inventory


def show_inventory(inventory):
    print("\n=== INVENTÁRIO DE CLASSES ===")

    if len(inventory) == 0:
        print("Nenhuma detecção encontrada.")
        return

    for class_name, amount in inventory.items():
        print(f"{class_name}: {amount}")

#Ranking

def create_ranking(inventory, limit):
  ranking = []

  for class_name, amount in inventory.items():
    ranking.append((class_name, amount))

  for a in range(len(ranking)):
    for b in range(len(ranking) - 1 - a):
      if ranking[b][1] < ranking[b + 1][1]:
        ranking[b], ranking[b + 1] = ranking[b + 1], ranking[b]

  ranking = ranking[:limit]
  return ranking


def show_ranking(ranking):
  print("\n===RANKING DE CLASSES===")
  if len(ranking) == 0:
    print("Nenhuma classe encontrada.")
    return
  
  position = 1

  for class_name, amount in ranking:
    print(f"{position}º - {class_name}: {amount}")
    position += 1


def ranking_analysis(confidence, results):
 
    print("\n1 - Ranking geral")
    print("2 - Ranking de uma pasta")

    option = input("Escolha uma opção: ")

    if option == "1":
        inventory = create_inventory(results, confidence)

    elif option == "2":
        folder = choose_folder()
        inventory = create_inventory(results, confidence, folder)

    else:
        print(MSG_INVALID)
        return

    # Pergunta quantas posições o ranking deve mostrar
    while True:
        try:
            limit = int(input("Quantas posições deseja mostrar? "))

            if limit > 0:
                break

            print(MSG_INVALID)

        except ValueError:
            print(MSG_INVALID)

    # Cria e mostra o ranking
    ranking = create_ranking(inventory, limit)
    show_ranking(ranking)


#Busca reversa

def create_reverse_index(results, confidence):
    # Dicionário que relaciona classes às fotos
    reverse_index = {}

    # Percorre todas as fotos
    for photo, detections in results.items():

        # Filtra as detecções pela confiança mínima
        filtered = filter_detections(detections, confidence)

        # Percorre as classes encontradas na foto
        for class_name, score in filtered:

            # Se a classe ainda não existe, cria uma lista
            if class_name not in reverse_index:
                reverse_index[class_name] = []

            # Adiciona a foto à lista daquela classe
            if photo not in reverse_index[class_name]:
                reverse_index[class_name].append(photo)

    return reverse_index


def search_class(reverse_index):
    # Mostra as classes disponíveis
    print("\n=== CLASSES DISPONÍVEIS ===")

    for class_name in reverse_index:
        print(class_name)

    # Pergunta qual classe o usuário deseja procurar
    class_name = input("\nDigite a classe que deseja buscar: ")

    # Verifica se a classe existe no índice
    if class_name in reverse_index:
        photos = reverse_index[class_name]

        print(f"\nA classe {class_name} aparece em {len(photos)} fotos:")

        # Mostra as fotos encontradas
        for photo in photos:
            print(photo)
    else:
        print("Essa classe não foi encontrada.")


def analyze_reverse_search(confidence, results):
    # Cria o índice reverso com a confiança atual
    reverse_index = create_reverse_index(results, confidence)

    # Faz a busca pela classe escolhida
    search_class(reverse_index)


#Comparação

def get_folder_classes(folder, results, confidence):
    # Cria um conjunto vazio de classes
    classes = set()

    # Percorre todas as fotos da pasta
    photos = list_photos(folder)

    for photo in photos:
        # Busca as detecções da foto
        detections = results[photo]

        # Aplica a confiança mínima
        filtered = filter_detections(detections, confidence)

        # Adiciona as classes ao conjunto
        for class_name, score in filtered:
            classes.add(class_name)

    return classes


def compare_folders(folder_1, folder_2):

  common = folder_1.intersection(folder_2)

  just_1 = folder_1.difference(folder_2)

  just_2 = folder_2.difference(folder_1)

  all_classes = folder_1.union(folder_2)

  return common, just_1, just_2, all_classes


def analyze_folder_comparison(results, confidence):
    # Escolhe as duas pastas
    print("\nEscolha a primeira pasta:")
    folder_1 = choose_folder()

    print("\nEscolha a segunda pasta:")
    folder_2 = choose_folder()

    # Verifica se as pastas são diferentes
    if folder_1 == folder_2:
        print("Escolha duas pastas diferentes!")
        return

    # Busca as classes de cada pasta
    classes_1 = get_folder_classes(folder_1, results, confidence)
    classes_2 = get_folder_classes(folder_2, results, confidence)

    # Compara os conjuntos
    common, just_1, just_2, all_classes = compare_folders(classes_1, classes_2)

    # Mostra os resultados
    print("\n=== COMPARAÇÃO DE PASTAS ===")
    print(f"Classes em comum: {common}")
    print(f"Exclusivas de {folder_1}: {just_1}")
    print(f"Exclusivas de {folder_2}: {just_2}")
    print(f"União das classes: {all_classes}")


#Matriz pasta x classe

def create_matrix(results, confidence):
    # Pega todas as pastas do acervo
    folders = list_folders()

    # Lista que guardará todas as classes diferentes
    classes = []

    # Descobre quais classes aparecem no acervo
    for folder in folders:
        photos = list_photos(folder)

        for photo in photos:
            detections = results[photo]
            filtered = filter_detections(detections, confidence)

            for class_name, score in filtered:
                if class_name not in classes:
                    classes.append(class_name)

    # Cria a matriz preenchida inicialmente com zeros
    matrix = []

    for folder in folders:
        row = []

        for class_name in classes:
            row.append(0)

        matrix.append(row)

    # Preenche a matriz contando as detecções
    for i in range(len(folders)):
        photos = list_photos(folders[i])

        for photo in photos:
            detections = results[photo]
            filtered = filter_detections(detections, confidence)

            for detected_class, score in filtered:
                for j in range(len(classes)):
                    if detected_class == classes[j]:
                        matrix[i][j] += 1

    return folders, classes, matrix


def show_matrix(folders, classes, matrix):
    print("\n=== MATRIZ DE PASTAS POR CLASSES ===")

    if len(classes) == 0:
        print("Nenhuma detecção encontrada.")
        return

    # Mostra o cabeçalho com os nomes das classes
    print(f"{'PASTA':<15}", end="")

    for class_name in classes:
        print(f"{class_name:<15}", end="")

    print(f"{'TOTAL':<10}")

    # Guarda o total de cada coluna
    column_totals = []

    for j in range(len(classes)):
        column_totals.append(0)

    # Mostra cada linha e calcula o total da pasta
    for i in range(len(folders)):
        row_total = 0

        print(f"{folders[i]:<15}", end="")

        for j in range(len(classes)):
            amount = matrix[i][j]

            print(f"{amount:<15}", end="")

            row_total += amount
            column_totals[j] += amount

        print(f"{row_total:<10}")

    # Mostra os totais de cada classe
    print(f"{'TOTAL':<15}", end="")

    for amount in column_totals:
        print(f"{amount:<15}", end="")

    print()

    # Procura a maior combinação de pasta e classe
    highest_amount = 0
    highest_folder = ""
    highest_class = ""

    for i in range(len(folders)):
        for j in range(len(classes)):
            if matrix[i][j] > highest_amount:
                highest_amount = matrix[i][j]
                highest_folder = folders[i]
                highest_class = classes[j]

    if highest_amount > 0:
        print("\n=== MAIOR COMBINAÇÃO ===")
        print(f"Pasta: {highest_folder}")
        print(f"Classe: {highest_class}")
        print(f"Quantidade: {highest_amount}")
    else:
        print("\nNenhuma detecção encontrada na matriz.")


def matrix_analysis(confidence, results):
    folders, classes, matrix = create_matrix(results, confidence)

    show_matrix(folders, classes, matrix)


#Histograma

def show_hist(ranking):

  for class_name, amount in ranking:
    bar = '#' * amount
    print (f'{class_name} | {bar} ({amount})')


def histogram_analysis(confidence, results):
    # Cria o inventário geral
    inventory = create_inventory(results, confidence)

    # Cria o ranking de todas as classes
    ranking = create_ranking(inventory, len(inventory))

    # Mostra o histograma
    print("\n=== HISTOGRAMA DE CLASSES ===")
    show_hist(ranking)


#Relátorio em arquivo

def report_analysis(confidence, results):
    # Cria o inventário geral
    inventory = create_inventory(results, confidence)

    # Cria o ranking completo
    ranking = create_ranking(inventory, len(inventory))

    # Salva as informações no arquivo
    save_report(inventory, ranking)


def save_report(inventory, ranking):
    # Salva o relatório na pasta do projeto.
    report_path = os.path.join(GROUP_DIR, "report.txt")

    with open(report_path, "w", encoding="utf-8") as file:
        file.write("==== PHOTO CENSUS ====\n")
        file.write("==== RELATÓRIO ====\n")
        file.write("\n=== INVENTÁRIO ===\n")

        for class_name, amount in inventory.items():
            file.write(f"{class_name}: {amount}\n")

        file.write("\n=== RANKING ===\n")
        position = 1

        for class_name, amount in ranking:
            file.write(f"{position} - {class_name}: {amount}\n")
            position += 1

    print("Relatório salvo com sucesso!")


def read_report():
    report_path = os.path.join(GROUP_DIR, "report.txt")

    try:
        with open(report_path, "r", encoding="utf-8") as file:
            content = file.read()
        print(content)
    except FileNotFoundError:
        print("Nenhum relatório foi encontrado.")


#Analise (inventario)

def inventory_analysis(confidence, results):
    print("\n1 - Inventário geral")
    print("2 - Inventário de uma pasta")

    option = input("Escolha uma opção: ")

    if option == "1":
        inventory = create_inventory(results, confidence)
    elif option == "2":
        folder = choose_folder()
        inventory = create_inventory(results, confidence, folder)
    else:
        print(MSG_INVALID)
        return

    show_inventory(inventory)


#MENUS

def show_menu(confidence): #menu principal
    print('\n--- OPTIONS ---')
    print(f'-- Confiança Mínima atual {confidence}--\n')
    print('1 - configurar a confiança mínima')
    print('2 - Analisar uma foto')
    print('3 - Analisar uma pasta')
    print('4 - Mostrar inventário de classes')
    print('5 - Mostrar ranking top N')
    print('6 - Busca reversa por classe')
    print('7 - Comparar duas pastas')
    print('8 - Mostrar matriz de pastas por classes')
    print('9 - Mostrar histograma de classes')
    print("10 - Gerar relatório")
    print("11 - Ler relatório salvo")
    print('0 - Sair')
    return input("Escolha uma opção: ")


def analyze_photo(confidence, results):
    folder = choose_folder()
    photo = choose_photo(folder)

    if photo is None:
        return

    while True:
        print("\n1 - Análise geral")
        print("2 - Contar uma classe")
        option = input("Escolha uma opção: ")

        if option == "1":
            show_photo_summary(photo, confidence, results)
            break
        elif option == "2":
            count_photo_class(confidence, photo, results)
            break
        else:
            print(MSG_INVALID)


def analyze_folder(confidence, results):
    folder = choose_folder()

    # Repete o menu até uma das análises da pasta ser escolhida.
    while True:
        print("1 - Relatório da pasta")
        print("2 - Foto mais cheia e mais vazia")
        print("3 - Procurar uma classe na pasta")
        print("4 - Gráfico de barras em texto")

        option = input("Escolha uma opção: ")

        if option == "1":
            report_folder(folder, confidence, results)
            break
        elif option == "2":
            find_fullest_emptiest(folder,confidence, results)
            break
        elif option == "3":
            find_class_in_folder(folder,confidence, results)
            break
        elif option == "4":
            show_bar_chart(folder, confidence, results)
            break
        else:
            print(MSG_INVALID)


#Principal

def main():
    print("PhotoCensus - Group 05")

    results = load_collection()
    show_folders()

    while True:
        option = show_menu(confidence)

        if option == "1":
            set_minimal_confidence()
        elif option == "2":
            analyze_photo(confidence, results)
        elif option == "3":
            analyze_folder(confidence, results)
        elif option == "4":
            inventory_analysis(confidence, results)
        elif option == "5":
            ranking_analysis(confidence, results)
        elif option == "6":
            analyze_reverse_search(confidence, results)
        elif option == "7":
            analyze_folder_comparison(results, confidence)
        elif option == "8":
            matrix_analysis(confidence, results)
        elif option == "9":
            histogram_analysis(confidence, results)
        elif option == "10":
            report_analysis(confidence, results)
        elif option == "11":
            read_report()
        elif option == "0":
            break
        else:
            print(MSG_INVALID)


if __name__ == "__main__":
    main()