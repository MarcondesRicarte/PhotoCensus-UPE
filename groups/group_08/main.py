import os
import sys

GROUP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(GROUP_DIR, "..", "..", "kit"))
from black_box import *

# A partir dessa parte, produzi o que seriam as funções de validação e a formatação auxiliar do projeto
def get_valid_folder(): # opção 2 à 7
    show_folders()
    while True:
        folder = input("Digite o nome da pasta: ").strip()
        if folder == "":
            print("Erro: O nome da pasta não pode estar em branco. Tente novamente.")
        elif not folder_exists(folder):
            print(f"Erro: A pasta '{folder}' não existe. Tente novamente.")
        else:
            return folder

def get_valid_photo_number(folder): #opção 2 e 3 
    total = total_photos(folder)
    while True:
        entrada = input(f"Digite o número da foto (1 a {total}): ").strip()
        if entrada.isdigit():
            number = int(entrada)
            if 1 <= number <= total:
                return number
        print(f"Erro: Digite um número inteiro entre 1 e {total}.")

def get_valid_confidence(): #opção 1
    while True:
        entrada = input("Digite a confiança mínima (0.0 a 1.0): ")
        try:
            conf = float(entrada)
            if 0.0 <= conf <= 1.0:
                return conf
            print("Erro: A confiança deve estar entre 0.0 e 1.0.")
        except ValueError:
            print("Erro: Digite um número decimal válido (Ex: 0.5).")

def get_valid_class_name(): #opção 3 e 6
    show_classes()
    class_name = input("Digite o nome da classe (ex: car, person): ").strip().lower()
    valid_classes = ",airplane,apple,backpack,banana,baseball bat,baseball glove,bear,bed,bench,bicycle,bird,boat,book,bottle,bowl,broccoli,bus,cake,car,carrot,cat,cell phone,chair,clock,couch,cow,cup,dining table,dog,donut,elephant,fire hydrant,fork,frisbee,giraffe,hair drier,handbag,horse,hot dog,keyboard,kite,knife,laptop,microwave,motorcycle,mouse,orange,oven,parking meter,person,pizza,potted plant,refrigerator,remote,sandwich,scissors,sheep,sink,skateboard,skis,snowboard,spoon,sports ball,stop sign,suitcase,surfboard,teddy bear,tennis racket,tie,toaster,toilet,toothbrush,traffic light,train,truck,tv,umbrella,vase,wine glass,zebra,"
    
    while True:
        if class_name == "":
            print("Erro: O nome da classe não pode estar em branco.")
            class_name = input("Digite o nome da classe (ex: car, person): ").strip().lower()
        elif "," in class_name or f",{class_name}," not in valid_classes:
            print("Erro: O nome da classe não está listada. Tente novamente.")
            class_name = input("Digite o nome da classe (ex: car, person): ").strip().lower()
        else:
            return class_name

def get_short_photo_name(photo_path):
    filename = os.path.basename(photo_path)
    return filename.replace(".jpg", "").replace(".jpeg", "").replace(".png", "")
    
# A partir daqui, fui programando as funções da operação do programa (que vai da opção 2 a 7)
def analyze_photo(min_conf):  # 1. Entrada e caminho: Valida a pasta/número e monta o caminho real da imagem
    folder = get_valid_folder()
    number = get_valid_photo_number(folder)
    path = photo_name(folder, number) # Função da black-box (Os índices começam em 1)

    total_objs = count_objects(path, min_conf) # 2. As consultas na black-box: 1 - count_objects filtra pela confiança mínima escolhida pelo usuário; 2- main_object e max_confidence sempre retornam o objeto mais forte da foto (0.0 a 1.0)
    top_obj = main_object(path)
    top_conf_percent = max_confidence(path) * 100
    
    print("\n--- Análise da Foto ---") # 3. Saída formatada: :.0f serve para arredondar a porcentagem sem casas decimais
    print(f"Caminho: {path}")
    print(f"Total de objetos (conf = {min_conf}): {total_objs}")
    if top_obj == "":
        print("Objeto principal: Nenhum objeto detectado.")
    else:
        print(f"Objeto principal: {top_obj}")
        print(f"Maior confiança: {top_conf_percent:.0f}%")

def count_class_in_photo(min_conf): # 1. Entrada: Vai validar a pasta, número da foto e nome da classe desejada!
    folder = get_valid_folder()
    number = get_valid_photo_number(folder)
    path = photo_name(folder, number)
    target_class = get_valid_class_name()

    amount = count_class(path, target_class, min_conf) # 2. Contagem pontual: count_class conta apenas objetos daquela classe >= min_conf
    short_name = get_short_photo_name(path)

# 3. Saída: Vai informar quantos itens da classe existem naquela imagem específica
    print(f"\nResultado: Foram encontrados {amount} objeto(s) da classe '{target_class}' em '{short_name}' (conf = {min_conf}).")

