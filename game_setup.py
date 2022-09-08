from flask import request, render_template, Blueprint
import csv
import pandas as pd
from round import process_checkbox_list


player_setup_page = Blueprint('player_setup_page', __name__, template_folder='templates')
@player_setup_page.route('/player-setup', methods=['POST', 'GET'])
def player_setup():
    if request.method == 'POST':
        user_name = request.form['name']
        processed_user_name = user_name.upper()
        add_user_to_game(processed_user_name)
    df = pd.read_csv('game_files/user_info.csv')
    names = df['user_name']
    return render_template('setup.html', user_names=names)


def add_user_to_game(user_name):
    fields = ['1', user_name]
    with open(r'game_files/user_info.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(fields)


file_setup_page = Blueprint('file_setup_page', __name__, template_folder='templates')
@file_setup_page.route('/file-setup', methods=['POST', 'GET'])
def game_file_setup():
    if request.method == 'POST':
        user_file = process_checkbox_list(request.form.getlist('reset_user_file'))
        print(user_file)
        round_info_file = process_checkbox_list(request.form.getlist('reset_round_info_file'))
        print(round_info_file)
        processed_round_info_file = process_checkbox_list(request.form.getlist('reset_processed_round_info_file'))
        print(processed_round_info_file)
    return render_template('game_file_setup.html')
