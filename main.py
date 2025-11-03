import csv
import sys

from argparse import ArgumentParser
from tabulate import tabulate


REPORT_CHOISES = {
    'brand-rating-average': ['brand', 'rating'],
    'brand-price-average': ['brand', 'price'],
    'name-rating-average': ['name', 'rating'],
    'name-price-average': ['name', 'price'],
}


def create_parser():
    """Функция получения аргументов командной строки."""

    parser = ArgumentParser(description='Report Parser')

    parser.add_argument(
        '--report',
        type=str,
        choices=list(REPORT_CHOISES),
        default='brand-rating-average',
        help='Наименование отчета'
    )
    parser.add_argument(
        '--files',
        type=str,
        nargs="+",
        help='Наименования файлов для составления отчета'
    )
    parser.add_argument(
        '--dir-path',
        type=str,
        default='./files/',
        help='Директория с файлами'
    )

    return parser


def create_report_data(parser: ArgumentParser) -> tuple:
    """Функция парсинга csv файлов и формирования сводного отчета."""

    args = parser.parse_args()

    report_name = args.report
    files_data = args.files
    dir_path = args.dir_path
    position_value, culculated_value = REPORT_CHOISES[report_name]

    if files_data:

        summary_report = {}

        for current_file in files_data:

            with open(f'{dir_path}{current_file}', mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    summary_report.setdefault(row[position_value], []).append(float(row[culculated_value]))

        report_data = [[key, round(sum(values) / len(values), 2)] for key, values in summary_report.items()]
        report_data.sort(key=lambda i: i[1], reverse=True)

        headers = [position_value, culculated_value]

        return report_name, report_data, headers

    sys.exit('Не указаны файлы для парсинга!')


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
        parser = create_parser()

        report_name, report_data, headers = create_report_data(
            parser
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
