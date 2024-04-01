# dict-tape

_A collection of Python utilities for manipulating dictionaries_

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/O5O7V0GB2)

## Installation

```bash
pip install dict-tape
```

## Usage

```python
from dict_tape import chain_get
```

## Features

### Traversal

#### `chain_get`

This is intended to help solve problems like this with deeply nested dictionaries:

```python
some_dict.get('a', {})[0].get('b', {}).get('e', 'default')
```

The problem is that while `.get()` can help with chains of dictionaries, if you have lists
intermixed in there, you can't sanely default things and have to just hope the list has items
(since list indexing will throw an exception if the list is empty).

But with `chain_get()` you can accomplish this in a way that will sanely default:

```python
from dict_tape import chain_get

some_dict = {'a': [{'b': {'e': 'value'}}]}
# Prints 'value'
print(chain_get(some_dict, 'a', 0, 'b', 'e', default='default'))

some_dict = {'a': []}
# Prints 'default'
print(chain_get(some_dict, 'a', 0, 'b', 'e', default='default'))
```

`chain_get()` will also do some sanity checking on your types and arguments:

- Checks to make sure that every new level is a `dict`, `list`, or `str`
- If the current data being indexed is a `list` or `str`, it will check that the arg provided is an `int`
- If the current data being indexed is a `dict`, it will check that the arg provided is an `int` or `str`
- If the resulting data it finds with traversal doesn't match the type provided for `default`, it will throw an error so you know you got something you apparently didn't expect

**Options**

- `default`:  The default value to return if the chain fails at any point.
- `check_arg_types`:  You can set this to `False` to disable checking whether arg types are valid for data.  If this is disabled, when it would normally throw an error for this problem it will instead return the `default` value.
- `check_data_types`:  You can set this to `False` to disable checking whether the data types are valid.  If this is disabled, when it would normally throw an error for this problem it will instead return the `default` value.
