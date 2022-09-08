import csv
from round import get_round_number_values


def generate_all_files():
    number_of_rounds = get_round_number_values()
    generate_round_number_file()
    generate_user_file()
    generate_round_info_file(number_of_rounds)
    generate_processed_round_info_files(number_of_rounds)
    return 'Generated files'


def generate_round_number_file():
    f = open('game_files/round_number.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')
    round_number_row = ['round_number', 'round_played']
    writer.writerow(round_number_row)
    for i in range(1, 10):
        row = [str(i), "Not yet played"]
        writer.writerow(row)
    f.close()


def generate_user_file():
    f = open('game_files/user_info.csv', 'w+')
    writer = csv.writer(f, lineterminator='\n')
    user_name_row = ['user_number', 'user_name']
    writer.writerow(user_name_row)
    f.close()


def generate_files(number_of_rounds, file_path_front, file_path_back, fields):
    for i in range(len(number_of_rounds)):
        file_path = file_path_front + str(number_of_rounds[i]) + file_path_back
        print(file_path)
        f = open(file_path, 'w+')
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(fields)
        f.close()


def generate_round_info_file(round_numbers):
    file_path_front = "game_files/round_information_files/round_information_"
    file_path_back = ".csv"
    round_information_row = ['round_number', 'user_name', 'protected_peddle', 'unprotected_peddle',
                             'highest_peddle_in_hand',
                             'has_banker', 'has_sold_out', 'has_double_crossed', 'has_utterly_wiped_out']
    generate_files(round_numbers, file_path_front, file_path_back, round_information_row)


def generate_processed_round_info_files(round_numbers):
    file_path_front = "game_files/round_processed_files/processed_round_information_"
    file_path_back = ".csv"
    fields = ['user_name', 'protected_peddle', 'unprotected_peddle', 'highest_peddle_in_hand', 'has_banker',
              'has_sold_out', 'has_double_crossed', 'has_utterly_wiped_out', 'net_profit']
    generate_files(round_numbers, file_path_front, file_path_back, fields)