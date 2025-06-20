import argparse
import csv

from tabulate import tabulate

from parser.executors import find_executor
from parser.utils import convert_dict_values


def main():
    parser = argparse.ArgumentParser(
        description="Парсер csv с возможностями фильтрации и аггрегации через команды --where и --aggregate"
    )
    parser.add_argument("input_file", type=str, help="Название входного файла, должен лежать в основной директории")
    parser.add_argument(
        "--where", "-w", type=str, help="field(operand)value - Общий вид значения. Доуступные операторы: '<, >, ='"
    )
    parser.add_argument("--aggregate", "-a", type=str, help="field=aggr_func - общий вид значения")

    args = parser.parse_args()

    # Использование vars для получения всех аргументов в виде словаря
    args_dict = vars(args)

    # Создание списка кортежей с названием аргумента и его значением
    args_list = [
        (key, value)
        for key, value in args_dict.items()
        if key != "input_file" and value is not None
    ]
    # Получем данные из файла
    with open(args.input_file, mode="r", encoding="utf-8") as file:
        # Создание объекта DictReader
        csv_reader = csv.DictReader(file)
        columns = csv_reader.fieldnames
        data = [row for row in csv_reader]
        if not data:
            return print([])
        data = convert_dict_values(data)

    # Через фабрику получаем нужную функцию
    for command, value in args_list:
        executor = find_executor(command)
        data = executor(data, value, columns)
        if not data:
            return print([])
    print(tabulate(data, headers="keys", tablefmt="grid"))


if __name__ == "__main__":
    main()
