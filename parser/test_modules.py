import pytest
from .executors import (
    check_and_split_filter,
    execute_where,
    check_and_split_aggregate,
    execute_aggregate,
    find_executor,
)
from .utils import convert_value, convert_dict_values


# Тесты utils
@pytest.mark.parametrize("input_val, expected", [
    ("42", 42),
    ("3.14", 3.14),
    ("hello", "hello"),
])
def test_convert_value(input_val, expected):
    assert convert_value(input_val) == expected


def test_convert_dict_values():
    input_data = [{"a": "1", "b": "2.5", "c": "text"}]
    expected_output = [{"a": 1, "b": 2.5, "c": "text"}]
    assert convert_dict_values(input_data) == expected_output


# Тесты executors

@pytest.mark.parametrize("input_val, expected", [
    ("price>100", ("price", 100, ">")),
    ("age=30", ("age", 30, "=")),
    ("rate<4.5", ("rate", 4.5, "<")),
])
def test_check_and_split_filter_valid(input_val, expected):
    assert check_and_split_filter(input_val) == expected


@pytest.mark.parametrize("input_val", [
    "invalidstring",
    "field>>100",
    "=100",
    "field=",
])
def test_check_and_split_filter_invalid(input_val):
    with pytest.raises(Exception):
        check_and_split_filter(input_val)


def test_execute_where_equal():
    data = [{"price": 100}, {"price": 200}]
    result = execute_where(data, "price=100", ["price"])
    assert result == [{"price": 100}]


def test_execute_where_greater():
    data = [{"age": 18}, {"age": 25}, {"age": 30}]
    result = execute_where(data, "age>20", ["age"])
    assert result == [{"age": 25}, {"age": 30}]


def test_execute_where_less():
    data = [{"rate": 4.0}, {"rate": 3.5}]
    result = execute_where(data, "rate<4.0", ["rate"])
    assert result == [{"rate": 3.5}]


def test_execute_where_invalid_column():
    with pytest.raises(Exception):
        execute_where([{"a": 1}], "b=1", ["a"])


@pytest.mark.parametrize("input_val, expected", [
    ("score=max", ("score", "max")),
    ("price=avg", ("price", "avg")),
])
def test_check_and_split_aggregate_valid(input_val, expected):
    assert check_and_split_aggregate(input_val) == expected


@pytest.mark.parametrize("input_val", [
    "invalidaggregate",
    "=max",
    "value=",
])
def test_check_and_split_aggregate_invalid(input_val):
    with pytest.raises(Exception):
        check_and_split_aggregate(input_val)


def test_execute_aggregate_min():
    data = [{"score": 5}, {"score": 2}, {"score": 8}]
    result = execute_aggregate(data, "score=min", ["score"])
    assert result == [{"min": 2}]


def test_execute_aggregate_max():
    data = [{"score": 5}, {"score": 2}, {"score": 8}]
    result = execute_aggregate(data, "score=max", ["score"])
    assert result == [{"max": 8}]


def test_execute_aggregate_avg():
    data = [{"score": 5}, {"score": 15}]
    result = execute_aggregate(data, "score=avg", ["score"])
    assert result == [{"avg": 10.0}]


def test_execute_aggregate_invalid_column():
    with pytest.raises(Exception):
        execute_aggregate([{"a": 1}], "b=max", ["a"])


def test_execute_aggregate_invalid_func():
    with pytest.raises(Exception):
        execute_aggregate([{"a": 1}], "a=sum", ["a"])


@pytest.mark.parametrize("command, expected", [
    ("where", execute_where),
    ("aggregate", execute_aggregate),
])
def test_find_executor_valid(command, expected):
    assert find_executor(command) is expected


def test_find_executor_invalid():
    with pytest.raises(Exception):
        find_executor("nonexistent")