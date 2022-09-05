from flask import request, render_template, Blueprint
import csv
import pandas as pd
import numpy as np

round_information_page = Blueprint('round_information_page', __name__, template_folder='templates')
calculate_round_page = Blueprint('calculate_round_page', __name__, template_folder='templates')


@round_information_page.route('/round-information', methods=['POST', 'GET'])
def round_information():
    df = pd.read_csv('game_files/user_info.csv')
    names = df['user_name']
    number_of_players = len(names)
    if request.method == 'POST':
        user_name, protected_peddle, unprotected_peddle, highest_peddle_in_hand, has_banker, has_sold_out, \
        has_double_crossed, has_utterly_wiped_out = get_request_form_values(request)
        process_round(number_of_players, user_name, protected_peddle, unprotected_peddle, highest_peddle_in_hand,
                      has_banker, has_sold_out, has_double_crossed, has_utterly_wiped_out)
    return render_template('round_information.html', number_of_players=number_of_players, names=names)


def get_request_form_values(incoming_request):
    user_name = incoming_request.form.getlist('user_name')
    protected_peddle = incoming_request.form.getlist('protected_peddle')
    unprotected_peddle = incoming_request.form.getlist('unprotected_peddle')
    highest_peddle_in_hand = incoming_request.form.getlist('highest_peddle_in_hand')
    has_banker = process_checkbox_list(incoming_request.form.getlist('has_banker'))
    has_sold_out = process_checkbox_list(incoming_request.form.getlist('has_sold_out'))
    has_double_crossed = process_checkbox_list(incoming_request.form.getlist('has_double_crossed'))
    has_utterly_wiped_out = process_checkbox_list(incoming_request.form.getlist('has_utterly_wiped_out'))
    return user_name, protected_peddle, unprotected_peddle, highest_peddle_in_hand, has_banker, has_sold_out, \
           has_double_crossed, has_utterly_wiped_out


def process_checkbox_list(input_list):
    """
    This function will validate the checkbox values that are input from the webpage
    If a checkbox is not ticked a '0' is inputted.
    If a checkbox is ticket a '0' is inputted followed by a '1'.
    Because a '0' & a '1' are inputted we need to remove the 0 and keep the 1.

    Example
    Two inputs - 0,0,1
    Input one = 0 (Not checked)
    Input two = 0,1 (Checked) - We need to remove the 0 from here
    Expected output - 0,1

    Example
    Two inputs - 0,1,0,1
    Input one = 0,1 (Checked) - We need to remove the 0 from here
    Input two = 0,1 (Checked) - We need to remove the 0 from here
    Expected output - 1,1

    Example
    Two inputs - 0,1,0
    Input one = 0,1 (Checked) - We need to remove the 0 from here
    Input two = 0 (Not checked)
    Expected output - 1,0
    """
    list_length = len(input_list)
    skip_until = -1
    updated_list = []
    # Loop over the list of checkbox inputs
    for i in range(list_length):
        # Ensure the loop does not run out of bounds
        if (i + 1) < list_length:
            # Skip the next value
            if i <= skip_until:
                continue
            else:
                current_value = input_list[i]
                next_value = input_list[i + 1]
                if current_value == '0' and next_value == '1':
                    updated_list.append('1')
                    if i + 1 < list_length:
                        # Skip the next index to ensure when we get an input of 0,1 (checked box)
                        skip_until = i + 1
                else:
                    updated_list.append('0')
        elif (i + 1) == list_length:
            if i <= skip_until:
                continue
            else:
                updated_list.append(input_list[i])
    return updated_list


def process_round(length, user_name, protected_peddle, unprotected_peddle, highest_peddle_in_hand, has_banker,
                  has_sold_out,
                  has_double_crossed, has_utterly_wiped_out):
    write_round_information_to_file(length, user_name, protected_peddle, unprotected_peddle, highest_peddle_in_hand,
                                    has_banker,
                                    has_sold_out, has_double_crossed, has_utterly_wiped_out)
    calculate_round()


