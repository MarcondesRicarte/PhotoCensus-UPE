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
    print("PhotoCensus - Group 07")

# ---------- ENTRADAS ----------

def ask_int_in_range(prompt, low, high):
    """Repete até o usuário digitar um inteiro entre low e high."""
    while True:
        text = input(prompt).strip()
        if text.lstrip("-").isdigit() and low <= int(text) <= high:
            return int(text)
        print(f"Número inválido. Digite um número inteiro de {low} a {high}.")


def ask_class_name():
    """Pede o nome de uma classe (não aceita vazio)."""
    show_classes()
    name = input(CLASS_PROMPT).strip().lower()
    while not name:
        print("Você não digitou nada. Tente novamente.")
        name = input(CLASS_PROMPT).strip().lower()
    return name


def ask_folder():
    show_folders()
    while True:
        folder = input(FOLDER_PROMPT).strip()
        if folder and folder_exists(folder) and total_photos(folder) > 0:
            return folder
        print("Pasta inválida. Tente novamente.")


def ask_photo():
    folder = ask_folder()
    total = total_photos(folder)
    print(f"A pasta '{folder}' tem {total} fotos.")
    number = ask_int_in_range(f"Escolha o número da foto (1 a {total}): ", 1, total)
    return photo_name(folder, number)


# ---------- CARGA, FILTRO E INVENTÁRIO ----------

def load_collection():
    results = {}
    folder_photos = {}
    for folder in list_folders():
        photos = list_photos(folder)
        folder_photos[folder] = photos
        for photo in photos:
            results[photo] = detect(photo)
    return results, folder_photos


def filter_detections(detections, min_conf):
    return [d for d in detections if d[1] >= min_conf]


def show_summary(results, folder_photos, min_conf):
    all_count = 0
    kept_count = 0
    for photo, dets in results.items():
        all_count += len(dets)
        kept_count += len(filter_detections(dets, min_conf))

    print("\n--- Resumo do acervo ---")
    print(f"Pastas: {len(folder_photos)}")
    print(f"Fotos: {len(results)}")
    print(f"Detecções (a partir de 0.25): {all_count}")
    print(f"Detecções com confiança >= {min_conf}: {kept_count}")


def build_inventory(results, photos, min_conf):
    inventory = {}
    for photo in photos:
        for name, _ in filter_detections(results[photo], min_conf):
            inventory[name] = inventory.get(name, 0) + 1
    return inventory


def show_inventory(inventory, title):
    print(f"\n--- Inventário: {title} ---")
    if not inventory:
        print("Nenhum objeto com essa confiança mínima.")
        return

    total = 0
    for name, amount in inventory.items():
        print(f"{name}: {amount}")
        total += amount

    print(f"\nClasses distintas: {len(inventory)}")
    print(f"Total de objetos: {total}")


def build_ranking(results, min_conf):
    """Inventário do acervo inteiro já ordenado do maior para o menor."""
    inventory = build_inventory(results, list(results), min_conf)
    return inventory, sort_desc(list(inventory.items()))


# ---------- ORDENAÇÃO (sem sorted/.sort) ----------

def sort_desc(items):
    """Insertion sort decrescente pela quantidade (estável)."""
    ranking = list(items)
    for i in range(1, len(ranking)):
        current = ranking[i]
        j = i - 1
        while j >= 0 and ranking[j][1] < current[1]:
            ranking[j + 1] = ranking[j]
            j -= 1
        ranking[j + 1] = current
    return ranking


def sort_names(names):
    """Selection sort alfabético."""
    remaining = list(names)
    ordered = []
    while remaining:
        smallest = remaining[0]
        for name in remaining:
            if name < smallest:
                smallest = name
        remaining.remove(smallest)
        ordered.append(smallest)
    return ordered


# ---------- BUSCA REVERSA E CONJUNTOS ----------

def build_reverse_index(results, min_conf):
    index = {}
    for photo in results:
        for name, _ in filter_detections(results[photo], min_conf):
            photos_with_class = index.setdefault(name, [])
            if photo not in photos_with_class:
                photos_with_class.append(photo)
    return index


def count_class_in(detections, class_name):
    return len([1 for name, _ in detections if name == class_name])


def classes_of_folder(results, folder_photos, folder, min_conf):
    found = set()
    for photo in folder_photos[folder]:
        for name, _ in filter_detections(results[photo], min_conf):
            found.add(name)
    return found


