import argparse
import csv

from tabulate import tabulate


FILES_DIR = 'test_files'


def get_parser_args(parser):

    parser.add_argument(
        '--files',
        nargs="+",
        help='Выберите файлы'
    )
    parser.add_argument(
        '--report',
        default='average-rating',
        type=str,
        help='Наименование отчета'
    )

    files_data = parser.parse_args().files
    report_name = parser.parse_args().report

    return files_data, report_name


def get_report_data(files_data: list, files_dir: str) -> dict:

    elem_report = {}

    for elem in files_data:

        with open(f'./{files_dir}/{elem}', mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                elem_report.setdefault(row['brand'], []).append(float(row['rating']))

    report_data = [[key, round(sum(values_list) / len(values_list), 2)] for key, values_list in elem_report.items()]
    report_data.sort(key=lambda i: i[1], reverse=True)

    return report_data


def print_report_table(report_name: str, report_data: dict):
    
    table = tabulate(
        report_data,
        headers = ['brand', 'rating'],
        tablefmt='outline',
        showindex='always'
    )

    print(report_name, table, sep='\n')


def main():

    parser = argparse.ArgumentParser(description="Average Rating")

    files_data, report_name = get_parser_args(parser)
    report_data = get_report_data(files_data, FILES_DIR)
    report_table = print_report_table(report_name, report_data)

    return report_table


if __name__ == '__main__':
    main()
