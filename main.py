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
    """Вспомогательная функция проверки наличия аргументов."""

    if not args.report:
        raise ArgumentError(
            report_param, 'Не выбран параметр наименования отчета'
        )
    if not args.files:
        raise ArgumentError(
            files_param, 'Не выбран параметр файлов для составления отчета'
        )


def get_parser_args(args=None):
    """Функция получения аргументов командной строки."""

    parser = ArgumentParser(description='Report Parser')

    report = parser.add_argument(
        '--report',
        type=str,
        choices=list(REPORT_CHOISES),
        help='Наименование отчета'
    )
    files = parser.add_argument(
        '--files',
        type=str,
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

    for current_file in files_data:
        try:
            current_files_path = os.path.join(dir_path, current_file)
            with open(current_files_path, mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    summary_report.setdefault(
                        row[position_value], []
                    ).append(float(row[culculated_value]))

        except:
            raise Exception(
                f'Несуществующая директория или файл "{current_files_path}"'
            )

    report_data = [
        [key, round(sum(values) / len(values), 2)]
        for key, values in summary_report.items()
    ]
    report_data.sort(key=lambda i: i[1], reverse=True)

    headers = [position_value, culculated_value]

    return report_name, report_data, headers


def print_report_table(
    report_name: str,
    report_data: list,
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

        dir_path = input('Укажите путь к месту расположения файлов: ')

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
        sys.exit(1)


if __name__ == '__main__':
    main()
