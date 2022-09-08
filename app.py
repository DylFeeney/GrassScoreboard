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


#background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
    print ("Hello")
    return ("nothing")


if __name__ == '__main__':
    app.run()
