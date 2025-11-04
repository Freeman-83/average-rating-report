import csv
import os
import sys

from argparse import (
    ArgumentError,
    ArgumentParser,
    ArgumentTypeError,
    Namespace
)

from tabulate import tabulate


REPORT_CHOISES = {
    'average-rating': ['brand', 'rating'],
    # 'average-price': ['brand', 'price'], # добавление дополнительного отчета
}


def check_exist_parser_args(report_param, files_param, args) -> None:
    """Вспомогательная функция проверки наличия аргументов."""

    if not args.report:
        raise ArgumentError(
            report_param, 'Не указано наименование отчета'
        )
    if not args.files:
        raise ArgumentError(
            files_param, 'Не выбраны файлы для составления отчета'
        )


def check_empty_input(arg) -> str | None:
    """Вспомогательная функция проверки пустого значения аргумента."""

    if not arg:
        raise ArgumentTypeError('Пустое значение аргумета')
    return arg


def get_parser_args(args=None) -> Namespace:
    """Функция получения аргументов командной строки."""

    parser = ArgumentParser(description='Report Parser')

    report = parser.add_argument(
        '--report',
        type=check_empty_input,
        choices=list(REPORT_CHOISES),
        help='Наименование отчета'
    )
    files = parser.add_argument(
        '--files',
        type=check_empty_input,
        nargs='+',
        help='Перечень файлов для составления отчета',
    )

    parser_args = parser.parse_args(args)

    check_exist_parser_args(report, files, parser_args)

    return parser_args


def create_report_data(
    report_name: str,
    files_data: list,
    dir_path: str
) -> tuple[str, list, list]:
    """Функция парсинга csv файлов и формирования сводного отчета."""

    position_value, culculated_value = REPORT_CHOISES[report_name]

    summary_report: dict[str, list] = {}

    for current_file in files_data:
        try:
            current_files_path = os.path.join(dir_path, current_file)
            with open(current_files_path, mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    summary_report.setdefault(
                        row[position_value], []
                    ).append(float(row[culculated_value]))

        except KeyError:
            raise KeyError(
                f'В файле "{current_file}" отсутствует позиция "{position_value}"'
            )

        except Exception:
            raise FileNotFoundError(
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
) -> None:
    """Функция консольного вывода таблицы с отчетом."""

    report_table = tabulate(
        report_data,
        headers=headers,
        tablefmt='outline',
        showindex=range(1, len(report_data) + 1)
    )

    print(report_name, report_table, sep='\n')


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
