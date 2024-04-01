from src.dict_tape.exceptions import ArgTypeError, DataTypeError, ResultTypeError


def chain_get[T](
    data: dict | list | str,
    *args: str | int,
    default: T | None = None,
    check_arg_types: bool = True,
    check_data_types: bool = True
) -> T | None:
    """
    Get a deeply nested item from a dict or list without worrying about KeyError/IndexError

    Intended to be a natural extension to .get() for nested data structures

    :param data: the data to search
    :param args: an arg-list of keys/indices to use to traverse the data
    :param default: a default value to return if traversal fails
    :param check_arg_types: set as False to disable type checking on the provided keys
    :param check_data_types: set as False to disable type checking on the data and return type
    :return: The value found after traversal, or the default value
    :raises TypeError: Raised if any of the type checking fails (if enabled)
    :raises ValueError: Raised if no args are provided for traversal
    """
    if not args:
        raise ValueError('At least one arg must be provided')
    try:
        for i, arg in enumerate(args):
            arg_type = type(arg)
            data_type = type(data)
            if data_type not in (dict, list, str):
                raise DataTypeError(
                    f"Invalid data type '{data_type.__name__}' at args[{i}] (must be dict, list, or str)"
                )
            if (data_type in [list, str]) and arg_type != int:
                raise ArgTypeError(
                    f"Invalid key type '{arg_type.__name__}' at args[{i}] (must be int for list or str)"
                )
            elif (data_type == dict) and arg_type not in [str, int]:
                raise ArgTypeError(f"Invalid key type '{arg_type.__name__}' at args[{i}] (must be str for dict)")
            try:
                data = data[arg]
            except TypeError:
                raise ArgTypeError(f"Invalid key type '{arg_type.__name__}' at args[{i}] (must be int for list or str)")
        if default is not None and type(data) != type(default):
            raise ResultTypeError(
                f'Result [{data}] ({type(data).__name__}) does not match type of default [{default}] ({type(default).__name__})'
            )
        return data
    except DataTypeError as dte:
        if check_data_types:
            raise TypeError(str(dte))
        return default
    except ArgTypeError as ate:
        if check_arg_types:
            raise TypeError(str(ate))
        return default
    except ResultTypeError as rte:
        if check_data_types:
            raise TypeError(str(rte))
        return default
    except TypeError:
        if not check_data_types:
            return default
        raise
    except (KeyError, IndexError):
        return default
