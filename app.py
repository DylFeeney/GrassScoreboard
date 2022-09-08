from flask import Flask, render_template
import csv
from game_setup import player_setup_page, file_setup_page
from round import round_information_page, calculate_round_page, get_round_number_values
import pandas as pd

app = Flask(__name__)
app.register_blueprint(player_setup_page)
app.register_blueprint(file_setup_page)
app.register_blueprint(round_information_page)
app.register_blueprint(calculate_round_page)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')

@app.route('/new-round')
def new_round():
    return "New round created"

def get_current_number_of_rounds():
    df = pd.read_csv('game_files/round_number.csv')

@app.route('/csv')
def print_csv():
    fields = ['user_number_one', 'user_name_one']
    with open(r'game_files/user_info.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
    return 'CSV Info'


@app.route('/generate')
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
        row = [str(i), 0]
        writer.writerow(row)
    f.close()

def generate_user_file():
    f = open('game_files/user_info.csv', 'w')
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



#background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
    print ("Hello")
    return ("nothing")


if __name__ == '__main__':
    app.run()
