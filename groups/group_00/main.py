"""
PhotoCensus - Group 01 (TEMPLATE)

Copy this folder to /groups/group_XX/ (XX = your group number)
and write your project here. Do not modify anything in /kit.
"""
import os
import sys

# Lets this file find black_box.py in /kit (do not remove these lines)
GROUP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(GROUP_DIR, "..", "..", "kit"))
from black_box import *  # noqa: E402,F401,F403


def load_collection():
    resultados = {}

    folders = list_folders()

    total_photos = 0
    total_detections = 0

    for folder in folders:
        photos = list_photos(folder)

        for photo in photos:
            detections = detect(photo)

            resultados[photo] = detections

            total_photos += 1
            total_detections += len(detections)

    print("=== RESUMO DO ACERVO ===")
    print("Pastas:", len(folders))
    print("Fotos:", total_photos)
    print("Detecções:", total_detections)

    return resultados

def ler_inteiro(mensagem):
    while True:
        entrada = input(mensagem)
        if entrada.isdigit():
            return int(entrada)
        print("Entrada inválida. Por favor digite um número inteiro.")

def filter_detections(detections, min_confidence):
    filtered = []
    for class_name, confidence in detections:
        if confidence >= min_confidence:
            filtered.append((class_name, confidence))
    return filtered


def build_inventory(resultados, photos, min_confidence):
    inventory = {}
    for photo in photos:
        detections = filter_detections(resultados[photo], min_confidence)
        for class_name, confidence in detections:
            if class_name in inventory:
                inventory[class_name] += 1
            else:
                inventory[class_name] = 1
    return inventory



def show_inventory(inventory):
    if len(inventory) == 0:
        print("Nenhum objeto encontrado.")
        return
    for class_name, amount in inventory.items():
        print(f"{class_name}: {amount}")

def bubble_sort_desc(ranking):
    '''Ordena a lista de tuplas (classe, quantidade) em ordem decrescente (bolha).'''
    for i in range(len(ranking)-1):
        for j in range(len(ranking) -1 -i):
            if ranking[j][1] < ranking[j + 1][1]:
                ranking[j], ranking[j + 1] = ranking[j + 1], ranking[j]
    return ranking

def ask_top_n(total):
    """Pede o N até ser um inteiro entre 1 e o total de classes."""
    n = input(f"Quantas classes deseja ver (1-{total})? ")
    while not (n.isdigit() and 1 <= int(n) <= total):
        n = input(f"Inválido! Digite um inteiro entre 1 e {total}: ")
    return int(n)

def top_n_ranking(inventory):
    """Requisito 4: converte o inventário em lista, ordena e mostra o Top N."""
    ranking = bubble_sort_desc(list(inventory.items()))
    if not ranking:
        print("Nenhum objeto encontrado.")
        return ranking

    n = ask_top_n(len(ranking))
    print(f"\n=== Top {n} classes ===")
    for pos in range(n):
        print(f"{pos + 1}. {ranking[pos][0]}: {ranking[pos][1]}")
    return ranking

def build_reverse_index(resultados, min_confidence):
    """Monta o índice reverso {classe: [fotos onde ela aparece]}."""
    index = {}
    for photo in resultados:
        for class_name, confidence in filter_detections(resultados[photo], min_confidence):
            if class_name not in index:
                index[class_name] = []
            if photo not in index[class_name]:
                index[class_name].append(photo)
    return index

def reverse_search(resultados, min_confidence):
    """Requisito 5: mostra as fotos onde uma classe aparece e quantas vezes."""
    index = build_reverse_index(resultados, min_confidence)
    print("Classes disponíveis:", ", ".join(index))
    class_name = input("Digite a classe: ").strip().lower()

    if class_name not in index:
        print(f"Classe '{class_name}' não encontrada com confiança >= {min_confidence}.")
        return

    print(f"\n=== Fotos com '{class_name}' ({len(index[class_name])}) ===")
    for photo in index[class_name]:
        amount = 0
        for name, confidence in filter_detections(resultados[photo], min_confidence):
            if name == class_name:
                amount += 1
        print(f"{os.path.basename(photo)}: {amount}")

