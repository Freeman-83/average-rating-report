import pytest

from argparse import ArgumentError

from main import (
    get_parser_args,
    create_report_data,
    print_report_table,
)

test_input_data = {
    'correct_args_data': [
        '--report', 'average-rating',
        '--files', 'products1.csv', 'products2.csv'
    ],
    'args_data_without_report_name': [
        '--files', 'products1.csv', 'products2.csv'
    ],
    'args_data_without_files': [
        '--report', 'average-rating'
    ],
    'incorrect_type_args': ['--report', 1, '--files', True],
    'empty_args': ['--report', '', '--files', ''],
    'nonexistent_parsing_position': [
        '--report', 'average-rating',
        '--files', 'products1.csv', 'products3.csv'
    ],
    'nonexistent_file': [
        '--report', 'average-rating',
        '--files', 'products1.csv', 'products4.csv'
    ],
}


def test_get_parser_args():
    """Проверка корректности передаваемых параметров и аргументов."""

    expected_params_args = {
        'report': 'average-rating',
        'files': ['products1.csv', 'products2.csv']
    }

    current_params_args = vars(
        get_parser_args(test_input_data['correct_args_data'])
    )

    assert current_params_args == expected_params_args


def test_get_parser_args_without_report_name():
    """Проверка обработки ввода данных без наименования отчета."""

    with pytest.raises(
        ArgumentError,
        match='Не указано наименование отчета'
    ):
        get_parser_args(
            test_input_data['args_data_without_report_name']
        )


def test_get_parser_args_without_files():
    """Проверка обработки ввода данных без файлов для формирования отчета."""

    with pytest.raises(
        ArgumentError,
        match='Не выбраны файлы для составления отчета'
    ):
        get_parser_args(
            test_input_data['args_data_without_files']
        )


def test_get_parser_args_with_incorrect_type():
    """Проверка обработки ввода некорректных типов данных аргументов."""

    with pytest.raises(TypeError):
        get_parser_args(
            test_input_data['incorrect_type_args']
        )


def test_get_empty_parser_args():
    """Проверка обработки ввода пустых аргументов."""

    with pytest.raises(SystemExit):
        get_parser_args(
            test_input_data['empty_args']
        )


def test_create_report_data():
    """Проверка корректности создания сводного отчета."""

    args = get_parser_args(test_input_data['correct_args_data'])

    expected_report_data = (
        'average-rating',
        [['apple', 4.55], ['samsung', 4.53], ['xiaomi', 4.37]],
        ['brand', 'rating']
    )

    current_report_data = create_report_data(
        args.report,
        args.files,
        dir_path='files'
    )

    assert current_report_data == expected_report_data


def test_get_parser_files_with_nonexistent_position():
    """Проверка обработки файлов с несуществующей позицией отчета."""

    with pytest.raises(KeyError):
        args = get_parser_args(
            test_input_data['nonexistent_parsing_position']
        )
        create_report_data(
            args.report,
            args.files,
            dir_path='files'
        )


def test_parsing_data_with_nonexistent_file():
    """Проверка обработки данных для парсинга с несуществующим файлом."""

    with pytest.raises(FileNotFoundError):
        args = get_parser_args(
            test_input_data['nonexistent_file']
        )
        create_report_data(
            args.report,
            args.files,
            dir_path='files'
        )


def test_print_report_data(capfd: pytest.CaptureFixture[str]):
    """Проверка формата печати таблицы сводного отчета."""

    args = get_parser_args(test_input_data['correct_args_data'])

    report_name, report_data, headers = create_report_data(
        args.report,
        args.files,
        dir_path='files'
    )

    print_report_table(
        report_name,
        report_data,
        headers
    )
    
    out, _ = capfd.readouterr()

    expected_table = '''average-rating
+----+---------+----------+
|    | brand   |   rating |
|----+---------+----------|
|  1 | apple   |     4.55 |
|  2 | samsung |     4.53 |
|  3 | xiaomi  |     4.37 |
+----+---------+----------+
'''

    assert out == expected_table
