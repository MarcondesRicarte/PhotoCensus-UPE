import os
import sys

# Adiciona a pasta kit ao caminho do Python
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "kit"))
from black_box import *




# ============================================================
# FUNÇÃO ask_folder
# Objetivo: pedir o nome de uma pasta e só aceitar quando ela for válida.
# ============================================================
def ask_folder():

    # [0] mostra as pastas
    show_folders()
    # [1] Pede o nome da pasta. O .strip() tira espaços das pontas
    #     (assim "  street " vira "street").
    folder = input("Digite o nome da pasta (ex: street, animals, sports): ").strip()

    # [2] Laço de validação: repete ENQUANTO a pasta for inválida.
    #     Ela é inválida se QUALQUER uma das 3 condições for verdadeira (por isso o "or"):
    #       - folder == ""                -> o usuário só apertou Enter
    #       - not folder_exists(folder)   -> a pasta não existe em images/
    #       - total_photos(folder) == 0   -> existe, mas não tem fotos (pega ".." e "kit")
    #     A ordem importa: se a primeira for verdadeira, o Python nem testa as outras.
    while folder == "" or not folder_exists(folder) or total_photos(folder) == 0:
        print("Pasta inválida. Tente novamente.")
        # [3] Pede de novo DENTRO do laço; sem isso ele repetiria para sempre.
        folder = input("Digite o nome da pasta (ex: street, animals, sports): ").strip()

    # [4] Chegou aqui = pasta válida. O "return" entrega o valor para quem chamou a função.
    return folder





# ============================================================
# FUNÇÃO ask_photo
# Objetivo: pedir pasta + número da foto (os dois validados).
# ============================================================
def ask_photo():
    # [1] Primeiro pede a pasta, já validada, usando a função do passo 1.
    #     (uma função pode chamar outra função)
    folder = ask_folder()

    # [2] Guarda quantas fotos a pasta tem e mostra para o usuário.
    total = total_photos(folder)
    print(f"A pasta '{folder}' tem {total} fotos.")

    # [3] number começa em 0 DE PROPÓSITO: 0 é inválido, então o while entra pelo menos uma vez.
    number = 0

    # [4] Repete ENQUANTO o número estiver fora do intervalo de 1 até o total.
    while number < 1 or number > total:
        typed = input(f"Escolha o número da foto (1 a {total}): ").strip()

        # [5] int() dá ValueError se o texto não for inteiro (abc, 2.7, vazio).
        #     Em vez de quebrar, o except coloca number = 0 (inválido) e o laço repete.
        try:
            number = int(typed)
        except ValueError:
            number = 0

        # [6] Só mostra o erro se o número ficou inválido.
        if number < 1 or number > total:
            print(f"Número inválido. Digite um número inteiro de 1 a {total}.")

    # [7] Pasta e número válidos: monta e devolve o caminho da foto.
    return photo_name(folder, number)




















