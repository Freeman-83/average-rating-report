from argparse import ArgumentParser

from main import (
    create_parser,
    create_report_data,
    print_report_table
)


# def test_create_parser():

#     # args = get_parser_args(parser)

#     # print(parser.argument_default)

#     # print(list(dict(args)))

#     args_list = ['report', 'files', 'dir_path']

    # for i in range(len(args)):
    #     assert args[i] == args_list[i]


# 'brand-rating-average', 'products1.csv products2.csv'


def test_create_report_data():

    parser = ArgumentParser(description='test-parser')

    res = parser.parse_args(['--files', 'products1.csv', 'products2.csv'])

    # files_data = ['products1.csv', 'products2.csv']
    # dir_path = './files/'
    # position_row = 'brand'
    # culculating_row = 'rating'

    res = (
        [['apple', 4.55], ['samsung', 4.53], ['xiaomi', 4.37]],
        'brand',
        'rating'
    )

    assert create_report_data(
        parser
    ) == res
