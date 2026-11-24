"""
PhotoCensus - Grupo 06
Módulo 2: sistema completo em UM arquivo

Organização deste arquivo (de cima para baixo):
  1. ENTRADAS        = perguntas ao usuário, com validação
  2. ACERVO          = carga, filtro, inventário, ranking e busca reversa (requisitos 1 a 5)
  3. ANÁLISES        = comparação, matriz, histograma e relatório (requisitos 6 a 9)
  4. MÓDULO 1        = funcionalidades do Módulo 1 com as novas estruturas
  5. MENU E main()   = o main() só organiza o menu; o trabalho está nas funções (requisito 10)

Formato dos dados usados pelas funções:
  resultados     = {foto: [(classe, confianca), ...]}   dicionário de resultados
  filtrados      = o mesmo formato, já filtrado pela confiança mínima
  inventario      = {classe: quantidade}                 dicionário de contagem
  indice_reverso = {classe: [fotos onde aparece]}       índice reverso
  ranking       = [(classe, quantidade), ...]          lista de tuplas, do maior para o menor
"""
import os
import sys

# ---------------------------------------------------------------
# O black_box.py (as funções prontas do professor) fica na pasta "kit".
# os.path.join(... )= junta pedaços de caminho (usa '/'ou '\'conforme o sistema; Linux ou Windows)
# '..'= 'subir uma pasta'
# sys.path.append(... )= acrescenta essa pasta na lista onde o Python procura arquivos
# from black_box import * = traz todas as funções do black_box.py (folder_exists, count_objects...)
# ---------------------------------------------------------------

GROUP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(GROUP_DIR, "..", "..", "kit"))
from black_box import *


# Guarda a lista de fotos de cada pasta, para não chamar list_photos toda hora.
# Formato: {pasta: [fotos]}. É preenchido sozinho, na primeira vez que a pasta é usada.
fotos_por_pasta = {}


# ===============================================================
# 1. ENTRADAS: perguntas ao usuário (todas usam uma "bandeira" valido que vira True
# quando o valor é aceito; o try/except evita que o programa feche com erro)
# ===============================================================


def ask_folder(folders, mensagem="Nome da pasta: "):
    # Pergunta até o usuário digitar uma pasta que existe na lista "folders".
    print("Pastas disponíveis: ")
    for folder in folders:
        print(folder)
    print()

    folder = input(mensagem).strip().lower()
    while folder not in folders:                # "not in" também funciona com lista
        print("Pasta não encontrada! Tente de novo.")
        folder = input(mensagem).strip().lower()
    return folder


def ask_folder_all(folders):
    # Igual ao ask_folder, mas deixar vazio significa "acervo inteiro" (devolve "").
    print("Pastas disponíveis: ")
    for folder in folders:
        print(folder, end=" ")
    print()

    folder = input("Digite a pasta (ou deixe vazio para o acervo inteiro): ").strip().lower()
    while folder != "" and folder not in folders:
        print("Pasta não encontrada! Tente de novo.")
        folder = input("Digite a pasta (ou deixe vazio para o acervo inteiro): ").strip().lower()
    return folder


def ask_photo(photos):
    # Mostra quantas fotos a pasta tem e devolve o CAMINHO da foto escolhida.
    # IMPORTANTE: só chame esta função com a lista NÃO vazia (veja choose_photo).
    total = len(photos)
    print(f"Total de fotos: {total}")

    valido = False
    while not valido:
        try:
            # int() gera ValueError se o texto não for um número inteiro (ex.: "abc", "2.5", vazio)
            numero = int(input(f"Número da foto (1 a {total}): "))
            if numero >= 1 and numero <= total:
                valido = True
            else:
                print("Número inválido! Tente de novo.")
        except ValueError:
            print("Número inválido! Tente de novo.")

    return photos[numero - 1]                   # a lista começa em 0, por isso numero - 1


def choose_photo(resultados, folder):
    # Pergunta a foto da pasta. Se a pasta não tem fotos, avisa e devolve None
    # (assim o ask_photo nunca fica preso num laço sem saída).
    photos = photos_of_folder(resultados, folder)
    if len(photos) == 0:
        print(f"A pasta {folder} não tem fotos.")
        return None
    return ask_photo(photos)


