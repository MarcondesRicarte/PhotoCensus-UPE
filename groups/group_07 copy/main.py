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
    diretorio = perguntar_pasta()
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
            caminho_imagem = perguntar_foto()
            detectados = count_objects(caminho_imagem, confidence_pad_level)
            print(f"\n Arquivo analisado: {caminho_imagem}")
            print(f"Quantidade de objetos(confiança minima de {confidence_pad_level}): {detectados}")

            if detectados > 0:
                objetos_destaque = main_object(caminho_imagem)
                maior_taxa = max_confidence(caminho_imagem)*100
                print(f"Objetos de destaque: {objetos_destaque}")
                print(f"Maior taxa de confiança: {maior_taxa:.2f}%")
            else:
                print("Nenhum objeto atingiu a confiança desejada.")

        elif decision == "3":
            print("\n--Contar uma classe de fotos:")
            caminho_imagem = perguntar_foto()
            show_classes()


            nome_classe=""
            while nome_classe=="":
                nome_classe = input("Digite o nome da classe desejada: ").lower().strip()
                if nome_classe=="":
                    print("Nome da classe não pode ser vazio. Tente novamente.")

            ocorrencias = count_class(caminho_imagem, nome_classe, confidence_pad_level)
            print(f"\nClasse pesquisada: {nome_classe}")
            print(f"Total encontrado na imagem (confiança >= {confidence_pad_level}): {ocorrencias}")

        elif decision == "4":
            print("\n--Relatorio da pasta:")
            diretorio = perguntar_pasta()
            qtd_imagens = total_photos(diretorio)

            soma_objetos = 0
            imagens_sem_nada = 0
            indice = 1

            while indice <= qtd_imagens:
                arquivo_atual = photo_name(diretorio, indice)
                qtd_na_foto = count_objects(arquivo_atual, confidence_pad_level)

                print(f"Imagem {indice} -> {arquivo_atual}: {qtd_na_foto} objeto(s)")

                soma_objetos += qtd_na_foto
                if qtd_na_foto == 0:
                    imagens_sem_nada += 1

                indice += 1

            media_por_foto = soma_objetos / qtd_imagens
            print("\n--- Resumo do Diretório ---")
            print(f"\nSoma total de objetos encontrados na pasta '{diretorio}': {soma_objetos}")
            print(f"Total de imagens sem objetos: {imagens_sem_nada}")
            print(f"Média de objetos por imagem: {media_por_foto:.2f}")

        elif decision == "5":
            print("\n--Foto mais cheia e mais vazia:")
            diretorio = perguntar_pasta()
            qtd_imagens = total_photos(diretorio)
            primeira_imagem = photo_name(diretorio, 1)
            quantidade_inicial = count_objects(primeira_imagem, confidence_pad_level)
            imagem_mais_cheia = primeira_imagem
            recorde_mais_cheia = quantidade_inicial
            imagem_mais_vazia = primeira_imagem
            recorde_mais_vazia = quantidade_inicial
            for idx in range (2,qtd_imagens+1):
                imagem_atual = photo_name(diretorio, idx)
                quantidade_atual = count_objects(imagem_atual, confidence_pad_level)
                if quantidade_atual > recorde_mais_cheia:
                    recorde_mais_cheia = quantidade_atual
                    imagem_mais_cheia = imagem_atual
                if quantidade_atual < recorde_mais_vazia:
                    recorde_mais_vazia = quantidade_atual
                    imagem_mais_vazia = imagem_atual
            print(f"\nImagem mais cheia: {imagem_mais_cheia} com {recorde_mais_cheia} objeto(s)")        
            print(f"Imagem mais vazia: {imagem_mais_vazia} com {recorde_mais_vazia} objeto(s)")

        elif decision == "6":
            print("\n--Procurar classe na pasta:")
            diretorio = perguntar_pasta()
            qtd_imagens = total_photos(diretorio)
            show_classes()
            alvo = ""
            while alvo == "":
                alvo = input("Digite o nome da classe desejada: ").lower().strip()
                if alvo == "":
                    print("Nome da classe não pode ser vazio. Tente novamente.")

            fotos_positivas = 0
            soma_da_classe = 0
            for idx in range(1, qtd_imagens + 1):
                imagem_atual = photo_name(diretorio, idx)
                achados = count_class(imagem_atual, alvo, confidence_pad_level)
                if achados > 0:
                    fotos_positivas += 1
                    soma_da_classe += achados
            percentual = (fotos_positivas / qtd_imagens) * 100
            
            print(f"\nResultados para a classe '{alvo}' na pasta '{diretorio}' (confiança >={confidence_pad_level})':")
            print(f"Presente em {fotos_positivas} de {qtd_imagens} fotos ({percentual:.2f}%)")
            print(f"Total de aparições da classe: {soma_da_classe}")

        elif decision =="7":
            print("\n--Grafico de barras da classe:")
            diretorio = perguntar_pasta()
            qtd_imagens = total_photos(diretorio)
            print(f"\nDistribuição de objetos em {diretorio} (confiança >={confidence_pad_level}):")
            for idx in range(1, qtd_imagens + 1):
                imagem_atual = photo_name(diretorio, idx)
                qtd_na_foto = count_objects(imagem_atual, confidence_pad_level)
                barra_visual = ""
                for _ in range(qtd_na_foto):
                    barra_visual = barra_visual + "="
                print(f"Imagem {idx:02d}: [{barra_visual}] ({qtd_na_foto} objeto(s))")

        else:
            print("Opção inválida. Tente novamente um número de 1 a 7.")



if __name__ == "__main__":
    main()