def main():
    print("PhotoCensus - Group 02")
    
    # Inicializando variáveis globais do programa
    execution = True
    confidence_level = 0.5  # Valor padrão de exemplo
    

    while execution:    
        print("        Menu do PhotoCensus")
        print("""
        1 --> Configurar confiança mínima
        2 --> Analisar uma foto
        3 --> Contar uma classe na foto
        4 --> Relatório da pasta 
        5 --> Foto mais cheia e mais vazia
        6 --> Procurar uma classe na pasta
        7 --> Gráfico de barras em texto
        0 --> Sair""")

        decision = input("Escolha uma opção: ")

        if decision == "0":
            execution = False
            
        elif decision == "1":

            print("\n--- Configurar confiança mínima ---")

            ## 1) Mostra o valor atual da confiança
            print(f"Nível de confiança atual: {confidence_level}")

            while True :

                ##2) aqui recebemos o novo valor em str pra fazer devidas correções para não quebrar o programa
                Atualizacao_confianca_str = input ("Digite o novo valor a ser atribuído à confiança: ")
                Atualizacao_confianca_str = Atualizacao_confianca_str.strip()
                Atualizacao_confianca_str = Atualizacao_confianca_str.replace(",",".")

                ## 3)O try protege o programa contra valores inválidos impedindo o sistema quebrar
                try :
                    Atualizacao_confianca = float(Atualizacao_confianca_str)
                    
                    
                ## 4) Se o valor digitado pelo usuário der algum erro, ele cai no except e o laço é executado novamente pedindo um novo valor
                except ValueError:
                    print ("Você digitou um valor errado. Por favor, digite um valor válido (entre 0 e 1) e não tente quebrar o programa!")
                    continue
                
                ## 5) Se virou número, só aceita se estiver entre 0 e 1. Escrito do jeito "positivo" para também rejeitar nan e inf
                if 0 <= Atualizacao_confianca <= 1:
                    print ("Valor aceito!")
                    confidence_level = Atualizacao_confianca
                    break

                ## 6) Se chegou aqui, o número estava fora do intervalo: avisa, e o laço volta a pedir sozinho
                print ("Valor inválido, escolha um valor no intervalo de 0 a 1. Por favor não tente quebrar o código!")


            ## 7) Mostra o valor que ficou configurado
            print(f"Novo nível de confiança: {confidence_level}")
            

        elif decision == "2":

            print("\n--- Analisar uma foto ---")

            
            
            photo = ask_photo()

            # 2) Busca os dados da foto
            total_objs = count_objects(photo, confidence_level)

            # 3) Mostra o resultado
            print(f"\nFoto: {photo}")
            print(f"Objetos detectados (confiança >= {confidence_level}): {total_objs}")
            if total_objs > 0:
                main_obj = main_object(photo)
                best_conf = max_confidence(photo)
                print(f"Objeto principal: {main_obj}")
                print(f"Maior confiança: {best_conf * 100:.0f}%")
            else:
                print("Nenhum objeto com essa confiança mínima.")
            print()
            

        elif decision == "3":
            print ("\n--- Contar uma classe na foto ---")
            # [1] Pergunta a foto
            photo = ask_photo()

            # [2] Mostra as classes que o modelo reconhece (a função já imprime sozinha)
            show_classes()

            # [3] Pede a classe. .strip() tira espaços e .lower() deixa minúsculo
            classe = input("Diga a classe: ").strip().lower()

            # [4] Não aceita vazio: repete enquanto o usuário não digitar nada
            while classe == "":
                print("Você não digitou nada. Tente novamente.")
                classe = input("Diga a classe: ").strip().lower()

            # [5] Mostra a classe escolhida, entre colchetes, para conferir
            print(f"Classe escolhida: [{classe}]")

            amount = count_class(photo,classe,confidence_level)

            print(f"Objetos da classe '{classe}' (confiança >= {confidence_level}): {amount}")

        elif decision == "4":
            print("\n--- Relatório da pasta ---")
            
            # ask_folder() já rejeita pasta inválida e pasta sem fotos
            pasta = ask_folder()
            total_fotos = total_photos(pasta)

            total_objetos = 0    # acumulador: soma dos objetos de todas as fotos
            fotos_vazias = 0     # contador: fotos com 0 objetos

            # for percorre todas as fotos; range(1, total + 1) porque as
            # fotos começam em 1 e o range para antes do último número
            for numero in range(1, total_fotos + 1):
                foto = photo_name(pasta, numero)
                quantidade = count_objects(foto, confidence_level)

                # Uma linha por foto com a quantidade de objetos
                print(f"Foto {numero} | {foto} | {quantidade} objeto(s)")

                total_objetos = total_objetos + quantidade   # acumula o total
                if quantidade == 0:
                    fotos_vazias = fotos_vazias + 1          # conta foto vazia

            # total_fotos nunca é 0 aqui, pois ask_folder() rejeita pasta sem fotos
            media = total_objetos / total_fotos

            # Resumo final do relatório
            print("\nTotal geral de objetos:", total_objetos)
            print(f"Média de objetos por foto: {media:.2f}")
            print("Fotos sem nenhum objeto:", fotos_vazias)


        elif decision == "5":
            print("\n--- Foto mais cheia e Foto mais vazia ---")
            
                    # ask_folder() já rejeita pasta inválida e pasta sem fotos
            pasta = ask_folder()
            total_fotos = total_photos(pasta)

            # Variáveis de apoio. max() e min() são PROIBIDOS no Módulo 1,
            # então guardamos "o melhor até agora" e comparamos com if dentro do laço.
            maior_quantidade = 0     # maior número de objetos visto até agora
            foto_mais_cheia = ""     # caminho da foto que tem esse maior número
            menor_quantidade = 0     # menor número de objetos visto até agora
            foto_mais_vazia = ""     # caminho da foto que tem esse menor número

            # for percorre todas as fotos; as fotos começam em 1
            for numero in range(1, total_fotos + 1):
                foto = photo_name(pasta, numero)
                quantidade = count_objects(foto, confidence_level)

                if numero == 1:
                    # [1] Na primeira foto não há com quem comparar:
                    #     ela é ao mesmo tempo a maior e a menor até agora.
                    maior_quantidade = quantidade
                    foto_mais_cheia = foto
                    menor_quantidade = quantidade
                    foto_mais_vazia = foto
                else:
                    # [2] Nas próximas, só troca se achar uma foto MELHOR.
                    #     Usamos > e < (sem o "=") para, em caso de empate,
                    #     valer a primeira foto encontrada.
                    if quantidade > maior_quantidade:
                        maior_quantidade = quantidade
                        foto_mais_cheia = foto
                    if quantidade < menor_quantidade:
                        menor_quantidade = quantidade
                        foto_mais_vazia = foto

            # [3] Terminado o laço, mostra o resultado
            print(f"\nFoto mais cheia: {foto_mais_cheia} ({maior_quantidade} objetos)")
            print(f"Foto mais vazia: {foto_mais_vazia} ({menor_quantidade} objetos)")

        elif decision == "6":
            print("\n--- Procurar uma classe na pasta ---")
            
                    # [1] ask_folder() já rejeita pasta inválida e pasta sem fotos
            pasta = ask_folder()
            total_fotos = total_photos(pasta)

            # [2] Mostra as classes que o modelo reconhece (a função já imprime sozinha)
            show_classes()

            # [3] Pede a classe. .strip() tira espaços e .lower() deixa minúsculo
            classe = input("Diga a classe (ex.: car, person): ").strip().lower()

            # [4] Não aceita vazio: repete enquanto o usuário não digitar nada
            while classe == "":
                print("Você não digitou nada. Tente novamente.")
                classe = input("Diga a classe (ex.: car, person): ").strip().lower()

            # [5] Variáveis de apoio (sum() é proibido, então contamos à mão)
            fotos_com_classe = 0    # contador: em quantas fotos a classe aparece
            total_encontrado = 0    # acumulador: quantidade total de objetos da classe

            # [6] for percorre todas as fotos; as fotos começam em 1
            for numero in range(1, total_fotos + 1):
                foto = photo_name(pasta, numero)
                quantidade = count_class(foto, classe, confidence_level)

                # Só conta a foto se a classe apareceu pelo menos uma vez nela
                if quantidade > 0:
                    fotos_com_classe = fotos_com_classe + 1
                    total_encontrado = total_encontrado + quantidade

            # [7] Porcentagem de fotos da pasta em que a classe aparece
            #     (total_fotos nunca é 0, pois ask_folder() rejeita pasta sem fotos)
            porcentagem = fotos_com_classe / total_fotos * 100

            # [8] Mostra o resultado
            print(f"\nClasse: '{classe}' | pasta: '{pasta}' | confiança >= {confidence_level}")
            print(f"Aparece em {fotos_com_classe} de {total_fotos} fotos.")
            print(f"Quantidade total encontrada: {total_encontrado}")
            print(f"Porcentagem de fotos com a classe: {porcentagem:.1f}%")
            if total_encontrado == 0:
                # count_class devolve 0 tanto para "não tem na pasta" quanto para
                # classe digitada errada; por isso lembramos de conferir a lista
                print("Nenhum encontrado. Confira se a classe está na lista acima.")
            
        elif decision == "7":
            print("\n--- Gráfico de barras em texto ---")

            # [1] Pede a pasta já validada e descobre o total de fotos
            pasta = ask_folder()
            total_fotos = total_photos(pasta)

            print(f"\nGráfico de objetos por foto na pasta '{pasta}' (confiança >= {confidence_level}):\n")

            # [2] Percorre todas as fotos da pasta (de 1 até total_fotos)
            for numero in range(1, total_fotos + 1):
                foto = photo_name(pasta, numero)
                quantidade = count_objects(foto, confidence_level)

                # [3] Constrói a barra repetindo o caractere '#' de acordo com a quantidade
                #     (Se o seu professor exigir laço em vez de multiplicação de string,
                #      veja a alternativa logo abaixo)
                barra = "#" * quantidade

                # [4] Exibe o número da foto, a barra e a quantidade entre parênteses
                print(f"Foto {numero:2d} | {barra} ({quantidade})")
            
        else:
            print("Escolha incorreta. Escolha uma opção válida\n")

if __name__ == "__main__":
    main()