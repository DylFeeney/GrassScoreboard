from flask import request, render_template, Blueprint
import csv
import pandas as pd
from round import process_checkbox_list, get_round_number_values
from file import generate_user_file, generate_round_info_file, generate_processed_round_info_files, generate_round_number_file


player_setup_page = Blueprint('player_setup_page', __name__, template_folder='templates')
@player_setup_page.route('/player-setup', methods=['POST', 'GET'])
def player_setup():
    if request.method == 'POST':
        user_name = request.form['name']
        processed_user_name = user_name.upper()
        add_user_to_game(processed_user_name)
    df = pd.read_csv('game_files/user_info.csv')
    names = df['user_name']
    return render_template('player-setup.html', user_names=names)


def add_user_to_game(user_name):
    fields = ['1', user_name]
    with open(r'game_files/user_info.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(fields)


file_setup_page = Blueprint('file_setup_page', __name__, template_folder='templates')
@file_setup_page.route('/file-setup', methods=['POST', 'GET'])
def game_file_setup():
    if request.method == 'POST':
        number_of_rounds = get_round_number_values()

        user_file = process_checkbox_list(request.form.getlist('reset_user_file'))
        if user_file[0] == str(1):
            generate_user_file()
        round_number_file = process_checkbox_list(request.form.getlist('reset_round_number_file'))

        if round_number_file[0] == str(1):
            generate_round_number_file()
        round_info_file = process_checkbox_list(request.form.getlist('reset_round_info_file'))

        if round_info_file[0] == str(1):
            generate_round_info_file(number_of_rounds)
        processed_round_info_file = process_checkbox_list(request.form.getlist('reset_processed_round_info_file'))

        if processed_round_info_file[0] == str(1):
            generate_processed_round_info_files(number_of_rounds)

    return render_template('game_file_setup.html')
