import os
from black_box import *
from ui_utils import *
from module1_ops import *
from data_engine import *

GROUP_DIR = os.path.dirname(os.path.abspath(__file__))


def handle_folder_option(option, folder, min_conf):
    """Route Module 1 folder-based options (2 to 7)."""
    if option == "2" or option == "3":
        num = ask_photo_number(folder)
        if option == "2":
            photo, total_objs, main_obj, highest_conf = get_photo_stats(folder, num, min_conf)
            print_photo_analysis(photo, total_objs, main_obj, highest_conf)
        else:
            photo = photo_name(folder, num)
            class_name = ask_class_name()
            total_class = count_class(photo, class_name, min_conf)
            print_class_in_photo(photo, class_name, total_class, min_conf)
    elif option == "4":
        total_objs, avg, empty = compute_folder_report(folder, min_conf)
        print_folder_summary(total_objs, avg, empty)
    elif option == "5":
        m_num, m_qtd, l_num, l_qtd = find_population_extremes(folder, min_conf)
        print_population_extremes(folder, min_conf, m_num, m_qtd, l_num, l_qtd)
    elif option == "6":
        class_name = ask_class_name()
        total_app, phts_with, pct = search_class_stats(folder, class_name, min_conf)
        print_class_search(folder, class_name, total_app, phts_with, pct)
    elif option == "7":
        print_bar_chart(folder, min_conf)


def handle_module2_option(option, results, min_conf):
    """Route Module 2 dataset-wide options (8 to 14)."""
    if option == "8":
        scope = ask_binary_choice("Inventory for [1] Whole dataset or [2] Specific folder? ")
        folder = ask_folder() if scope == "2" else ""
        inv = build_inventory(results, min_conf, folder)
        print_inventory(inv, folder if folder else "Whole Dataset", min_conf)
    elif option == "9":
        n = ask_top_n()
        ranking = build_ranking(build_inventory(results, min_conf))
        print_ranking(ranking, n, min_conf)
    elif option == "10":
        target = ask_class_name()
        rev_idx = build_reverse_index(results, min_conf)
        details = get_reverse_search_details(results, rev_idx, target, min_conf)
        print_reverse_search(target, details, min_conf)
    elif option == "11":
        print("Select First Folder:")
        f1 = ask_folder()
        print("Select Second Folder:")
        f2 = ask_folder()
        c, oa, ob, u = compare_folder_sets(
            get_folder_classes_set(results, f1, min_conf),
            get_folder_classes_set(results, f2, min_conf),
        )
        print_set_comparison(f1, f2, c, oa, ob, u)
    elif option == "12":
        folders, classes, matrix, r_tot, c_tot, peak = build_folder_class_matrix(results, min_conf)
        print_matrix(folders, classes, matrix, r_tot, c_tot, peak)
    elif option == "13":
        ranking = build_ranking(build_inventory(results, min_conf))
        print_ranking_histogram(ranking, min_conf)
    elif option == "14":
        action = ask_binary_choice("[1] Save report.txt or [2] Read report.txt? ")
        report_path = os.path.join(GROUP_DIR, "report.txt")
        if action == "1":
            inv = build_inventory(results, min_conf)
            save_report_file(report_path, inv, build_ranking(inv), min_conf)
        else:
            read_report_file(report_path)