def ask_confidence():
    # Pergunta até o valor ser um número entre 0 e 1
    valido = False
    while not valido:
        try:
            # .replace(",", ".") aceita "0,8" e "0.8"; float() gera ValueError se não for número
            confianca = float(input("Confiança mínima (0 a 1): ").strip().replace(",", "."))
            if confianca >= 0 and confianca <= 1:
                valido = True
            else:
                print("Valor inválido! Digite um número entre 0 e 1.")
        except ValueError:
            print("Valor inválido! Digite um número entre 0 e 1.")
    return confianca


def ask_top_n(maximo):
    # Pergunta o N do ranking: um número inteiro de 1 até "maximo" (quantidade de classes)
    valido = False
    while not valido:
        try:
            n = int(input(f"Quantas classes mostrar (1 a {maximo})? "))
            if n >= 1 and n <= maximo:
                valido = True
            else:
                print("Número inválido! Tente de novo.")
        except ValueError:
            print("Número inválido! Tente de novo.")
    return n


def ask_class(filtrados):
    # Pergunta o nome de uma classe (as classes do kit estão em inglês: tv, person, car...)
    print("Classes disponíveis:", list_classes(filtrados))

    class_name = input("Digite a classe: ").strip().lower()
    while class_name == "":
        print("Digite alguma classe!")
        class_name = input("Digite a classe: ").strip().lower()
    return class_name


# ===============================================================
# 2. ACERVO: requisitos 1 a 5
# ===============================================================


# ---------------------------------------------------------------
# REQUISITO 1: carga do acervo (roda UMA vez, ao iniciar)
# ---------------------------------------------------------------

def load_collection(folders):
    # Monta o dicionário de resultados: {foto: [(classe, confianca), ...]}
    resultados = {}
    for folder in folders:                      # laço de fora: cada pasta
        for photo in list_photos(folder):       # 🔌 list_photos: lista com os caminhos das fotos da pasta
            resultados[photo] = detect(photo)      # 🔌 detect: lista de tuplas (classe, confianca), desde 0.25
    return resultados


def show_summary(folders, resultados):
    total_detections = 0
    for photo in resultados:
        total_detections += len(resultados[photo])

    print("\n--- Resumo do acervo ---")
    print(f"Pastas: {len(folders)}")
    print(f"Fotos: {len(resultados)}")
    print(f"Detecções: {total_detections}")


# ---------------------------------------------------------------
# REQUISITO 2: filtro de confiança
# ---------------------------------------------------------------

def filter_detections(detections, confianca_minima):
    # Recebe uma lista de detecções e devolve uma lista NOVA só com as que passam no filtro.
    filtrados = []
    for detection in detections:
        if detection[1] >= confianca_minima:      # [1] = confiança
            filtrados.append(detection)
    return filtrados


def filter_collection(resultados, confianca_minima):
    # Aplica o filtro em todas as fotos e devolve um dicionário novo (o original não muda).
    filtrados = {}
    for photo in resultados:
        filtrados[photo] = filter_detections(resultados[photo], confianca_minima)
    return filtrados


# ---------------------------------------------------------------
# REQUISITO 3: inventário (dicionário de contagem)
# ---------------------------------------------------------------

def build_inventory(resultados, folder=""):
    # {classe: quantidade}. Com folder="" conta o acervo inteiro; com uma pasta, só ela.
    inventario = {}
    for photo in resultados:
        if folder == "" or photo_in_folder(photo, folder):
            for detection in resultados[photo]:
                class_name = detection[0]
                if class_name in inventario:         # "in" em dicionário confere as chaves
                    inventario[class_name] += 1      # já existe: soma 1
                else:
                    inventario[class_name] = 1       # primeira vez: começa em 1
    return inventario


def show_inventory(inventario, folder=""):
    if folder == "":
        print("\n--- Inventário do acervo inteiro ---")
    else:
        print(f"\n--- Inventário da pasta {folder} ---")
    if len(inventario) == 0:
        print("Nenhum objeto encontrado.")
    for class_name in inventario:
        print(f"{class_name:<15}: {inventario[class_name]}")


