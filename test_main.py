import pytest

from argparse import ArgumentError, Namespace 

from main import (
    get_parser_args,
    create_report_data,
    print_report_table,
    main
)

tests_args_data = {
    'correct_args': [
        '--report', 'average-rating',
        '--files', 'products1.csv', 'products2.csv'
    ],
    'correct_args_without_report_name': [
        '--files', 'products1.csv', 'products2.csv'
    ],
    'correct_args_without_files': [
        '--report', 'average-rating'
    ],
    'empty_args': ['--report', '', '--files', ''],
    'incorrect_name_args': [
        '--report', 'nonexistent_report',
        '--files', 'nonexistent_file.csv'
    ],
    'incorrect_type_args': ['--report', 1, '--files', True],
}


def test_get_parser_args():
    """Проверка корректности параметров и аргументов."""

    expected_namespace = Namespace(
        report='average-rating',
        files=['products1.csv', 'products2.csv']
    )
    current_parser_namespace = get_parser_args(
        tests_args_data['correct_args']
    )

    assert current_parser_namespace == expected_namespace


def test_get_parser_args_without_report_name():
    """Проверка работы программы без указания наименования отчета."""

    with pytest.raises(
        ArgumentError,
        match='Не выбран параметр наименования отчета'
    ):
        get_parser_args(
            tests_args_data['correct_args_without_report_name']
        )


def test_get_parser_args_without_files():
    """Проверка работы программы без указания файлов для парсинга."""

    with pytest.raises(
        ArgumentError,
        match='Не выбран параметр с файлами для составления отчета'
    ):
        get_parser_args(
            tests_args_data['correct_args_without_files']
        )


def test_get_parser_args_with_incorrect_type():
    """Проверка работы программы с некорректными типами данных."""

    with pytest.raises(TypeError):
        get_parser_args(
            tests_args_data['incorrect_type_args']
        )


def test_create_report_data():
    """Проверка создания сводного отчета."""

    args = get_parser_args(tests_args_data['correct_args'])

    test_report_data = (
        'average-rating',
        [['apple', 4.55], ['samsung', 4.53], ['xiaomi', 4.37]],
        ['brand', 'rating']
    )

    assert create_report_data(
        args.report,
        args.files,
        dir_path='files'
    ) == test_report_data
