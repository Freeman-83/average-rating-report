import csv

from argparse import ArgumentParser
from tabulate import tabulate


REPORT_CHOISES = {
    'brand-rating-average': ['brand', 'rating'],
    'brand-price-average': ['brand', 'price'],
    'name-rating-average': ['name', 'rating'],
    'name-price-average': ['name', 'price'],
}


def get_parser_args(parser: ArgumentParser) -> tuple:
    """Функция получения аргументов командной строки."""

    parser.add_argument(
        '--report',
        choices=list(REPORT_CHOISES),
        default='brand-rating-average',
        type=str,
        help='Наименование отчета'
    )
    parser.add_argument(
        '--files',
        type=str,
        nargs="+",
        help='Выберите файлы'
    )
    parser.add_argument(
        '--dir-path',
        default='./files/',
        type=str,
        help='Путь к файлам'
    )

    report_name = parser.parse_args().report
    files_data = parser.parse_args().files
    dir_path = parser.parse_args().dir_path

    return report_name, files_data, dir_path


def create_report_data(
    files_data: list,
    dir_path: str,
    position_row: str,
    culculating_row: str
) -> tuple[list, str, str]:
    """Функция парсинга файлов csv и формирования сводного отчета."""

    elem_report = {}

    for current_file in files_data:

        with open(f'{dir_path}{current_file}', mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                elem_report.setdefault(row[position_row], []).append(float(row[culculating_row]))

    report_data = [[key, round(sum(values_list) / len(values_list), 2)] for key, values_list in elem_report.items()]
    report_data.sort(key=lambda i: i[1], reverse=True)

    return report_data, position_row, culculating_row


def print_report_table(
    report_name: str,
    report_data: dict,
    position_row: str,
    culculating_row: str
):
    """Функция консольного вывода отчетной таблицы."""

    table = tabulate(
        report_data,
        headers = [position_row, culculating_row],
        tablefmt='outline',
        showindex=(indx for indx, _ in enumerate(report_data, start=1))
    )

    print(report_name, table, sep='\n')


def main():

    parser = ArgumentParser(description='Report')

    try:
        report_name, files_data, dir_path = get_parser_args(parser)

        report_data, position_row, culculating_row = create_report_data(
            files_data,
            dir_path,
            *REPORT_CHOISES[report_name]
        )

        print_report_table(report_name, report_data, position_row, culculating_row)
    
    except Exception as e:
        print(f'Ошибка в работе программы: {e}')


if __name__ == '__main__':
    main()
