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







# ==================== ENTRADAS ====================

def ask_folder():
    show_folders()
    pasta_valida = False
    nome_pasta = ""

    while not pasta_valida:
        nome_pasta = input("Informe a pasta desejada (ex: animals, sports, street): ").strip()

        if nome_pasta == "":
            print("Erro: o nome da pasta não pode ficar em branco.")
        elif not folder_exists(nome_pasta):
            print("Erro: essa pasta não foi encontrada.")
        elif total_photos(nome_pasta) == 0:
            print("Erro: a pasta escolhida não possui fotos válidas.")
        else:
            pasta_valida = True

    return nome_pasta


def ask_photo():
    diretorio = ask_folder()
    qtd_imagens = total_photos(diretorio)
    print(f"Total de imagens disponíveis em '{diretorio}': {qtd_imagens}")

    indice_valido = False
    indice_escolhido = 0

    while not indice_valido:
        entrada = input(f"Digite o número da imagem (de 1 até {qtd_imagens}): ").strip()

        try:
            indice_escolhido = int(entrada)
            if 1 <= indice_escolhido <= qtd_imagens:
                indice_valido = True
            else:
                print(f"Fora do intervalo! Escolha um valor entre 1 e {qtd_imagens}.")
        except ValueError:
            print("Entrada inválida! Digite apenas números inteiros.")

    return photo_name(diretorio, indice_escolhido)


def pedir_classe(mensagem):
    show_classes()
    nome_classe = ""

    while nome_classe == "":
        nome_classe = input(mensagem).strip().lower()
        if nome_classe == "":
            print("O nome da classe não pode ser vazio.")

    return nome_classe


def pedir_inteiro(mensagem, minimo, maximo):
    valor_valido = False
    numero = 0

    while not valor_valido:
        entrada = input(mensagem).strip()

        try:
            numero = int(entrada)
            if minimo <= numero <= maximo:
                valor_valido = True
            else:
                print(f"Fora do intervalo! Escolha um valor entre {minimo} e {maximo}.")
        except ValueError:
            print("Entrada inválida! Digite apenas números inteiros.")

    return numero


# ==================== CARGA, FILTRO E INVENTÁRIO ====================

def carregar_acervo():
    resultados = {}
    fotos_por_pasta = {}

    for pasta in list_folders():
        fotos_por_pasta[pasta] = list_photos(pasta)

        for foto in fotos_por_pasta[pasta]:
            resultados[foto] = detect(foto)

    return resultados, fotos_por_pasta


def filtrar_deteccoes(deteccoes, limiar):
    aprovadas = []

    for nome_classe, confianca in deteccoes:
        if confianca >= limiar:
            aprovadas.append((nome_classe, confianca))

    return aprovadas


def exibir_resumo(resultados, fotos_por_pasta, limiar):
    total_bruto = 0
    total_filtrado = 0

    for foto in resultados:
        total_bruto += len(resultados[foto])
        total_filtrado += len(filtrar_deteccoes(resultados[foto], limiar))

    print("\n--- Resumo do acervo ---")
    print(f"Pastas: {len(fotos_por_pasta)}")
    print(f"Fotos: {len(resultados)}")
    print(f"Detecções (a partir de 0.25): {total_bruto}")
    print(f"Detecções com confiança >= {limiar}: {total_filtrado}")


def montar_inventario(resultados, lista_fotos, limiar):
    inventario = {}

    for foto in lista_fotos:
        for nome_classe, confianca in filtrar_deteccoes(resultados[foto], limiar):
            if nome_classe in inventario:
                inventario[nome_classe] += 1
            else:
                inventario[nome_classe] = 1

    return inventario


def exibir_inventario(inventario, titulo):
    print(f"\n--- Inventário: {titulo} ---")

    if len(inventario) == 0:
        print("Nenhum objeto com essa confiança mínima.")
        return

    total = 0
    for nome_classe in inventario:
        print(f"{nome_classe}: {inventario[nome_classe]}")
        total += inventario[nome_classe]

    print(f"\nClasses distintas: {len(inventario)}")
    print(f"Total de objetos: {total}")


# ==================== ORDENAÇÃO  ====================