# ---------------------------------------------------------------
# REQUISITO 4: ranking Top N (ordenação feita pelo grupo: bolha)
# ---------------------------------------------------------------

def inventory_to_list(inventario):
    # Converte {classe: quantidade} em lista de tuplas [(classe, quantidade), ...]
    ranking = []
    for class_name in inventario:
        ranking.append((class_name, inventario[class_name]))
    return ranking


def sort_ranking(ranking):
    # Ordenação por bolha (bubble sort), do MAIOR para o MENOR.
    # Compara vizinhos: se o da esquerda for MENOR que o da direita, troca de lugar.
    # A cada volta de fora, o menor valor "afunda" para o fim da parte ainda não ordenada.
    tamanho = len(ranking)
    for i in range(tamanho - 1):
        for j in range(tamanho - 1 - i):
            if ranking[j][1] < ranking[j + 1][1]:      # [1] = quantidade; troque < por > para ordem crescente
                auxiliar = ranking[j]                    # troca usando uma variável auxiliar
                ranking[j] = ranking[j + 1]
                ranking[j + 1] = auxiliar
    return ranking


def show_top_n(ranking, n):
    print(f"\n--- Top {n} classes mais frequentes ---")
    for posicao in range(n):
        item = ranking[posicao]
        print(f"{posicao + 1}. {item[0]} - {item[1]}")


def top_n_option(ranking):
    # Valida o N e mostra o ranking (se existir alguma classe)
    if len(ranking) > 0:
        n = ask_top_n(len(ranking))
        show_top_n(ranking, n)
    else:
      print("Nenhuma classe detectada com essa confiança minima")

# ---------------------------------------------------------------
# REQUISITO 5: índice reverso e busca reversa
# ---------------------------------------------------------------

def build_reverse_index(resultados):
    # {classe: [fotos onde ela aparece]}
    indice_reverso = {}
    for photo in resultados:
        for detection in resultados[photo]:
            class_name = detection[0]
            if class_name not in indice_reverso:
                indice_reverso[class_name] = []                  # primeira vez: cria a lista
            if photo not in indice_reverso[class_name]:          # não repete a mesma foto
                indice_reverso[class_name].append(photo)
    return indice_reverso


def search_class(indice_reverso, resultados, class_name):
    # Lista as fotos onde a classe aparece e quantos objetos dela há em cada foto.
    if class_name in indice_reverso:
        print(f"\n--- Fotos com '{class_name}' ---")
        for photo in indice_reverso[class_name]:
            quantidade = 0
            for detection in resultados[photo]:
                if detection[0] == class_name:
                    quantidade += 1
            print(f"{photo}: {quantidade}")
    else:
      print(f"Classe {class_name} não encontrada no acervo")

# ---------------------------------------------------------------
# Recalcula tudo quando a confiança muda
# ---------------------------------------------------------------

def rebuild(resultados, confianca_minima):
    # Devolve 4 coisas, todas respeitando a confiança mínima:
    # (resultados filtrados, inventário, índice reverso, ranking ordenado)
    filtrados = filter_collection(resultados, confianca_minima)
    inventario = build_inventory(filtrados)
    indice_reverso = build_reverse_index(filtrados)
    ranking = sort_ranking(inventory_to_list(inventario))
    return filtrados, inventario, indice_reverso, ranking


# ===============================================================
# 3. ANÁLISES: requisitos 6 a 9 e funções auxiliares
# ===============================================================


# ---------------------------------------------------------------
# FUNÇÕES AUXILIARES
# ---------------------------------------------------------------

def photo_in_folder(photo, folder):
    # Confere se a foto pertence à pasta, comparando com a lista de fotos da pasta.
    # A lista vem do kit (list_photos) só na PRIMEIRA vez; depois fica guardada em
    # fotos_por_pasta. Isso evita chamar o kit milhares de vezes dentro dos laços.
    if folder not in fotos_por_pasta:
        fotos_por_pasta[folder] = list_photos(folder)
    return photo in fotos_por_pasta[folder]


def photos_of_folder(resultados, folder):
    # Devolve a lista das fotos que pertencem à pasta (na ordem do dicionário)
    photos = []
    for photo in resultados:                       # for em dicionário percorre as CHAVES (as fotos)
        if photo_in_folder(photo, folder):
            photos.append(photo)
    return photos


