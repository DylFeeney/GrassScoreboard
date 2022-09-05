from flask import request, render_template, Blueprint
import csv
import pandas as pd


game_setup_page = Blueprint('game_setup_page', __name__, template_folder='templates')
@game_setup_page.route('/setup', methods=['POST', 'GET'])
def game_setup():
    if request.method == 'POST':
        user_name = request.form['name']
        processed_user_name = user_name.upper()
        add_user_to_game(processed_user_name)
    df = pd.read_csv('game_files/user_info.csv')
    names = df['user_name']
    print(names)
    return render_template('setup.html', user_names=names)


def add_user_to_game(user_name):
    fields = ['1', user_name]
    with open(r'game_files/user_info.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(fields)