def inventario_para_lista(inventario):
    itens = []

    for nome_classe in inventario:
        itens.append((nome_classe, inventario[nome_classe]))

    return itens


def ordenar_decrescente(itens):
    # Bubble sort em uma cópia, do maior para o menor.
    ranking = itens[:]
    n = len(ranking)

    for i in range(n - 1):
        for j in range(n - 1 - i):
            if ranking[j][1] < ranking[j + 1][1]:
                ranking[j], ranking[j + 1] = ranking[j + 1], ranking[j]

    return ranking


def ordenar_nomes(nomes):
    # Insertion sort alfabético.
    lista = list(nomes)

    for i in range(1, len(lista)):
        atual = lista[i]
        j = i - 1

        while j >= 0 and lista[j] > atual:
            lista[j + 1] = lista[j]
            j -= 1

        lista[j + 1] = atual

    return lista


def montar_ranking(resultados, limiar):
    inventario = montar_inventario(resultados, list(resultados), limiar)
    ranking = ordenar_decrescente(inventario_para_lista(inventario))
    return inventario, ranking


# ==================== BUSCA REVERSA E CONJUNTOS ====================

def montar_indice_reverso(resultados, limiar):
    indice = {}

    for foto in resultados:
        for nome_classe, confianca in filtrar_deteccoes(resultados[foto], limiar):
            if nome_classe not in indice:
                indice[nome_classe] = []

            if foto not in indice[nome_classe]:
                indice[nome_classe].append(foto)

    return indice


def contar_classe_em(deteccoes, alvo):
    quantidade = 0

    for nome_classe, confianca in deteccoes:
        if nome_classe == alvo:
            quantidade += 1

    return quantidade


def classes_da_pasta(resultados, fotos_por_pasta, pasta, limiar):
    conjunto = set()

    for foto in fotos_por_pasta[pasta]:
        for nome_classe, confianca in filtrar_deteccoes(resultados[foto], limiar):
            conjunto.add(nome_classe)

    return conjunto


def exibir_conjunto(titulo, nomes):
    ordenados = ordenar_nomes(nomes)

    if len(ordenados) == 0:
        print(f"{titulo} (0): nenhuma")
    else:
        print(f"{titulo} ({len(ordenados)}): " + ", ".join(ordenados))


# ==================== MATRIZ PASTA x CLASSE ====================

def montar_matriz(resultados, fotos_por_pasta, limiar, classes):
    matriz = []

    for pasta in fotos_por_pasta:
        inventario = montar_inventario(resultados, fotos_por_pasta[pasta], limiar)
        linha = []

        for nome_classe in classes:
            if nome_classe in inventario:
                linha.append(inventario[nome_classe])
            else:
                linha.append(0)

        matriz.append(linha)

    return matriz


def totais_da_matriz(matriz):
    totais_linhas = []
    for linha in matriz:
        soma = 0
        for valor in linha:
            soma += valor
        totais_linhas.append(soma)

    totais_colunas = []
    for j in range(len(matriz[0])):
        soma = 0
        for i in range(len(matriz)):
            soma += matriz[i][j]
        totais_colunas.append(soma)

    return totais_linhas, totais_colunas


def maior_da_matriz(matriz, pastas, classes):
    melhor_valor = -1
    melhor_pasta = ""
    melhor_classe = ""

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] > melhor_valor:
                melhor_valor = matriz[i][j]
                melhor_pasta = pastas[i]
                melhor_classe = classes[j]

    return melhor_valor, melhor_pasta, melhor_classe


def imprimir_matriz(pastas, classes, matriz, totais_linhas, totais_colunas):
    total_geral = 0
    for t in totais_linhas:
        total_geral += t

    colunas_por_bloco = 6

    for inicio in range(0, len(classes), colunas_por_bloco):
        fim = inicio + colunas_por_bloco
        if fim > len(classes):
            fim = len(classes)

        ultimo_bloco = (fim == len(classes))

        cabecalho = f"{'Pasta':<14}"
        for j in range(inicio, fim):
            cabecalho += f"{classes[j][:12]:>13}"
        if ultimo_bloco:
            cabecalho += f"{'Total':>8}"

        print("\n" + cabecalho)
        print("-" * len(cabecalho))

        for i in range(len(pastas)):
            linha = f"{pastas[i]:<14}"
            for j in range(inicio, fim):
                linha += f"{matriz[i][j]:>13}"
            if ultimo_bloco:
                linha += f"{totais_linhas[i]:>8}"
            print(linha)

        rodape = f"{'TOTAL':<14}"
        for j in range(inicio, fim):
            rodape += f"{totais_colunas[j]:>13}"
        if ultimo_bloco:
            rodape += f"{total_geral:>8}"
        print(rodape)