def folder_report(min_conf): # 1. Preparação: Serve para descobrir quantas fotos existem na pasta para definir o limite do 'for'
    folder = get_valid_folder()
    total_pics = total_photos(folder)

    grand_total = 0 # Acumulador (soma de objetos) 
    empty_photos = 0 # Contador (fotos zeradas)

    print(f"\n--- Relatório da Pasta: {folder} (conf = {min_conf}) ---") # 2. Varredura com for: Percorre da foto 1 até total_pics (inclusive, por isso + 1)
    for i in range(1, total_pics + 1): 
        path = photo_name(folder, i)
        objs = count_objects(path, min_conf)
        print(f"{get_short_photo_name(path)}: {objs} objeto(s)")

        grand_total += objs # Atualiza o total geral e verifica se a foto ficou vazia na confiança atual
        if objs == 0:
            empty_photos += 1

    average = grand_total / total_pics if total_pics > 0 else 0.0 # 3. Cálculo da média: Protegido contra divisão por zero caso a pasta estivesse vazia

    print("-"*45)
    print(f"Total geral de objetos: {grand_total}")
    print(f"Média de objetos por foto: {average:.2f}")
    print(f"Foto(s) sem objetos: {empty_photos}")

def fullest_and_emptiest_photos(min_conf): # 1. Preparação: Vai validar a pasta e obter o total de imagens
    folder = get_valid_folder()
    total_pics = total_photos(folder)

    if total_pics <= 0:
        print(f"\nAviso: A pasta '{folder}' não possui fotos.")
        return

    first_path = photo_name(folder, 1) # 2. Inicialização: Começa assumindo que a primeira foto é a mais cheia e a mais vazia
    first_count = count_objects(first_path, min_conf)

    max_photo = first_path
    max_objs = first_count

    min_photo = first_path
    min_objs = first_count

    for i in range(2, total_pics + 1): # Comparação manual: Como a foto 1 já foi lida, o 'for' começa na foto 2
        path = photo_name(folder, i)
        objs = count_objects(path, min_conf)

        if objs > max_objs: # Se encontrar uma foto com MAIS objetos que o recorde atual, substitui
            max_objs = objs
            max_photo = path

        if objs < min_objs: # Se encontrar uma foto com MENOS objetos que o recorde atual, substitui
            min_objs = objs
            min_photo = path

    print(f"\n--- Extremos da pasta '{folder}' (conf = {min_conf}) ---")
    print(f"Foto mais cheia: {get_short_photo_name(max_photo)} com {max_objs} objeto(s)")
    print(f"Foto mais vazia: {get_short_photo_name(min_photo)} com {min_objs} objeto(s)")

def search_class_in_folder(min_conf): # 1. Entrada e variáveis de controle
    folder = get_valid_folder()
    target_class = get_valid_class_name()

    total_pics = total_photos(folder)
    photos_with_class = 0
    total_found = 0

    for i in range(1, total_pics + 1): # 2. Varredura da pasta: Testa foto por foto buscando apenas a classe escolhida
        path = photo_name(folder, i)
        amount = count_class(path, target_class, min_conf)

        if amount > 0: # Só incrementa se a classe apareceu pelo menos 1 vez naquela foto
            photos_with_class += 1
            total_found += amount

# 3. Porcentagem de presença: (fotos onde apareceu / total de fotos) * 100
    presence_percent = (photos_with_class / total_pics ) * 100 if total_pics > 0 else 0.0

    print(f"\n--- Busca da classe '{target_class}' em '{folder}' (conf = {min_conf}) ---")
    print(f"Aparece em: {photos_with_class} de {total_pics} fotos ({presence_percent:.1f}%)")
    print(f"Quantidade total encontrada: {total_found}")

def folder_bar_chart(min_conf): # 1. Preparação: Valida a pasta e pega a quantidade de fotos
    folder = get_valid_folder()
    total_pics = total_photos(folder)

    print(f"\n--- Gráfico de Objetos: {folder} (conf = {min_conf}) ---")
    for i in range(1, total_pics + 1): # 2. Laço externo (Fotos): Percorre cada imagem da pasta
        path = photo_name(folder, i)
        objs = count_objects(path, min_conf)
        label = get_short_photo_name(path)

        bar = "" # 3. Laço interno (Barras): Requisito para desenhar a barra de '#' proporcional à quantidade de objetos encontrados
        for _ in range(objs):
            bar += "█"

        print(f"{label:<15} | {bar} ({objs})")

# E aqui, o menu principal do programa, que vai chamar todas as funções acima de acordo com a escolha do usuário
def show_menu(min_conf):
    print("\n"+"="*45)
    print(f" PhotoCensus - Group 08 (Confiança: {min_conf})")
    print("=" * 45)
    print("1- Configurar confiança mínima")  
    print("2- Analisar uma foto")
    print("3- Contar uma classe na foto")
    print("4- Relatório da pasta")
    print("5- Foto mais cheia e mais vazia da pasta")
    print("6- Procurar uma classe na pasta")
    print("7- Gráfico de objetos por foto na pasta")
    print("0- Sair")
    print("=" * 45)

def main():
    min_confidence = 0.5 # Confiança padrão inicial exigida

    while True:
        show_menu(min_confidence)
        option = input("Escolha uma opção: ").strip()

        if option == "1":
            min_confidence = get_valid_confidence()
            print(f"Confiança mínima atualizada para {min_confidence}.")

        elif option == "2":
            analyze_photo(min_confidence)

        elif option == "3":
            count_class_in_photo(min_confidence)

        elif option == "4":
            folder_report(min_confidence)

        elif option == "5":
            fullest_and_emptiest_photos(min_confidence)

        elif option == "6":
            search_class_in_folder(min_confidence)
        
        elif option == "7":
            folder_bar_chart(min_confidence)

        elif option == "0":
            print("Encerrando PhotoCensus...")
            break

        else:
            print("Opção inválida! Digite um número de 0 a 7.")

if __name__ == "__main__":
    main()