def show_set(title, names):
    ordered = sort_names(names)
    text = ", ".join(ordered) if ordered else "nenhuma"
    print(f"{title} ({len(ordered)}): {text}")


# ---------- MATRIZ PASTA x CLASSE ----------

def build_matrix(results, folder_photos, min_conf, classes):
    matrix = []
    for folder in folder_photos:
        inventory = build_inventory(results, folder_photos[folder], min_conf)
        matrix.append([inventory.get(c, 0) for c in classes])
    return matrix


def matrix_totals(matrix):
    row_totals = []
    for row in matrix:
        acc = 0
        for value in row:
            acc += value
        row_totals.append(acc)

    column_totals = [0] * len(matrix[0])
    for row in matrix:
        for j, value in enumerate(row):
            column_totals[j] += value

    return row_totals, column_totals


def find_largest(matrix, folders, classes):
    best = (-1, "", "")
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value > best[0]:
                best = (value, folders[i], classes[j])
    return best


def print_matrix(folders, classes, matrix, row_totals, column_totals):
    grand_total = 0
    for t in row_totals:
        grand_total += t

    block_size = 6
    for start in range(0, len(classes), block_size):
        end = min_of(start + block_size, len(classes))
        is_last = end == len(classes)

        header = f"{'Pasta':<14}"
        for j in range(start, end):
            header += f"{classes[j][:12]:>13}"
        if is_last:
            header += f"{'Total':>8}"

        print("\n" + header)
        print("-" * len(header))

        for i, folder in enumerate(folders):
            line = f"{folder:<14}"
            for j in range(start, end):
                line += f"{matrix[i][j]:>13}"
            if is_last:
                line += f"{row_totals[i]:>8}"
            print(line)

        footer = f"{'TOTAL':<14}"
        for j in range(start, end):
            footer += f"{column_totals[j]:>13}"
        if is_last:
            footer += f"{grand_total:>8}"
        print(footer)


def min_of(a, b):
    """Menor de dois valores (min() é proibido)."""
    return a if a < b else b


# ---------- HISTOGRAMA E RELATÓRIO ----------