def list_classes(resultados):
    # Devolve a lista de classes DIFERENTES, na ordem em que aparecem (sem repetir).
    # Usamos lista (e não set) para a ordem ser sempre a mesma em toda execução.
    classes = []
    for photo in resultados:
        for detection in resultados[photo]:        # detection é uma tupla (classe, confianca)
            class_name = detection[0]           # [0] = primeiro item da tupla
            if class_name not in classes:       # "not in" = ainda não está na lista
                classes.append(class_name)
    return classes


# ---------------------------------------------------------------
# REQUISITO 6: comparação de pastas com conjuntos (set)
# ---------------------------------------------------------------

def classes_of_folder(resultados, folder):
    # Devolve um CONJUNTO (set) com as classes que aparecem na pasta.
    # set() cria um conjunto vazio; .add() coloca um item; repetidos são ignorados sozinhos.
    classes = set()
    for photo in resultados:
        if photo_in_folder(photo, folder):
            for detection in resultados[photo]:
                classes.add(detection[0])
    return classes


def compare_folders(resultados, folder_a, folder_b):
    # Devolve 4 conjuntos: (em_comum, so_a, so_b, uniao)
    conjunto_a = classes_of_folder(resultados, folder_a)
    conjunto_b = classes_of_folder(resultados, folder_b)

    em_comum = conjunto_a & conjunto_b      # & = interseção: está nas DUAS pastas
    so_a = conjunto_a - conjunto_b      # -  = diferença: está só na pasta A
    so_b = conjunto_b - conjunto_a      # está só na pasta B
    uniao = conjunto_a | conjunto_b       # | = união: está em pelo menos uma das pastas
    return em_comum, so_a, so_b, uniao


def show_set(titulo, itens, classes_ordenadas):
    # Mostra os itens do conjunto sempre na mesma ordem (conjunto não tem ordem própria).
    print(f"{titulo}: ", end="")
    if len(itens) > 0:
        for class_name in classes_ordenadas:
            if class_name in itens:
                print(class_name, end="  ")
        print()
    else:
        print("(nenhuma)")

def show_comparison(resultados, folder_a, folder_b):
    em_comum, so_a, so_b, uniao = compare_folders(resultados, folder_a, folder_b)
    classes = list_classes(resultados)

    print(f"\n--- Comparação: {folder_a} x {folder_b} ---")
    show_set("Em comum", em_comum, classes)
    show_set(f"Só em {folder_a}", so_a, classes)
    show_set(f"Só em {folder_b}", so_b, classes)
    show_set("União", uniao, classes)


# ---------------------------------------------------------------
# REQUISITO 7: matriz pasta x classe
# ---------------------------------------------------------------

def build_matrix(resultados, folders, classes):
    # Matriz = lista de listas. matrix[i][j] = quantas vezes a classe j aparece na pasta i.
    #            car  person  tv
    #   street  [ 2,    2,     0 ]   <- matrix[0]
    #   office  [ 0,    1,     1 ]   <- matrix[1]
    matrix = []
    for folder in folders:                      # cada pasta vira uma LINHA
        linha = []
        for class_name in classes:              # cada classe vira uma COLUNA
            quantidade = 0
            for photo in resultados:
                if photo_in_folder(photo, folder):
                    for detection in resultados[photo]:
                        if detection[0] == class_name:
                            quantidade += 1
            linha.append(quantidade)
        matrix.append(linha)
    return matrix


def find_highest(matrix, folders, classes):
    # Procura a combinação (pasta, classe) com o maior valor (sem usar função pronta de máximo).
    # Usa o mesmo padrão do "campeão" do Módulo 1.
    if len(folders) == 0 or len(classes) == 0:
        return None

    best_folder = folders[0]
    best_class = classes[0]
    best_value = matrix[0][0]                   # começa supondo que o primeiro é o maior

    for i in range(len(folders)):
        for j in range(len(classes)):
            if matrix[i][j] > best_value:       # ">" (e não ">=") mantém o primeiro em caso de empate
                best_value = matrix[i][j]
                best_folder = folders[i]
                best_class = classes[j]

    return best_folder, best_class, best_value