def folder_classes(resultados, folder, min_confidence):
    """Devolve o conjunto (set) de classes distintas de uma pasta."""
    classes = set()
    for photo in list_photos(folder):
        for class_name, confidence in filter_detections(resultados[photo], min_confidence):
            classes.add(class_name)
    return classes

def ask_folder(message):
    """Pede o nome da pasta até ela existir."""
    folder = input(message).strip()
    while not folder_exists(folder):
        folder = input("Pasta inválida. Digite de novo: ").strip()
    return folder

def compare_folders(resultados, min_confidence):
    """Requisito 6: compara as classes de duas pastas usando conjuntos."""
    show_folders()
    folder1 = ask_folder("Primeira pasta: ")
    folder2 = ask_folder("Segunda pasta: ")
    set1 = folder_classes(resultados, folder1, min_confidence)
    set2 = folder_classes(resultados, folder2, min_confidence)

    results = [
        ("Em comum", set1 & set2),
        (f"Só em {folder1}", set1 - set2),
        (f"Só em {folder2}", set2 - set1),
        ("União", set1 | set2),
    ]
    for title, classes in results:
        print(f"{title} ({len(classes)}): {', '.join(classes) or 'nenhuma'}")

def build_matrix(resultados, folders, classes, min_confidence):
    """Monta a matriz: cada linha é uma pasta, cada coluna é uma classe."""
    matrix = []
    for folder in folders:
        inventory = build_inventory(resultados, list_photos(folder), min_confidence)
        row = []
        for class_name in classes:
            row.append(inventory.get(class_name, 0))
        matrix.append(row)
    return matrix

def show_matrix(resultados, min_confidence):
    """Requisito 7: imprime a matriz pasta x classe com totais e o maior valor."""
    folders = list_folders()
    classes = list(build_inventory(resultados, list(resultados), min_confidence))
    if not classes:
        print("Nenhum objeto encontrado.")
        return

    matrix = build_matrix(resultados, folders, classes, min_confidence)

    # cabeçalho (nomes das classes cortados em 7 letras para alinhar)
    print(f"{'':<13}" + "".join(f"{name[:7]:>8}" for name in classes) + f"{'Total':>8}")

    col_totals = [0] * len(classes)
    best_value, best_folder, best_class = 0, "", ""

    for i in range(len(folders)):
        line = f"{folders[i]:<13}"
        row_total = 0
        for j in range(len(classes)):
            value = matrix[i][j]
            line += f"{value:>8}"
            row_total += value
            col_totals[j] += value
            # guarda a maior combinação (pasta, classe)
            if value > best_value:
                best_value, best_folder, best_class = value, folders[i], classes[j]
        print(line + f"{row_total:>8}")

    print(f"{'Total':<13}" + "".join(f"{total:>8}" for total in col_totals))
    print(f"\nMaior valor: {best_class} na pasta {best_folder} ({best_value})")

def create_report_text(inventory, ranking):
    """Monta o conteúdo do relatório e devolve como texto."""
    lines = []
    lines.append("RELATÓRIO DO ACERVO")
    lines.append("===================")
    lines.append("")
    lines.append("INVENTÁRIO:")

    for class_name, amount in inventory.items():
        lines.append(f"{class_name}: {amount}")

    lines.append("")
    lines.append("RANKING:")

    position = 1
    for class_name, amount in ranking:
        lines.append(f"{position}. {class_name}: {amount}")
        position += 1

    return "\n".join(lines)


def save_report(inventory, ranking):
    """Salva inventário e ranking no arquivo report.txt."""
    report_text = create_report_text(inventory, ranking)

    with open("report.txt", "w", encoding="utf-8") as file:
        file.write(report_text)
    
    print("Relatório salvo em report.txt.")