def print_histogram(ranking):
    biggest = ranking[0][1]
    step = 1
    if biggest > 50:
        step = -(-biggest // 50)  # divisão arredondada para cima
        print(f"(cada # = {step} objetos)")

    for name, amount in ranking:
        bars = amount // step or 1  # toda classe ganha ao menos um '#'
        print(f"{name:<15}| {'#' * bars} ({amount})")


def save_report(inventory, ranking, min_conf, path):
    lines = [
        "PhotoCensus - Relatório do acervo",
        f"Confiança mínima: {min_conf}",
        "",
        "INVENTÁRIO",
    ]
    for name, amount in inventory.items():
        lines.append(f"{name}: {amount}")

    lines.append("")
    lines.append("RANKING")
    for position, (name, amount) in enumerate(ranking, start=1):
        lines.append(f"{position}. {name} - {amount}")

    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")


def read_report(path):
    if not os.path.exists(path):
        print("Ainda não existe relatório salvo. Use a opção de salvar primeiro.")
        return
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    print("\n--- Conteúdo do relatório ---")
    print(content)


# ---------- OPÇÕES DO MENU ----------

def set_confidence(results, folder_photos, current):
    print("\n--- Configurar confiança mínima ---")
    print(f"Nível de confiança atual: {current}")

    while True:
        text = input("Digite o novo valor a ser atribuído à confiança: ")
        text = text.strip().replace(",", ".")
        try:
            value = float(text)
        except ValueError:
            print("Você digitou um valor errado. Por favor, digite um valor válido (entre 0 e 1).")
            continue

        if 0 <= value <= 1:
            print("Valor aceito!")
            break
        print("Valor inválido, escolha um valor no intervalo de 0 a 1.")

    print(f"Novo nível de confiança: {value}")
    show_summary(results, folder_photos, value)
    return value


def analyze_photo(results, conf):
    print("\n--- Analisar uma foto ---")
    photo = ask_photo()
    kept = filter_detections(results[photo], conf)

    print(f"\nFoto: {photo}")
    print(f"Objetos detectados (confiança >= {conf}): {len(kept)}")

    if kept:
        main_name, main_conf = kept[0]
        for name, c in kept:
            if c > main_conf:
                main_name, main_conf = name, c
        print(f"Objeto principal: {main_name}")
        print(f"Maior confiança: {main_conf * 100:.0f}%")
    else:
        print("Nenhum objeto com essa confiança mínima.")
    print()


def count_class_in_photo(conf):
    print("\n--- Contar uma classe na foto ---")
    photo = ask_photo()
    name = ask_class_name()
    print(f"Classe escolhida: [{name}]")
    amount = count_class(photo, name, conf)
    print(f"Objetos da classe '{name}' (confiança >= {conf}): {amount}")


def folder_report(conf):
    print("\n--- Relatório da pasta ---")
    folder = ask_folder()
    total = total_photos(folder)

    objects = 0
    empty = 0
    for n in range(1, total + 1):
        photo = photo_name(folder, n)
        amount = count_objects(photo, conf)
        print(f"Foto {n} | {photo} | {amount} objeto(s)")
        objects += amount
        if amount == 0:
            empty += 1

    print("\nTotal geral de objetos:", objects)
    print(f"Média de objetos por foto: {objects / total:.2f}")
    print("Fotos sem nenhum objeto:", empty)


def fullest_and_emptiest(conf):
    print("\n--- Foto mais cheia e Foto mais vazia ---")
    folder = ask_folder()
    total = total_photos(folder)

    first = photo_name(folder, 1)
    first_amount = count_objects(first, conf)
    fullest, fullest_amount = first, first_amount
    emptiest, emptiest_amount = first, first_amount

    for n in range(2, total + 1):
        photo = photo_name(folder, n)
        amount = count_objects(photo, conf)
        if amount > fullest_amount:
            fullest, fullest_amount = photo, amount
        if amount < emptiest_amount:
            emptiest, emptiest_amount = photo, amount

    print(f"\nFoto mais cheia: {fullest} ({fullest_amount} objetos)")
    print(f"Foto mais vazia: {emptiest} ({emptiest_amount} objetos)")


def search_class_in_folder(conf):
    print("\n--- Procurar uma classe na pasta ---")
    folder = ask_folder()
    total = total_photos(folder)
    name = ask_class_name()

    photos_hit = 0
    found = 0
    for n in range(1, total + 1):
        amount = count_class(photo_name(folder, n), name, conf)
        if amount > 0:
            photos_hit += 1
            found += amount

    print(f"\nClasse: '{name}' | pasta: '{folder}' | confiança >= {conf}")
    print(f"Aparece em {photos_hit} de {total} fotos.")
    print(f"Quantidade total encontrada: {found}")
    print(f"Porcentagem de fotos com a classe: {photos_hit / total * 100:.1f}%")

    if found == 0:
        print("Nenhum encontrado. Confira se a classe está na lista acima.")


def text_bar_chart(results, conf):
    print("\n--- Gráfico de barras em texto ---")
    folder = ask_folder()
    total = total_photos(folder)

    print(f"\nGráfico de objetos por foto na pasta '{folder}' (confiança >= {conf}):\n")

    for n in range(1, total + 1):
        photo = photo_name(folder, n)
        amount = len(filter_detections(results[photo], conf))
        print(f"{folder}_{n:02d} | {'#' * amount} ({amount})")


def show_ranking(results, conf):
    print("\n--- Ranking Top N ---")
    _, ranking = build_ranking(results, conf)

    if not ranking:
        print("Nenhum objeto com essa confiança mínima.")
        return

    n = ask_int_in_range(f"Quantas classes mostrar (1 a {len(ranking)}): ", 1, len(ranking))
    for position in range(n):
        name, amount = ranking[position]
        print(f"{position + 1}. {name} - {amount}")


def reverse_search(results, conf):
    print("\n--- Busca reversa ---")
    name = ask_class_name()
    index = build_reverse_index(results, conf)

    if name not in index:
        print(f"A classe '{name}' não foi encontrada com confiança >= {conf}.")
        return

    print(f"Fotos com '{name}' (confiança >= {conf}):")
    for photo in index[name]:
        amount = count_class_in(filter_detections(results[photo], conf), name)
        print(f"  {photo}: {amount}")
    print(f"Total de fotos: {len(index[name])}")


def compare_folders(results, folder_photos, conf):
    print("\n--- Comparar duas pastas ---")
    print("Primeira pasta:")
    folder_a = ask_folder()
    print("Segunda pasta:")
    folder_b = ask_folder()

    set_a = classes_of_folder(results, folder_photos, folder_a, conf)
    set_b = classes_of_folder(results, folder_photos, folder_b, conf)

    print(f"\nComparando '{folder_a}' e '{folder_b}' (confiança >= {conf}):\n")
    show_set("Em comum", set_a.intersection(set_b))
    show_set(f"Só em {folder_a}", set_a.difference(set_b))
    show_set(f"Só em {folder_b}", set_b.difference(set_a))
    show_set("União", set_a.union(set_b))


def show_matrix(results, folder_photos, conf):
    print("\n--- Matriz pasta x classe ---")
    _, ranking = build_ranking(results, conf)

    if not ranking:
        print("Nenhum objeto com essa confiança mínima.")
        return

    classes = [name for name, _ in ranking]
    folders = list(folder_photos)
    matrix = build_matrix(results, folder_photos, conf, classes)
    row_totals, column_totals = matrix_totals(matrix)

    print_matrix(folders, classes, matrix, row_totals, column_totals)

    value, folder, class_name = find_largest(matrix, folders, classes)
    print(f"\nMaior valor: {value} (pasta: {folder}, classe: {class_name})")


def show_histogram(results, conf):
    print("\n--- Histograma do inventário ---")
    _, ranking = build_ranking(results, conf)

    if not ranking:
        print("Nenhum objeto com essa confiança mínima.")
        return

    print(f"\nObjetos por classe (confiança >= {conf}), da mais para a menos frequente:\n")
    print_histogram(ranking)


def export_report(results, conf, path):
    print("\n--- Salvar relatório ---")
    inventory, ranking = build_ranking(results, conf)
    save_report(inventory, ranking, conf, path)
    print(f"Relatório salvo em: {path}")


def read_saved_report(path):
    print("\n--- Ler relatório salvo ---")
    read_report(path)


def inventory_option(results, folder_photos, conf):
    show_folders()
    prompt = "Digite o nome da pasta (ou Enter para o acervo inteiro): "
    folder = input(prompt).strip()
    while folder and folder not in folder_photos:
        print("Pasta inválida. Tente novamente.")
        folder = input(prompt).strip()

    if folder:
        photos = folder_photos[folder]
        title = f"pasta '{folder}' (confiança >= {conf})"
    else:
        photos = list(results)
        title = f"acervo inteiro (confiança >= {conf})"

    show_inventory(build_inventory(results, photos, conf), title)


# ---------- MENU E PRINCIPAL ----------

MENU_TEXT = [
    "Configurar confiança mínima",
    "Analisar uma foto",
    "Contar uma classe na foto",
    "Relatório da pasta",
    "Foto mais cheia e mais vazia",
    "Procurar uma classe na pasta",
    "Gráfico de barras em texto",
    "Ranking Top N",
    "Busca reversa",
    "Comparar duas pastas",
    "Matriz pasta x classe",
    "Histograma do inventário",
    "Salvar relatório (report.txt)",
    "Ler relatório salvo",
    "Inventário (acervo ou pasta)",
]


def show_menu():
    print("        Menu do PhotoCensus\n")
    for number, text in enumerate(MENU_TEXT, start=1):
        print(f"        {number} --> {text}")
    print("        0 --> Sair")


def main():
    print("PhotoCensus - Group 07")

    exception = True
    conf = 0.5
    results, folder_photos = load_collection()
    show_summary(results, folder_photos, conf)


    while exception:
        show_menu()
        choice = input("Escolha uma opção: ").strip()

        if choice == "0":
            exception=False
        elif choice == "1":
            conf = set_confidence(results, folder_photos, conf)
        elif choice == "2":
            analyze_photo(results, conf)
        elif choice == "3":
            count_class_in_photo(conf)
        elif choice == "4":
            folder_report(conf)
        elif choice == "5":
            fullest_and_emptiest(conf)
        elif choice == "6":
            search_class_in_folder(conf)
        elif choice == "7":
            text_bar_chart(results, conf)
        elif choice == "8":
            show_ranking(results, conf)
        elif choice == "9":
            reverse_search(results, conf)
        elif choice == "10":
            compare_folders(results, folder_photos, conf)
        elif choice == "11":
            show_matrix(results, folder_photos, conf)
        elif choice == "12":
            show_histogram(results, conf)
        elif choice == "13":
            export_report(results, conf, REPORT_PATH)
        elif choice == "14":
            read_saved_report(REPORT_PATH)
        elif choice == "15":
            inventory_option(results, folder_photos, conf)
        else:
            print("Escolha incorreta. Escolha uma opção válida\n")




if __name__ == "__main__":

    main()

