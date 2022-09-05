from flask import Flask, render_template
import csv
from game_setup import game_setup_page
from round import round_information_page, calculate_round_page

app = Flask(__name__)
app.register_blueprint(game_setup_page)
app.register_blueprint(round_information_page)
app.register_blueprint(calculate_round_page)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/csv')
def print_csv():
    fields = ['user_number_one', 'user_name_one']
    with open(r'game_files/user_info.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
    return 'CSV Info'


@app.route('/generate')
def generate_files():
    generate_user_file()
    generate_round_info_file()
    return 'Generated files'


def generate_user_file():
    f = open('game_files/user_info.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')
    user_name_row = ['user_number', 'user_name']
    writer.writerow(user_name_row)
    f.close()


def generate_round_info_file():
    f = open('game_files/round_information_files/round_information.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')
    round_information_row = ['user_name', 'protected_peddle', 'unprotected_peddle', 'highest_peddle_in_hand',
                             'has_banker', 'has_sold_out', 'has_double_crossed', 'has_utterly_wiped_out']
    writer.writerow(round_information_row)
    f.close()


if __name__ == '__main__':
    app.run()