def print_line(tamanho):
    for i in range(tamanho):
        print("-", end="")
    print()


def print_matrix(matrix, folders, classes):

    largura = 15 + 12 * (len(folders) + 1)

    print("\n--- Matriz pasta x classe ---")
    print(f"{'Pasta':<15}", end="")
    for folder in folders:
        print(f"{folder:>12}", end="")    # :>{coluna} = alinha à direita na largura da coluna
    print(f"{'Total':>12}")
    print_line(largura)

    folder_total = []                          # um total para cada linha, começando em 0
    for folder in folders:
        folder_total.append(0)

    total_geral = 0
    for j in range(len(classes)):
        print(f"{classes[j]:<15}", end="")      # :<15 = alinha à esquerda em 15 espaços
        class_total = 0
        for i in range(len(folders)):
            value = matrix[i][j]
            print(f"{value:>12}", end="")
            class_total += value                  # soma da linha
            folder_total[i] += value           # soma da coluna
        print(f"{class_total:>12}")
        total_geral += class_total

    print_line(largura)
    print(f"{'Total':<15}", end="")
    for total in folder_total:
        print(f"{total:>12}", end="")
    print(f"{total_geral:>12}")

    best = find_highest(matrix, folders, classes)
    if best is not None:
        print(f"\nMaior valor: classe '{best[1]}' na pasta '{best[0]}' ({best[2]})")


# ---------------------------------------------------------------
# REQUISITO 8: histograma em texto
# ---------------------------------------------------------------

def show_histogram(ranking):
    # Um # por unidade, na ordem do ranking (que já vem ordenado).
    print("\n--- Histograma (ordem do ranking) ---")
    if len(ranking) == 0:
        print("Nenhuma detecção para mostrar.")
    for item in ranking:
        class_name = item[0]                    # item = tupla (classe, quantidade)
        quantidade = item[1]
        print(f"{class_name:<15}|", end="")
        for i in range(quantidade):                 # laço de dentro: um # por objeto
            print("#", end="")
        print(f" ({quantidade})")


# ---------------------------------------------------------------
# REQUISITO 9: relatório em arquivo (report.txt)
# ---------------------------------------------------------------

def save_report(inventario, ranking, confianca_minima, nome_arquivo="report.txt"):
    # open(nome, "w") = abre para ESCREVER (cria o arquivo; se já existe, apaga e escreve de novo)
    # try/except = tenta executar; se der erro de arquivo, cai no except em vez de fechar o programa
    # O relatório também registra a confiança mínima usada, para saber de onde vieram os números.
    try:
        arquivo = open(nome_arquivo, "w", encoding="utf-8")

        arquivo.write("RELATÓRIO PHOTOCENSUS - GRUPO 06\n")      # \n = pular linha
        arquivo.write(f"Confiança mínima usada: {confianca_minima}\n\n")

        arquivo.write("INVENTÁRIO (classe: quantidade)\n")
        for class_name in inventario:
            arquivo.write(f"{class_name}: {inventario[class_name]}\n")

        arquivo.write("\nRANKING (posição. classe - quantidade)\n")
        posicao = 1
        for item in ranking:
            arquivo.write(f"{posicao}. {item[0]} - {item[1]}\n")
            posicao += 1

        arquivo.close()                            # fecha o arquivo (garante que tudo foi gravado)
        print(f"Relatório salvo em {nome_arquivo}")
        return True
    except OSError:
        print("Não foi possível salvar o relatório.")
        return False


def read_report(nome_arquivo="report.txt"):
    # open(nome, "r") = abre para LER. Se o arquivo não existe, dá FileNotFoundError.
    try:
        arquivo = open(nome_arquivo, "r", encoding="utf-8")
        conteudo = arquivo.read()                   # .read() = lê o arquivo inteiro como um texto
        arquivo.close()
        print(f"\n--- Conteúdo de {nome_arquivo} ---")
        print(conteudo)
        return True
    except FileNotFoundError:
        print("Ainda não existe relatório salvo. Salve um primeiro.")
        return False


# ===============================================================
# 4. MÓDULO 1: funcionalidades reescritas com as novas estruturas
# ===============================================================


