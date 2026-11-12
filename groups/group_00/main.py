import os
import sys

# Configura o caminho para importar o módulo black_box da pasta kit
caminho_atual = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(caminho_atual, "..", "..", "kit"))
from black_box import *


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


def exibir_menu():
    print("\n========================================")
    print("         PHOTOCENSUS - SISTEMA          ")
    print("========================================")
    print("[1] Ajustar confiança mínima")
    print("[2] Inspecionar uma única foto")
    print("[3] Contar classe específica em uma foto")
    print("[4] Gerar relatório completo da pasta")
    print("[5] Buscar foto mais cheia e mais vazia")
    print("[6] Buscar classe específica na pasta")
    print("[7] Exibir gráfico de barras em texto")
    print("[0] Encerrar programa")
    print("========================================")


def main():
    limiar_confianca = 0.5
    rodando = True

    while rodando:
        exibir_menu()
        escolha = input("Sua opção: ").strip()

        if escolha == "0":
            print("Encerrando o PhotoCensus. Até logo!")
            rodando = False

        elif escolha == "1":
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

        elif escolha == "2":
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

        elif escolha == "3":
            print("\n=== Contagem de Classe na Foto ===")
            caminho_img = ask_photo()
            show_classes()

            nome_classe = ""
            while nome_classe == "":
                nome_classe = input("Qual classe deseja contar? ").strip().lower()
                if nome_classe == "":
                    print("O nome da classe não pode ser vazio.")

            ocorrencias = count_class(caminho_img, nome_classe, limiar_confianca)
            print(f"Classe pesquisada: [{nome_classe}]")
            print(f"Total encontrado na imagem (confiança >= {limiar_confianca}): {ocorrencias}")

        elif escolha == "4":
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

        elif escolha == "5":
            print("\n=== Foto Mais Cheia e Mais Vazia ===")
            diretorio = ask_folder()
            qtd_imagens = total_photos(diretorio)

            # Analisa a primeira foto fora do laço para servir de base de comparação
            primeira_img = photo_name(diretorio, 1)
            qtd_inicial = count_objects(primeira_img, limiar_confianca)

            img_mais_cheia = primeira_img
            recorde_maior = qtd_inicial

            img_mais_vazia = primeira_img
            recorde_menor = qtd_inicial

            # Começa o laço a partir da foto 2
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

        elif escolha == "6":
            print("\n=== Busca de Classe na Pasta ===")
            diretorio = ask_folder()
            qtd_imagens = total_photos(diretorio)

            show_classes()
            alvo = ""
            while alvo == "":
                alvo = input("Informe a classe para buscar na pasta: ").strip().lower()
                if alvo == "":
                    print("Digite um nome de classe válido.")

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

        elif escolha == "7":
            print("\n=== Gráfico de Barras da Pasta ===")
            diretorio = ask_folder()
            qtd_imagens = total_photos(diretorio)

            print(f"\nDistribuição de objetos em '{diretorio}' (confiança >= {limiar_confianca}):\n")

            for idx in range(1, qtd_imagens + 1):
                img_atual = photo_name(diretorio, idx)
                qtd_atual = count_objects(img_atual, limiar_confianca)

                # Constrói a barra com um laço for e o símbolo '='
                barra_visual = ""
                for _ in range(qtd_atual):
                    barra_visual = barra_visual + "="

                print(f"Foto {idx:02d} [{barra_visual}] {qtd_atual}")

        else:
            print("Opção inválida! Escolha um número de 0 a 7.")


if __name__ == "__main__":
    main()