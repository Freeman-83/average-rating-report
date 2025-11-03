import csv
import os
import sys

from argparse import ArgumentParser, ArgumentError
from tabulate import tabulate


REPORT_CHOISES = {
    'average-rating': ['brand', 'rating'],
    # 'average-price': ['brand', 'price'],
}


def check_parser_args(report_param, files_param, args):

    if not args.report:
        raise ArgumentError(
            report_param, 'Не выбран параметр наименования отчета'
        )
    if not args.files:
        raise ArgumentError(
            files_param, 'Не выбран параметр с файлами для составления отчета'
        )


def check_type_args(arg):
    if not isinstance(arg, str):
        raise TypeError('Некорректный тип данных аргументов')
    return arg


def get_parser_args(args=None):
    """Функция получения аргументов командной строки."""
    
    parser = ArgumentParser(description='Report Parser')

    report = parser.add_argument(
        '--report',
        type=check_type_args,
        choices=list(REPORT_CHOISES),
        help='Наименование отчета'
    )
    files = parser.add_argument(
        '--files',
        type=check_type_args,
        nargs='+',
        help='Перечень файлов для составления отчета',
    )

    parser_args = parser.parse_args(args)

    check_parser_args(report, files, parser_args)

    return parser_args


def create_report_data(report_name, files_data, dir_path) -> tuple:
    """Функция парсинга csv файлов и формирования сводного отчета."""

    position_value, culculated_value = REPORT_CHOISES[report_name]

    summary_report = {}

    try:
        for current_file in files_data:
            with open(os.path.join(dir_path, current_file), mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    summary_report.setdefault(row[position_value], []).append(float(row[culculated_value]))
    except:
       raise Exception('Директория или файл не найдены')

    
    report_data = [[key, round(sum(values) / len(values), 2)] for key, values in summary_report.items()]
    report_data.sort(key=lambda i: i[1], reverse=True)

    headers = [position_value, culculated_value]

    return report_name, report_data, headers


def print_report_table(
    report_name: str,
    report_data: dict,
    headers: list
):
    """Функция консольного вывода отчетной таблицы."""

    table = tabulate(
        report_data,
        headers=headers,
        tablefmt='outline',
        showindex=range(1, len(report_data) + 1)
    )

    print(report_name, table, sep='\n')


def main():

    try:
        args = get_parser_args()

        print(args)

        dir_path = input('Введите путь к месту расположения файлов: ')

        report_name, report_data, headers = create_report_data(
            args.report,
            args.files,
            dir_path
        )

        print_report_table(
            report_name,
            report_data,
            headers
        )

    except Exception as e:
        print(f'Ошибка в работе программы: {e}')


if __name__ == '__main__':
    main()