def analyze_photo(resultados, photo):
    # Analisar uma foto: total de objetos, objeto principal e maior confiança
    detections = resultados[photo]
    total = len(detections)

    print(f"\nFoto: {photo}")
    print(f"Total de objetos: {total}")
    if total > 0:
        main_class = detections[0][0]           # começa supondo que o primeiro é o principal
        maior_confianca = detections[0][1]
        for detection in detections:
            if detection[1] > maior_confianca:
                maior_confianca = detection[1]
                main_class = detection[0]
        print(f"Objeto principal: {main_class}")
        print(f"Maior confiança: {maior_confianca * 100:.0f}%")
    else:
      print("Nenhum objeto acima da confiança mínima")

def count_class_in_photo(resultados, photo, class_name):
    quantidade = 0
    for detection in resultados[photo]:
        if detection[0] == class_name:
            quantidade += 1

    print(f"\nFoto: {photo}")
    if quantidade > 0:
        print(f"Classe {class_name} encontrada! Quantidade: {quantidade}")
    else:
        print(f"Classe {class_name} não encontrada nesta foto.")


def folder_report(resultados, folder):
    photos = photos_of_folder(resultados, folder)

    total_objects = 0       # acumulador: soma os objetos de todas as fotos
    empty_photos = 0        # contador: quantas fotos ficaram com 0 objetos

    print(f"\n--- Relatório da pasta {folder} ---")
    for numero in range(1, len(photos) + 1):
        objects = len(resultados[photos[numero - 1]])
        print(f"Foto {numero}: {objects} objeto(s)")
        total_objects += objects
        if objects == 0:
            empty_photos += 1

    if len(photos) > 0:                         # só divide se a pasta tiver fotos
        media = total_objects / len(photos)
    else:
        media = 0
    print(f"Total de objetos: {total_objects}")
    print(f"Média por foto: {media:.2f}")
    print(f"Fotos sem objetos: {empty_photos}")


def fullest_and_emptiest(resultados, folder):
    photos = photos_of_folder(resultados, folder)
    if len(photos) > 0:
        # começamos supondo que a foto 1 é a mais cheia e a mais vazia
        primeira_contagem = len(resultados[photos[0]])
        numero_mais_cheia = 1
        contagem_mais_cheia = primeira_contagem
        numero_mais_vazia = 1
        contagem_mais_vazia = primeira_contagem

        for numero in range(2, len(photos) + 1):
            objects = len(resultados[photos[numero - 1]])
            if objects > contagem_mais_cheia:
                contagem_mais_cheia = objects
                numero_mais_cheia = numero
            if objects < contagem_mais_vazia:
                contagem_mais_vazia = objects
                numero_mais_vazia = numero

        print(f"\n--- Pasta {folder} ---")
        print(f"Foto mais cheia: {numero_mais_cheia} com {contagem_mais_cheia} objeto(s)")
        print(f"Foto mais vazia: {numero_mais_vazia} com {contagem_mais_vazia} objeto(s)")
    else:
      print("Nenhuma foto encontrada na pasta.")

def search_class_in_folder(resultados, folder, class_name):
    photos = photos_of_folder(resultados, folder)

    photos_with_class = 0       # contador: em quantas fotos a classe aparece
    total_encontrados = 0             # acumulador: total de objetos dessa classe

    for photo in photos:
        encontrados = 0
        for detection in resultados[photo]:
            if detection[0] == class_name:
                encontrados += 1
        total_encontrados += encontrados
        if encontrados > 0:
            photos_with_class += 1

    porcentagem = 0
    if len(photos) > 0:
        porcentagem = photos_with_class / len(photos) * 100

    print(f"\nClasse {class_name} na pasta {folder}:")
    print(f"Aparece em {photos_with_class} de {len(photos)} fotos")
    print(f"Total encontrado: {total_encontrados}")
    print(f"Fotos com a classe: {porcentagem:.1f}%")


