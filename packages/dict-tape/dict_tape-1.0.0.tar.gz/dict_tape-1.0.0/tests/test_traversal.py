import pytest

from src.dict_tape import chain_get


@pytest.fixture
def nested_list_and_str():
    return {'level_1': {'level_2': [{'level_3': 'final_val'}]}}


@pytest.fixture
def nested_list_and_int():
    return {'level_1': {'level_2': [{'level_3': 10}]}}


def test_chain_get_basic(nested_list_and_str):
    result = chain_get(nested_list_and_str, 'level_1', 'level_2', 0, 'level_3', default='some_default')
    assert result == 'final_val'


def test_chain_get_basic_int(nested_list_and_int):
    result = chain_get(nested_list_and_int, 'level_1', 'level_2', 0, 'level_3', default=0)
    assert result == 10


def test_chain_get_bad_key(nested_list_and_str):
    result = chain_get(nested_list_and_str, 'level_1', 'level_2', 0, 'bad_key', default='some_default')
    assert result == 'some_default'


def test_chain_get_bad_key_int(nested_list_and_int):
    result = chain_get(nested_list_and_int, 'level_1', 'level_2', 0, 'bad_key', default=0)
    assert result == 0


def test_chain_get_bad_key_no_default(nested_list_and_str):
    result = chain_get(nested_list_and_str, 'level_1', 'level_2', 0, 'bad_key')
    assert result is None


def test_chain_get_no_args(nested_list_and_str):
    with pytest.raises(ValueError):
        chain_get(nested_list_and_str)


def test_chain_get_bad_arg_type(nested_list_and_str):
    with pytest.raises(TypeError):
        chain_get(nested_list_and_str, 'level_1', 'level_2', 'bad', 'level_3')


def test_chain_get_bad_data_type(nested_list_and_int):
    with pytest.raises(TypeError):
        chain_get(nested_list_and_int, 'level_1', 'level_2', 0, 'level_3', 'bad')


def test_chain_get_bad_default_type(nested_list_and_int):
    with pytest.raises(TypeError):
        chain_get(nested_list_and_int, 'level_1', 'level_2', 0, 'level_3', default='bad')


def test_chain_get_bad_arg_type_no_type_check(nested_list_and_str):
    result = chain_get(
        nested_list_and_str,
        'level_1', 'level_2',
        0, 'level_3', 'bad_key',
        default=0,
        check_arg_types=False
    )
    assert result == 0


def test_chain_get_bad_data_type_no_type_check(nested_list_and_int):
    result = chain_get(
        0,
        'level_1',
        default=0,
        check_data_types=False
    )
    assert result == 0


def test_chain_get_bad_default_type_no_type_check(nested_list_and_int):
    result = chain_get(
        nested_list_and_int,
        'level_1', 'level_2',
        0, 'level_3',
        default='some_default',
        check_data_types=False
    )
    assert result == 'some_default'