def write_round_information_to_file(length, user_name, protected_peddle, unprotected_peddle, highest_peddle_in_hand,
                                    has_banker,
                                    has_sold_out, has_double_crossed, has_utterly_wiped_out):
    with open(r'game_files/round_information_files/round_information.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        for i in range(length):
            fields = [user_name[i], protected_peddle[i], unprotected_peddle[i], highest_peddle_in_hand[i],
                      has_banker[i],
                      has_sold_out[i], has_double_crossed[i], has_utterly_wiped_out[i]]
            writer.writerow(fields)


@calculate_round_page.route('/calc')
def calculate_round():
    data = read_round_information_file()
    banker_card_status, player_name = banker_card_played(data)
    if banker_card_status:
        steal_money_using_banker(data, player_name)
    calculate_net_profit(data)
    calculate_penalties(data)
    calculate_best_peddle(data)
    calculate_bonus(data)
    write_processed_round_info(data)
    return 'Calculated round'


def read_round_information_file():
    df = pd.read_csv('game_files/round_information_files/round_information.csv')
    return df


def banker_card_played(input_data):
    """
    Determine if the Banker Card has been used. If so this is needed when calculating who to take money from and give it to
    """
    has_banker_row = input_data.loc[input_data['has_banker'] == 1]
    if has_banker_row.empty:
        return False, 'no_player'
    else:
        player_name = has_banker_row['user_name'].values[0]
        return True, player_name


def steal_money_using_banker(input_data_file, player_name):
    """
    player_name is the user who had played the banker card. This person is going to
    steal from all other players unprotected peddle cards

    [x] - Identify the user who had the banker card - banker_user
    [x] - Get all other users
    [x] - Loop over each of the users
        [x] - Check if there unprotected peddle card value is >= 5000
        [x] - if true
            [x] - remove 5000 from the user
            [x] - add 5000 to the stolen_money
        [X] - else
            [X] - do nothing to this user
    [x] - Add the stolen_value oo the banker_user unprotected peddle value
    [] - Return the updated data
    """
    # Identify the user who had the banker card - banker_user
    banker_user = input_data_file.loc[input_data_file['user_name'] == player_name]
    # Get all other users
    users_to_steal_from = input_data_file.loc[input_data_file['user_name'] != player_name]

    # Loop over the users_to_steal_from and remove 5000 from their unprotected_peddle if they have enough money
    # and add the money to the stolen_money for the banker_player
    stolen_money = 0
    for i in users_to_steal_from.index:
        current_users_unprotected = users_to_steal_from.at[i, 'unprotected_peddle']
        if current_users_unprotected >= 5000:
            stolen_money = stolen_money + 5000
            users_to_steal_from.at[i, 'unprotected_peddle'] = current_users_unprotected - 5000

    # Get the value of the banker_user unprotected_peddle and add the stolen_money onto it
    banker_user_unprotected = banker_user['unprotected_peddle'].values[0]
    updated_banker_user_unprotected = banker_user_unprotected + stolen_money

    # Update the banker_user to give them the stolen money
    update_unprotected_peddle_after_banker(input_data_file, player_name, updated_banker_user_unprotected)

    # Get the names and the updated unprotected_peddle values for the users_to_steal_from
    users_to_steal_from_names = users_to_steal_from['user_name']
    users_to_steal_from_updated_unprotected = users_to_steal_from['unprotected_peddle']

    # Update the banker_user to remove the stolen money
    for i in range(len(users_to_steal_from_names)):
        current_user_being_robbed = users_to_steal_from_names.values[i]
        current_user_being_robbed_new_unprotected = users_to_steal_from_updated_unprotected.values[i]
        update_unprotected_peddle_after_banker(input_data_file, current_user_being_robbed,
                                               current_user_being_robbed_new_unprotected)


def update_unprotected_peddle_after_banker(input_data, current_player_name, new_unprotected_peddle_value):
    # Get the index in the DataFrame of the banker_user to update their unprotected_peddle value
    index = input_data[input_data['user_name'] == current_player_name].index.values[0]

    # Update the banker_user unprotected_peddle value to account for the stolen_money
    input_data.at[index, 'unprotected_peddle'] = new_unprotected_peddle_value


def calculate_net_profit(input_data):
    """
    Each player adds their protected and at-risk profits to determine their net profit.
    """
    net_profit = []
    # Finding the index and adding 1 as the index is off by one without
    largest_index = input_data.index.values[-1] + 1
    # Looping over the entire DataFrame from 0 to the last index number and getting the net profit for each row
    for i in range(largest_index):
        protected_peddle = input_data.loc[i]['protected_peddle']
        unprotected_peddle = input_data.loc[i]['unprotected_peddle']
        net_profit.append(protected_peddle + unprotected_peddle)
    # Adding the new net_profit values to the DataFrame
    input_data['net_profit'] = net_profit


def calculate_penalties(input_data):
    """
    Calculate the penalties from players holding specific cards in their hands
    Sold Out -$25,000
    Double crossed -$50,000
    Utterly Wiped Out -$100,000
    """
    # Setting the penalty values
    sold_out_penalty = -25000
    double_crossed_penalty = -50000
    utterly_wiped_out_penalty = -100000

    # Finding the index and adding 1 as the index is off by one without
    largest_index = input_data.index.values[-1] + 1
    # Looping over the entire DataFrame from 0 to the last index number and getting the net profit for each row
    for i in range(largest_index):
        if input_data.loc[i]['has_sold_out'] == 1:
            apply_peddle_value(input_data, i, sold_out_penalty)

        if input_data.loc[i]['has_double_crossed'] == 1:
            apply_peddle_value(input_data, i, double_crossed_penalty)

        if input_data.loc[i]['has_utterly_wiped_out'] == 1:
            apply_peddle_value(input_data, i, utterly_wiped_out_penalty)


def apply_peddle_value(input_data, index, new_peddle_value):
    net_profit = input_data.loc[index]['net_profit']
    input_data.at[index, 'net_profit'] = net_profit + new_peddle_value


def calculate_best_peddle(input_data):
    """
    Remove the best peddle card in each persons hand from their profit for the round
    """
    # Finding the index and adding 1 as the index is off by one without
    largest_index = input_data.index.values[-1] + 1
    # Looping over the entire DataFrame from 0 to the last index number and getting the net profit for each row
    for i in range(largest_index):
        # Get the highest peddle card
        highest_peddle = input_data.loc[i]['highest_peddle_in_hand']
        # Forcing the highest_peddle value to be a negative. The value 0 will still be 0
        highest_peddle = -abs(highest_peddle)
        apply_peddle_value(input_data, i, highest_peddle)


def calculate_bonus(input_data):
    """
    Determine who receives the bonus of $25,000 for having the largest profit for this round
    """
    max_profit_bonus = 25000

    # Getting the max_profit from the net_profit column
    max_profit = input_data['net_profit'].max()
    """
    Check that the max_profit value is only in the output once (Two players do not have the same value which is 
    determined as the max_profit)
    
    Get the count of all the values in the net_profit column
    Returned data example
    75000   2
    -25000  1
    105000  1
    The max here is 105000 and we only have one instance.
    """
    max_profit_count = input_data['net_profit'].value_counts()
    """
    In the returned count value, the net_profit is the index. We can search the DataFrame for the max_profit
    and this will return the count value
    """
    max_profit_count = max_profit_count.loc[max_profit]
    if max_profit_count == 1:
        # Getting the row in the DataFrame that contains the highest profit
        index = input_data.loc[input_data['net_profit'] == max_profit].index.values[0]
        apply_peddle_value(input_data, index, max_profit_bonus)
    """
    Check that the max_profit value is only in the output once (Two players do not have the same value which is 
    determined as the max_profit)
    """
    return False


def write_processed_round_info(input_data):
    # Get the largest index in the DataFrame to write each row to the file
    # Need to add 1 as the index is off by one without
    largest_index = input_data.index.values[-1] + 1
    with open(r'game_files/round_processed_files/processed_round_information.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        heading_row = ['user_name', 'protected_peddle', 'unprotected_peddle', 'highest_peddle_in_hand', 'has_banker',
                       'has_sold_out', 'has_double_crossed', 'has_utterly_wiped_out', 'net_profit']
        writer.writerow(heading_row)
        for i in range(largest_index):
            fields = [input_data.at[i, 'user_name'], input_data.at[i, 'protected_peddle'],
                      input_data.at[i, 'unprotected_peddle'], input_data.at[i, 'highest_peddle_in_hand'],
                      input_data.at[i, 'has_banker'], input_data.at[i, 'has_sold_out'],
                      input_data.at[i, 'has_double_crossed'], input_data.at[i, 'has_utterly_wiped_out'],
                      input_data.at[i, 'net_profit']]
            writer.writerow(fields)

    print('Writing to file')


"""
def write_round_information_to_file(length, user_name, protected_peddle, unprotected_peddle, highest_peddle_in_hand, has_banker, has_sold_out, has_double_crossed, has_utterly_wiped_out):
    with open(r'game_files/round_information_files/round_information.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        for i in range(length):
            fields = [user_name[i], protected_peddle[i], unprotected_peddle[i], highest_peddle_in_hand[i],
                      has_banker[i],
                      has_sold_out[i], has_double_crossed[i], has_utterly_wiped_out[i]]
            writer.writerow(fields)
"""
