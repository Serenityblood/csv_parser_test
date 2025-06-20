from typing import List, Dict, Tuple, Union, Callable

from .utils import convert_value


def check_and_split_filter(value: str) -> Tuple[str, Union[str, int, float], str]:
    """Проверяет возможность разделить значение по принципу 'field(operand)value'.
    Доступны три оператора: '<, >, ='.
    При возможности возвращает кортеж (field, value, operand)"""
    splitter = ""
    if "=" in value:
        splitter = "="
    elif "<" in value:
        splitter = "<"
    elif ">" in value:
        splitter = ">"
    if not splitter:
        raise Exception("Нет допустимого знака '>, <, ='")
    splitted_value = value.split(splitter)
    if len(splitted_value) != 2:
        raise Exception(f"Неправильно задан параметр {value}.")
    field = splitted_value[0]
    field_value = splitted_value[1]
    if not field or not field_value:
        raise Exception(
            f"Одно из значений пусто. Скорее всего '=value' или 'field=' было использовано где-то. Исходное значение: {value}"
        )
    return field, convert_value(field_value), splitter


def execute_where(data: List[Dict], value: str, columns: List[str]):
    """Выполняет фильтрацию"""
    field, value, operand = check_and_split_filter(value)
    if field not in columns:
        raise Exception(f"Поля {field} нет в данных. Доступны: {columns}")
    if operand == "=":
        return [row for row in data if row[field] == value]
    elif operand == ">":
        return [row for row in data if row[field] > value]
    else:
        return [row for row in data if row[field] < value]


def check_and_split_aggregate(value: str) -> Tuple[str, str]:
    """Проверяет возможность разделить значение по принципу 'field=aggr_func'.
    При возможности возвращает кортеж (field, aggr_func)"""
    if "=" not in value:
        raise Exception("Нет разделителя '='")
    splitted_value = value.split("=")
    if len(splitted_value) != 2:
        raise Exception(f"Неправильно задан параметр {value}.")
    field = splitted_value[0]
    aggr_func = splitted_value[1]
    if not field or not aggr_func:
        raise Exception(
            f"Одно из значений пусто. Скорее всего '=aggr_func' или 'field=' было использовано где-то. Исходное значение: {value}"
        )
    return field, aggr_func


def aggr_min(data: List[Dict], field: str):
    min_val = None
    for row in data:
        if not min_val:
            min_val = row[field]
        else:
            min_val = row[field] if row[field] < min_val else min_val
    return [{"min": min_val}]


def aggr_max(data: List[Dict], field: str):
    max_val = None
    for row in data:
        if not max_val:
            max_val = row[field]
        else:
            max_val = row[field] if row[field] > max_val else max_val
    return [{"max": max_val}]


def aggr_avg(data: List[Dict], field: str):
    avg = sum([row[field] for row in data]) / len(data)
    return [{"avg": avg}]


aggr_funcs = {
    "min": aggr_min,
    "max": aggr_max,
    "avg": aggr_avg,
}


def execute_aggregate(data: List[Dict], value: str, columns: List[str]):
    """Выполняет аггрегацию"""
    field, aggr_func = check_and_split_aggregate(value)
    if field not in columns:
        raise Exception(f"Поля {field} нет в данных. Доступны: {columns}")
    aggr_func = aggr_funcs.get(aggr_func)
    if not aggr_func:
        raise Exception(
            f"Не была предоставлена допустимая команда для аггрегации. Доступны: {aggr_funcs.keys()}"
        )
    return aggr_func(data, field)


def find_executor(command_name: str) -> Callable:
    """Возвращает нужную для команды функцию"""
    if command_name == "where":
        return execute_where
    if command_name == "aggregate":
        return execute_aggregate
    raise Exception(f"Команды {command_name} нет в списке доступных")