# ==================== HISTOGRAMA E RELATÓRIO ====================

def imprimir_histograma(ranking):
    maior_barra = ranking[0][1]
    valor_do_simbolo = 1

    if maior_barra > 50:
        valor_do_simbolo = (maior_barra + 49) // 50
        print(f"(cada # = {valor_do_simbolo} objetos)")

    for nome_classe, quantidade in ranking:
        tamanho = quantidade // valor_do_simbolo
        if tamanho == 0:
            tamanho = 1

        print(f"{nome_classe:<15}| {'#' * tamanho} ({quantidade})")


def salvar_relatorio(inventario, ranking, limiar, caminho):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write("PhotoCensus - Relatório do acervo\n")
        arquivo.write(f"Confiança mínima: {limiar}\n\n")

        arquivo.write("INVENTÁRIO\n")
        for nome_classe in inventario:
            arquivo.write(f"{nome_classe}: {inventario[nome_classe]}\n")

        arquivo.write("\nRANKING\n")
        posicao = 1
        for nome_classe, quantidade in ranking:
            arquivo.write(f"{posicao}. {nome_classe} - {quantidade}\n")
            posicao += 1


def ler_relatorio(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
    except FileNotFoundError:
        print("Ainda não existe relatório salvo. Use a opção de salvar primeiro.")
        return

    print("\n--- Conteúdo do relatório ---")
    print(conteudo)


# ==================== MENU E PRINCIPAL ====================

def exibir_menu():
    print("\n========================================")
    print("         PHOTOCENSUS - SISTEMA          ")
    print("========================================")
    print("[1]  Ajustar confiança mínima")
    print("[2]  Inspecionar uma única foto")
    print("[3]  Contar classe específica em uma foto")
    print("[4]  Gerar relatório completo da pasta")
    print("[5]  Buscar foto mais cheia e mais vazia")
    print("[6]  Buscar classe específica na pasta")
    print("[7]  Exibir gráfico de barras em texto")
    print("[8]  Ranking Top N")
    print("[9]  Busca reversa (classe -> fotos)")
    print("[10] Comparar duas pastas")
    print("[11] Matriz pasta x classe")
    print("[12] Histograma do inventário")
    print("[13] Salvar relatório (report.txt)")
    print("[14] Ler relatório salvo")
    print("[15] Inventário (acervo ou pasta)")
    print("[0]  Encerrar programa")
    print("========================================")


# ==================== OPÇÕES DO MENU ====================

# Opção 1: devolve o novo valor da confiança mínima
def ajustar_confianca(resultados, fotos_por_pasta, limiar_confianca):
    print("\n=== Ajuste de Confiança Mínima ===")
    print(f"Confiança configurada atualmente: {limiar_confianca}")

    novo_limiar_ok = False
    while not novo_limiar_ok:
        texto_digitado = input("Novo valor de confiança (0.0 a 1.0): ").strip().replace(",", ".")

        try:
            valor_convertido = float(texto_digitado)
            if 0.0 <= valor_convertido <= 1.0:
                limiar_confianca = valor_convertido
                novo_limiar_ok = True
                print(f"Sucesso! Confiança atualizada para {limiar_confianca}")
            else:
                print("O valor precisa estar entre 0 e 1.")
        except ValueError:
            print("Formato inválido. Digite um número decimal (ex: 0.65).")

    exibir_resumo(resultados, fotos_por_pasta, limiar_confianca)
    return limiar_confianca


# Opção 2
def inspecionar_foto(limiar_confianca):
    print("\n=== Inspeção de Foto ===")
    caminho_img = ask_photo()
    detectados = count_objects(caminho_img, limiar_confianca)

    print(f"\nArquivo analisado: {caminho_img}")
    print(f"Quantidade de objetos (confiança mínima de {limiar_confianca}): {detectados}")

    if detectados > 0:
        obj_destaque = main_object(caminho_img)
        maior_taxa = max_confidence(caminho_img) * 100
        print(f"Objeto em destaque: {obj_destaque}")
        print(f"Pico de confiança atingido: {maior_taxa:.0f}%")
    else:
        print("Nenhum objeto atingiu o nível de confiança exigido.")


# Opção 3
def contar_classe_na_foto(limiar_confianca):
    print("\n=== Contagem de Classe na Foto ===")
    caminho_img = ask_photo()
    nome_classe = pedir_classe("Qual classe deseja contar? ")

    ocorrencias = count_class(caminho_img, nome_classe, limiar_confianca)
    print(f"Classe pesquisada: [{nome_classe}]")
    print(f"Total encontrado na imagem (confiança >= {limiar_confianca}): {ocorrencias}")


# Opção 4
def relatorio_da_pasta(limiar_confianca):
    print("\n=== Relatório Completo da Pasta ===")
    diretorio = ask_folder()
    qtd_imagens = total_photos(diretorio)

    soma_objetos = 0
    imagens_sem_nada = 0
    indice = 1

    while indice <= qtd_imagens:
        arquivo_atual = photo_name(diretorio, indice)
        qtd_na_foto = count_objects(arquivo_atual, limiar_confianca)

        print(f"Imagem {indice} -> {arquivo_atual}: {qtd_na_foto} objeto(s)")

        soma_objetos += qtd_na_foto
        if qtd_na_foto == 0:
            imagens_sem_nada += 1

        indice += 1

    media_por_foto = soma_objetos / qtd_imagens
    print("\n--- Resumo do Diretório ---")
    print(f"Soma total de objetos: {soma_objetos}")
    print(f"Média por imagem: {media_por_foto:.2f}")
    print(f"Imagens vazias (0 objetos): {imagens_sem_nada}")


# Opção 5
def foto_mais_cheia_e_mais_vazia(limiar_confianca):
    print("\n=== Foto Mais Cheia e Mais Vazia ===")
    diretorio = ask_folder()
    qtd_imagens = total_photos(diretorio)

    # A primeira foto serve de base de comparação
    primeira_img = photo_name(diretorio, 1)
    qtd_inicial = count_objects(primeira_img, limiar_confianca)

    img_mais_cheia = primeira_img
    recorde_maior = qtd_inicial

    img_mais_vazia = primeira_img
    recorde_menor = qtd_inicial

    for idx in range(2, qtd_imagens + 1):
        img_atual = photo_name(diretorio, idx)
        qtd_atual = count_objects(img_atual, limiar_confianca)

        if qtd_atual > recorde_maior:
            recorde_maior = qtd_atual
            img_mais_cheia = img_atual

        if qtd_atual < recorde_menor:
            recorde_menor = qtd_atual
            img_mais_vazia = img_atual

    print(f"\nMais cheia: {img_mais_cheia} com {recorde_maior} objeto(s)")
    print(f"Mais vazia: {img_mais_vazia} com {recorde_menor} objeto(s)")


# Opção 6
def buscar_classe_na_pasta(limiar_confianca):
    print("\n=== Busca de Classe na Pasta ===")
    diretorio = ask_folder()
    qtd_imagens = total_photos(diretorio)
    alvo = pedir_classe("Informe a classe para buscar na pasta: ")

    fotos_positivas = 0
    soma_da_classe = 0

    for idx in range(1, qtd_imagens + 1):
        img_atual = photo_name(diretorio, idx)
        achados = count_class(img_atual, alvo, limiar_confianca)

        if achados > 0:
            fotos_positivas += 1
            soma_da_classe += achados

    percentual = (fotos_positivas / qtd_imagens) * 100

    print(f"\nResultado para '{alvo}' na pasta '{diretorio}' (confiança >= {limiar_confianca}):")
    print(f"Presente em {fotos_positivas} de {qtd_imagens} fotos ({percentual:.1f}%)")
    print(f"Total de aparições da classe: {soma_da_classe}")

    if soma_da_classe == 0:
        print("Aviso: nenhuma ocorrência encontrada. Verifique se digitou o nome da classe corretamente.")


# Opção 7
def grafico_de_barras(limiar_confianca):
    print("\n=== Gráfico de Barras da Pasta ===")
    diretorio = ask_folder()
    qtd_imagens = total_photos(diretorio)

    print(f"\nDistribuição de objetos em '{diretorio}' (confiança >= {limiar_confianca}):\n")

    for idx in range(1, qtd_imagens + 1):
        img_atual = photo_name(diretorio, idx)
        qtd_atual = count_objects(img_atual, limiar_confianca)

        barra_visual = ""
        for _ in range(qtd_atual):
            barra_visual = barra_visual + "="

        print(f"Foto {idx:02d} [{barra_visual}] {qtd_atual}")


# Opção 8
def ranking_top_n(resultados, limiar_confianca):
    print("\n=== Ranking Top N ===")
    inventario, ranking = montar_ranking(resultados, limiar_confianca)

    if len(ranking) == 0:
        print("Nenhum objeto com essa confiança mínima.")
    else:
        n_classes = pedir_inteiro(
            f"Quantas classes mostrar (1 a {len(ranking)}): ", 1, len(ranking))

        for posicao in range(n_classes):
            nome_classe, quantidade = ranking[posicao]
            print(f"{posicao + 1}. {nome_classe} - {quantidade}")


# Opção 9
def busca_reversa(resultados, limiar_confianca):
    print("\n=== Busca Reversa ===")
    alvo = pedir_classe("Informe a classe (ex.: car, person): ")
    indice_reverso = montar_indice_reverso(resultados, limiar_confianca)

    if alvo not in indice_reverso:
        print(f"A classe '{alvo}' não foi encontrada com confiança >= {limiar_confianca}.")
    else:
        print(f"Fotos com '{alvo}' (confiança >= {limiar_confianca}):")

        for foto in indice_reverso[alvo]:
            filtradas = filtrar_deteccoes(resultados[foto], limiar_confianca)
            quantidade = contar_classe_em(filtradas, alvo)
            print(f"  {foto}: {quantidade}")

        print(f"Total de fotos: {len(indice_reverso[alvo])}")


# Opção 10
def comparar_pastas(resultados, fotos_por_pasta, limiar_confianca):
    print("\n=== Comparação de Duas Pastas ===")
    print("Primeira pasta:")
    pasta_a = ask_folder()
    print("Segunda pasta:")
    pasta_b = ask_folder()

    conjunto_a = classes_da_pasta(resultados, fotos_por_pasta, pasta_a, limiar_confianca)
    conjunto_b = classes_da_pasta(resultados, fotos_por_pasta, pasta_b, limiar_confianca)

    print(f"\nComparando '{pasta_a}' e '{pasta_b}' (confiança >= {limiar_confianca}):\n")

    exibir_conjunto("Em comum", conjunto_a & conjunto_b)
    exibir_conjunto(f"Só em {pasta_a}", conjunto_a - conjunto_b)
    exibir_conjunto(f"Só em {pasta_b}", conjunto_b - conjunto_a)
    exibir_conjunto("União", conjunto_a | conjunto_b)


# Opção 11
def exibir_matriz(resultados, fotos_por_pasta, limiar_confianca):
    print("\n=== Matriz Pasta x Classe ===")
    inventario, ranking = montar_ranking(resultados, limiar_confianca)

    if len(ranking) == 0:
        print("Nenhum objeto com essa confiança mínima.")
    else:
        # Colunas na ordem do ranking (mais frequente primeiro)
        classes = []
        for nome_classe, quantidade in ranking:
            classes.append(nome_classe)

        pastas = list(fotos_por_pasta)
        matriz = montar_matriz(resultados, fotos_por_pasta, limiar_confianca, classes)
        totais_linhas, totais_colunas = totais_da_matriz(matriz)

        imprimir_matriz(pastas, classes, matriz, totais_linhas, totais_colunas)

        valor, pasta_top, classe_top = maior_da_matriz(matriz, pastas, classes)
        print(f"\nMaior valor: {valor} (pasta: {pasta_top}, classe: {classe_top})")


# Opção 12
def exibir_histograma(resultados, limiar_confianca):
    print("\n=== Histograma do Inventário ===")
    inventario, ranking = montar_ranking(resultados, limiar_confianca)

    if len(ranking) == 0:
        print("Nenhum objeto com essa confiança mínima.")
    else:
        print(f"\nObjetos por classe (confiança >= {limiar_confianca}), "
              f"da mais para a menos frequente:\n")
        imprimir_histograma(ranking)


# Opção 13
def exportar_relatorio(resultados, limiar_confianca):
    print("\n=== Salvar Relatório ===")
    inventario, ranking = montar_ranking(resultados, limiar_confianca)
    salvar_relatorio(inventario, ranking, limiar_confianca, ARQUIVO_RELATORIO)
    print(f"Relatório salvo em: {ARQUIVO_RELATORIO}")


# Opção 14
def mostrar_relatorio_salvo():
    print("\n=== Ler Relatório Salvo ===")
    ler_relatorio(ARQUIVO_RELATORIO)


# Opção 15
def inventario_do_acervo_ou_pasta(resultados, fotos_por_pasta, limiar_confianca):
    print("\n=== Inventário ===")
    show_folders()

    pasta_escolhida = input("Pasta (ou Enter para o acervo inteiro): ").strip()
    while pasta_escolhida != "" and pasta_escolhida not in fotos_por_pasta:
        print("Erro: essa pasta não foi encontrada.")
        pasta_escolhida = input("Pasta (ou Enter para o acervo inteiro): ").strip()

    if pasta_escolhida == "":
        lista_fotos = list(resultados)
        titulo = f"acervo inteiro (confiança >= {limiar_confianca})"
    else:
        lista_fotos = fotos_por_pasta[pasta_escolhida]
        titulo = f"pasta '{pasta_escolhida}' (confiança >= {limiar_confianca})"

    inventario = montar_inventario(resultados, lista_fotos, limiar_confianca)
    exibir_inventario(inventario, titulo)


# ==================== PRINCIPAL ====================

def main():
    limiar_confianca = 0.5
    rodando = True

    # O acervo é carregado uma única vez, para as opções 8 a 15.
    resultados, fotos_por_pasta = carregar_acervo()
    exibir_resumo(resultados, fotos_por_pasta, limiar_confianca)

    while rodando:
        exibir_menu()
        escolha = input("Sua opção: ").strip()

        if escolha == "0":
            print("Encerrando o PhotoCensus. Até logo!")
            rodando = False

        elif escolha == "1":
            limiar_confianca = ajustar_confianca(resultados, fotos_por_pasta, limiar_confianca)

        elif escolha == "2":
            inspecionar_foto(limiar_confianca)

        elif escolha == "3":
            contar_classe_na_foto(limiar_confianca)

        elif escolha == "4":
            relatorio_da_pasta(limiar_confianca)

        elif escolha == "5":
            foto_mais_cheia_e_mais_vazia(limiar_confianca)

        elif escolha == "6":
            buscar_classe_na_pasta(limiar_confianca)

        elif escolha == "7":
            grafico_de_barras(limiar_confianca)

        elif escolha == "8":
            ranking_top_n(resultados, limiar_confianca)

        elif escolha == "9":
            busca_reversa(resultados, limiar_confianca)

        elif escolha == "10":
            comparar_pastas(resultados, fotos_por_pasta, limiar_confianca)

        elif escolha == "11":
            exibir_matriz(resultados, fotos_por_pasta, limiar_confianca)

        elif escolha == "12":
            exibir_histograma(resultados, limiar_confianca)

        elif escolha == "13":
            exportar_relatorio(resultados, limiar_confianca)

        elif escolha == "14":
            mostrar_relatorio_salvo()

        elif escolha == "15":
            inventario_do_acervo_ou_pasta(resultados, fotos_por_pasta, limiar_confianca)

        else:
            print("Opção inválida! Escolha um número de 0 a 15.")


if __name__ == "__main__":
    main()