def bar_chart(resultados, folder):
    photos = photos_of_folder(resultados, folder)

    print(f"\n--- Gráfico de barras da pasta {folder} ---")
    for numero in range(1, len(photos) + 1):         # laço de fora: cada foto
        objects = len(resultados[photos[numero - 1]])
        nome_arquivo = f"{folder}_{numero:02d}"
        print(f"{nome_arquivo:<15}|", end="")
        for i in range(objects):                     # laço de dentro: um # por objeto
            print("#", end="")
        print(f"({objects})")


# ===============================================================
# 5. MENU E main()
# ===============================================================


def show_menu(confianca_minima, current_folder):
    print("\n===== PHOTOCENSUS - GRUPO 06 =====")
    print(f"Confiança mínima: {confianca_minima} | Pasta atual: {current_folder}")
    print("--- Configurações ---")
    print(" 1 - Definir confiança mínima")
    print(" 2 - Trocar de pasta")
    print("--- Módulo 1 (pasta atual) ---")
    print(" 3 - Analisar uma foto")
    print(" 4 - Contar uma classe em uma foto")
    print(" 5 - Relatório da pasta")
    print(" 6 - Foto mais cheia e mais vazia")
    print(" 7 - Buscar uma classe na pasta")
    print(" 8 - Gráfico de barras da pasta")
    print("--- Módulo 2 (acervo) ---")
    print(" 9 - Inventário")
    print("10 - Ranking Top N")
    print("11 - Busca reversa de uma classe")
    print("12 - Comparar duas pastas")
    print("13 - Matriz pasta x classe")
    print("14 - Histograma")
    print("15 - Salvar relatório")
    print("16 - Ler relatório")
    print(" 0 - Sair")
    print("====================================")


def main():
    print("PhotoCensus - Grupo 06")

    # Requisito 1: carga do acervo (uma única vez)
    folders = list_folders()                    # 🔌 do kit
    resultados = load_collection(folders)
    show_summary(folders, resultados)

    confianca_minima = 0.5
    # Tudo abaixo respeita a confiança mínima (requisito 2)
    filtrados, inventario, indice_reverso, ranking = rebuild(resultados, confianca_minima)

    current_folder = ask_folder(folders, "Escolha a pasta de trabalho: ")
    opcao = ""

    while opcao != "0":
        show_menu(confianca_minima, current_folder)
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print("Até logo!")
        elif opcao == "1":
            confianca_minima = ask_confidence()
            filtrados, inventario, indice_reverso, ranking = rebuild(resultados, confianca_minima)
            print(f"Confiança mínima definida: {confianca_minima}")
        elif opcao == "2":
            current_folder = ask_folder(folders, "Escolha a pasta de trabalho: ")
        elif opcao == "3":
            photo = choose_photo(filtrados, current_folder)
            if photo is not None:                # None = pasta sem fotos (já avisou o usuário)
                analyze_photo(filtrados, photo)
        elif opcao == "4":
            photo = choose_photo(filtrados, current_folder)
            if photo is not None:
                count_class_in_photo(filtrados, photo, ask_class(filtrados))
        elif opcao == "5":
            folder_report(filtrados, current_folder)
        elif opcao == "6":
            fullest_and_emptiest(filtrados, current_folder)
        elif opcao == "7":
            search_class_in_folder(filtrados, current_folder, ask_class(filtrados))
        elif opcao == "8":
            bar_chart(filtrados, current_folder)
        elif opcao == "9":
            folder = ask_folder_all(folders)
            show_inventory(build_inventory(filtrados, folder), folder)
        elif opcao == "10":
            top_n_option(ranking)
        elif opcao == "11":
            search_class(indice_reverso, filtrados, ask_class(filtrados))
        elif opcao == "12":
            folder_a = ask_folder(folders, "Primeira pasta: ")
            folder_b = ask_folder(folders, "Segunda pasta: ")
            show_comparison(filtrados, folder_a, folder_b)
        elif opcao == "13":
            classes = list_classes(filtrados)
            print_matrix(build_matrix(filtrados, folders, classes), folders, classes)
        elif opcao == "14":
            show_histogram(ranking)
        elif opcao == "15":
            save_report(inventario, ranking, confianca_minima)
        elif opcao == "16":
            read_report()
        else:
            print("Opção inválida! Tente de novo.")


# Só executa main() quando o arquivo é rodado diretamente (não quando é importado)
if __name__ == "__main__":
    main()