def read_report():
    """Lê report.txt e devolve o conteúdo."""
    try:
        with open("report.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "O arquivo report.txt ainda não foi criado."


def show_inventory_histogram(ranking):
    """Exibe as classes em ordem do ranking, com barras de #."""
    if not ranking:
        print("Nenhum objeto encontrado.")
        return

    print("\n=== HISTOGRAMA DO INVENTÁRIO ===")

    for class_name, amount in ranking:
        bar = "#" * amount
        print(f"{class_name:<15} {amount:>4} | {bar}")

def analyze_photo(nivel_confianca):
    """lógica que estava dentro da opção 2."""
    print("Você escolheu analisar uma foto")
    print("-" * 30)
    show_folders()
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
        numero = ler_inteiro("Digite novamente: ")
    
    # Guardando resultado (Caminho) na variavel foto
    foto = photo_name(pasta, numero)
    quantidade = count_objects(foto, nivel_confianca)
    
    principal = main_object(foto)
    maior_confianca = max_confidence(foto)
    porcentagem = maior_confianca * 100
    
    print(f"Caminho: {foto}")
    print(f"Quantidade de objetos: {quantidade}")
    print(f"Objeto principal: {principal}")
    print(f"Maior confiança: {porcentagem:.0f} %")
    print('-'*30)
    print("Confiança mínima:", nivel_confianca)

def show_folder_report(nivel_confianca):
    """lógica que estava dentro da opção 4."""
    print("Você escolheu relatório da pasta")
    print("-" * 30)
    
    # choose folder  
    # Escolhendo a pasta validada com um while
    show_folders()
    folder = input('Digite o nome da pasta: ').strip()
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
    for number in range(1, total + 1):
        photo = photo_name(folder, number)
        amount = count_objects(photo, nivel_confianca)
        print(f'Foto {number}: {amount} objeto(s)')
        total_objects += amount 
        if amount == 0:
            empty_photos += 1
    
    # average of objects per photo
    # média de objetos por foto 
    avarage = total_objects / total
                    
    print('-' * 30)
    print('Total geral de objetos:', total_objects)
    print(f'Média de objetos por foto: {avarage:.2f}')
    print('Fotos sem nenhum objeto:', empty_photos)
    print('-' * 30)


def main():
    nivel_confianca = 0.5
    print("PhotoCensus - Group 01")
    resultados = load_collection()
    show_folders()
    # Your menu (while loop) starts here...
    while True:
        print("=== PHOTOS CENSUS ===")
        print(" 1 - Configurar confiança.")
        print(" 2 - Analisar uma foto.")
        print(" 3 - Contar uma classe.")
        print(" 4 - Relatório da pasta.")
        print(" 5 - Foto mais cheia e mais vazia. ")
        print(" 6 - Procurar uma classe. ")
        print(" 7 - Gráfico de barras. ")
        print(" 8 - Carregar acervo.")
        print(" 9 - Detecções de uma foto.")
        print(" 10 - Inventário.")
        print(" 11 - Ranking Top N.")
        print(" 12 - Busca reversa.")
        print(" 13 - Comparar pastas.")
        print(" 14 - Matriz pasta x classe.")
        print(" 15 - Histograma em texto.")
        print(" 16 - Salvar relatório.")
        print(" 17 - Ler relatório.")
        print(" 0 - Sair. ")
        
        
        option = input("Escolha uma opção: ")
        if option.isdigit():
            option = int(option)
        
        else:
            print("Opção inválida. Digite um número inteiro entre 0 e 14.")
            continue
        
        if option == 0:
            print("Programa encerrado!")
            break

        elif option == 1:
            print("Você escolheu configurar confianca")
            print("-" *30)

            while True:
                try:
                    confianca = float(input('Digite o nível de confiança:  '))
                    if confianca < 0 or confianca > 1:
                        print("Confiança inválida! Digite um número entre 0 e 1")
                        continue
                
                    break

                except ValueError:
                    print("Entrada inválida! Digite apenas números.")
           
            nivel_confianca = confianca

        elif option == 2:
            analyze_photo(nivel_confianca)
            

        elif option == 3:
            print("Você escolheu contar uma classe")
            print("-" * 30)
            show_folders()
            print('='*70)
            show_classes()
            print('='*70)
            
            folder = input("Digite o nome da pasta: ")
            
            while not folder_exists(folder):
                print("Pasta inválida!")
                folder = input("Digite novamente: ")
            
            total = total_photos(folder)

            number = ler_inteiro("Digite o número da foto: ")
            
            # Validando o número digitado 
            while number < 1 or number > total:
                print("Número inválido!")
                number = ler_inteiro("Digite novamente: ")

            photo = photo_name(folder, number)
            class_name = input("Digite a classe que deseja procurar: ")
            quantity = count_class(photo, class_name, nivel_confianca)

            print(f"Quantidade encontrada: {quantity}")
            print('-'*30)
 
        elif option == 4:
            show_folder_report(nivel_confianca)
                

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
            show_folders()
            print('='*70)
            show_classes()
            print('='*70)  
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
                quantidade = count_class(photo,class_name,nivel_confianca)
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
            print(f"Porcentagem: {porcentagem:.2f} %")
            print('-'*30)

        elif option == 7:
            print("Você escolheu gráfico de barras")
            print("-"*30)
            show_folders()
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
                nome = os.path.splitext(os.path.basename(foto))[0]
                print(f"{nome} | ", end="")
            #imprimi um # para cada objeto
                for i in range(quantidade):
                    print("#", end=" ")
                print(f" ({quantidade})")
            print("-" * 30)


        elif option == 8:
             resultados = load_collection()

        elif option == 9:
            show_folders()
            folder = input("Digite o nome da pasta: ")
            while not folder_exists(folder):
                print("Pasta inválida")
                folder = input("Digite o nome da pasta novamente:  ")

            number = ler_inteiro("Digite o número da foto: ")
            total = total_photos(folder)
            # Validando o número digitado 
            while number < 1 or number > total:
                print("Número inválido!")
                number = ler_inteiro("Digite novamente: ")



            foto = photo_name(folder, number)
            deteccoes = detect(foto)
            filtradas = filter_detections(deteccoes, nivel_confianca)

            print(f"Detecções em {foto} (confiança >= {nivel_confianca}):")
            if not filtradas:
                print("Nenhum objeto encontrado com esse nível de confiança.")
            else:
                for classe, confianca in filtradas:
                    print(f"- {classe}: {confianca:.2f}")


        elif option == 10:
            choice = input("Inventário do acervo inteiro (A) ou de uma pasta (P)? ").strip().upper()
            while choice != "A" and choice != "P":
                choice = input("Opção inválida. Digite A ou P: ").strip().upper()

            if choice == "A":
                photos = list(resultados.keys())

            else:
                show_folders()
                folder = input("Pasta: ").strip()
                
                while not folder_exists(folder):
                    folder = input("Pasta inválida. Digite de novo: ").strip()
                photos = list_photos(folder)

            inventory = build_inventory(resultados, photos, nivel_confianca)
            show_inventory(inventory)
            
        elif option == 11:
            inventory = build_inventory(resultados, list(resultados), nivel_confianca)
            top_n_ranking(inventory)
        
        elif option == 12:
            reverse_search(resultados, nivel_confianca)

        elif option == 13:
            compare_folders(resultados, nivel_confianca)

        elif option == 14:
            show_matrix(resultados, nivel_confianca)

        elif option == 15:
            inventory = build_inventory(resultados,list(resultados),nivel_confianca)

            ranking = bubble_sort_desc(list(inventory.items()))
            show_inventory_histogram(ranking)
        
        
        elif option == 16:
            inventory = build_inventory(resultados,list(resultados),nivel_confianca)
            ranking = bubble_sort_desc(list(inventory.items()))
            save_report(inventory, ranking)

        elif option == 17:
            print(read_report())

        
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()
