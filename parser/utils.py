from typing import List, Dict, Union


def convert_value(value: str) -> Union[str, int, float]:
    """Преобразует значение в int или float, если это возможно"""
    try:
        # Пробуем преобразовать к int
        return int(value)
    except ValueError:
        try:
            # Пробуем преобразовать к float
            return float(value)
        except ValueError:
            # Оставляем как строку
            return value


def convert_dict_values(
    data: List[Dict[str, str]],
) -> List[Dict[str, Union[str, int, float]]]:
    """Преобразует в int и float те значения в словаре, которые возможно"""
    return [{key: convert_value(value) for key, value in item.items()} for item in data]
