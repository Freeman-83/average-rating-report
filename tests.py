from argparse import ArgumentParser

from main import (
    get_parser_args,
    create_report_data,
    print_report_table
)


parser = ArgumentParser()


def test_create_report_data():

    files_data = 'products1.csv products2.csv'
    dir_path = './files/'
    position_row = 'brand'
    culculating_row = 'rating'

    res = (
        [['apple', 4.55], ['samsung', 4.53], ['xiaomi', 4.37]],
        'brand',
        'rating'
    )

    assert create_report_data(
        files_data,
        dir_path,
        position_row,
        culculating_row
    ) == res


def test_true():
    assert True