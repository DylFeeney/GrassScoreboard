import unittest
import pandas as pd
from round import *

class RoundTest(unittest.TestCase):
    """
    Test for process_checkbox_list
    Test 1:
        Not selected
        Input: ['0', '0', '0', '0']
        Output: ['0', '0', '0', '0']

    Test 2:
        User 1 has selected the card
        Input: ['0', '1', '0', '0', '0']
        Output: ['1', '0', '0', '0']

    Test 3:
        User 1 and User 3 selected the card
        Input: ['0', '1', '0', '0', '1', '0']
        Output: ['1', '0', '1', '0']

    Test 4:
        All users selected the card
        Input: ['0', '1', '0', '1', '0', '1', '0', '1']
        Output: ['1', '1', '1', '1']
    """
    def test_process_checkbox_list_no_card_selected(self):
        input_list = ['0', '0', '0', '0']
        actual = process_checkbox_list(input_list)
        expected = ['0', '0', '0', '0']
        self.assertEqual(actual, expected)

    def test_process_checkbox_list_user_one_selected(self):
        input_list = ['0', '1', '0', '0', '0']
        actual = process_checkbox_list(input_list)
        expected = ['1', '0', '0', '0']
        self.assertEqual(actual, expected)

    def test_process_checkbox_list_user_one_user_three_selected(self):
        input_list = ['0', '1', '0', '0', '1', '0']
        actual = process_checkbox_list(input_list)
        expected = ['1', '0', '1', '0']
        self.assertEqual(actual, expected)

    def test_process_checkbox_list_all_users_selected(self):
        input_list = ['0', '1', '0', '1', '0', '1', '0', '1']
        actual = process_checkbox_list(input_list)
        expected = ['1', '1', '1', '1']
        self.assertEqual(actual, expected)

    @staticmethod
    def test_steal_money_using_banker_first_in_list():
        input_data = pd.DataFrame({
            'user_name': ['DYLAN', 'VICKY', 'DECLAN'],
            'unprotected_peddle': [45000, 50000, 5000]
            })
        steal_money_using_banker(input_data, 'DYLAN')
        expected = pd.DataFrame({
            'user_name': ['DYLAN', 'VICKY', 'DECLAN'],
            'unprotected_peddle': [55000, 45000, 0]
            })
        pd.testing.assert_series_equal(input_data['unprotected_peddle'], expected['unprotected_peddle'])

    @staticmethod
    def test_steal_money_using_banker_middle_in_list():
        input_data = pd.DataFrame({
            'user_name': ['DYLAN', 'VICKY', 'DECLAN'],
            'unprotected_peddle': [45000, 50000, 5000]
            })
        steal_money_using_banker(input_data, 'VICKY')
        expected = pd.DataFrame({
            'user_name': ['DYLAN', 'VICKY', 'DECLAN'],
            'unprotected_peddle': [40000, 60000, 0]
            })
        pd.testing.assert_series_equal(input_data['unprotected_peddle'], expected['unprotected_peddle'])

    @staticmethod
    def test_steal_money_using_banker_last_in_list():
        input_data = pd.DataFrame({
            'user_name': ['DYLAN', 'VICKY', 'DECLAN'],
            'unprotected_peddle': [45000, 50000, 5000]
        })
        steal_money_using_banker(input_data, 'DECLAN')
        expected = pd.DataFrame({
            'user_name': ['DYLAN', 'VICKY', 'DECLAN'],
            'unprotected_peddle': [40000, 45000, 15000]
        })
        pd.testing.assert_series_equal(input_data['unprotected_peddle'], expected['unprotected_peddle'])

    @staticmethod
    def test_calculate_net_profit_all_positive():
        input_data = pd.DataFrame({
            'user_name': ['DYLAN', 'VICKY', 'DECLAN'],
            'protected_peddle': [50000, 25000, 75000],
            'unprotected_peddle': [45000, 50000, 5000]
        })
        calculate_net_profit(input_data)
        expected = pd.DataFrame({
            'user_name': ['DYLAN', 'VICKY', 'DECLAN'],
            'net_profit': [95000, 75000, 80000]
        })
        pd.testing.assert_series_equal(input_data['net_profit'], expected['net_profit'])

    @staticmethod
    def test_calculate_net_profit_all_negative():
        input_data = pd.DataFrame({
            'user_name': ['DYLAN', 'VICKY', 'DECLAN'],
            'protected_peddle': [-50000, -25000, -75000],
            'unprotected_peddle': [-45000, -50000, -5000]
        })
        calculate_net_profit(input_data)
        expected = pd.DataFrame({
            'user_name': ['DYLAN', 'VICKY', 'DECLAN'],
            'net_profit': [-95000, -75000, -80000]
        })
        pd.testing.assert_series_equal(input_data['net_profit'], expected['net_profit'])

    @staticmethod
    def test_calculate_net_profit_negative_and_positive():
        input_data = pd.DataFrame({
            'user_name': ['DYLAN', 'VICKY', 'DECLAN'],
            'protected_peddle': [50000, -25000, -75000],
            'unprotected_peddle': [-45000, 50000, 5000]
        })
        calculate_net_profit(input_data)
        expected = pd.DataFrame({
            'user_name': ['DYLAN', 'VICKY', 'DECLAN'],
            'net_profit': [5000, 25000, -70000]
        })
        pd.testing.assert_series_equal(input_data['net_profit'], expected['net_profit'])

    @staticmethod
    def test_calculate_penalties_no_penalties():
        input_data = pd.DataFrame({
            'user_name': ['DYLAN', 'VICKY', 'DECLAN'],
            'net_profit': [100000, 75000, 25000],
            'has_sold_out': [0, 0, 0],
            'has_double_crossed': [0, 0, 0],
            'has_utterly_wiped_out': [0, 0, 0]
        })
        calculate_penalties(input_data)
        expected = pd.DataFrame({
            'user_name': ['DYLAN', 'VICKY', 'DECLAN'],
            'net_profit': [100000, 75000, 25000]
        })
        pd.testing.assert_series_equal(input_data['net_profit'], expected['net_profit'])

    @staticmethod
    def test_calculate_penalties_each_type():
        input_data = pd.DataFrame({
            'user_name': ['DYLAN', 'VICKY', 'DECLAN'],
            'net_profit': [100000, 50000, 25000],
            'has_sold_out': [0, 0, 1],
            'has_double_crossed': [0, 1, 0],
            'has_utterly_wiped_out': [1, 0, 0]
        })
        calculate_penalties(input_data)
        expected = pd.DataFrame({
            'user_name': ['DYLAN', 'VICKY', 'DECLAN'],
            'net_profit': [0, 0, 0]
        })
        pd.testing.assert_series_equal(input_data['net_profit'], expected['net_profit'])

    @staticmethod
    def test_calculate_penalties_each_type_2():
        input_data = pd.DataFrame({
            'user_name': ['DYLAN', 'VICKY', 'DECLAN'],
            'net_profit': [100000, 50000, 175000],
            'has_sold_out': [0, 1, 1],
            'has_double_crossed': [1, 1, 1],
            'has_utterly_wiped_out': [1, 0, 1]
        })
        calculate_penalties(input_data)
        expected = pd.DataFrame({
            'user_name': ['DYLAN', 'VICKY', 'DECLAN'],
            'net_profit': [-50000, -25000, 0]
        })
        pd.testing.assert_series_equal(input_data['net_profit'], expected['net_profit'])

    @staticmethod
    def test_calculate_penalties_each_type_3():
        input_data = pd.DataFrame({
            'user_name': ['DYLAN', 'VICKY', 'DECLAN'],
            'net_profit': [-100000, -50000, -175000],
            'has_sold_out': [0, 1, 1],
            'has_double_crossed': [1, 1, 1],
            'has_utterly_wiped_out': [1, 0, 1]
        })
        calculate_penalties(input_data)
        expected = pd.DataFrame({
            'user_name': ['DYLAN', 'VICKY', 'DECLAN'],
            'net_profit': [-250000, -125000, -350000]
        })
        pd.testing.assert_series_equal(input_data['net_profit'], expected['net_profit'])

    def test_calculate_best_peddle_5000(self):
        input_data = pd.DataFrame({
            'user_name': ['DYLAN', 'VICKY', 'DECLAN', 'PETER'],
            'highest_peddle_in_hand': [5000, 25000, 50000, 100000],
            'net_profit': [100000, 100000, 100000, 100000]
        })
        calculate_best_peddle(input_data)
        expected = pd.DataFrame({
            'user_name': ['DYLAN', 'VICKY', 'DECLAN', 'PETER'],
            'net_profit': [95000, 75000, 50000, 0]
        })
        pd.testing.assert_series_equal(input_data['net_profit'], expected['net_profit'])

    def test_calculate_round(self):
        round_information = pd.DataFrame({
            'user_name': ['DYLAN', 'VICKY', 'DECLAN'],
            'protected_peddle': [50000, 25000, 75000],
            'unprotected_peddle': [45000, 50000, 5000],
            'highest_peddle_in_hand': [5000, 50000, 25000],
            'has_banker': [1, 0, 0],
            'has_sold_out': [1, 0, 0],
            'has_double_crossed': [0, 0, 0],
            'has_utterly_wiped_out': [0, 1, 0]
        })


