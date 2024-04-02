from __future__ import annotations

from functools import reduce, wraps
from itertools import chain, repeat
from typing import Any, Callable, Mapping, MutableMapping, Sequence, TypeVar


K = TypeVar('K')
V = TypeVar('V')


def getitem(obj: Mapping[K, V], key: K) -> V:
    """
    A functional wrapper for item access.
    """
    return obj[key]


def fnone(f: Callable, *defaults: Any) -> Callable:
    """
    Wraps a function f with default arguments.

    When the new function is called, it will look for positional arguments that
    are None and swap in the corresponding default values.

    """

    @wraps(f)
    def g(*args, **kwargs):
        new_args = [
            default if (arg is None) else arg
            for arg, default in zip(args, chain(defaults, repeat(None)))
        ]

        return f(*new_args, **kwargs)

    return g


def update_in(d: MutableMapping, keys: Sequence, f: Callable, *args: Any) -> bool:
    """
    Transforms a value (in place) in a nested data structure.

    d: A dict or similar.
    keys: A list of keys to lookup to find the item in question.
    f: A function to apply to the value found.

    If the final key in the sequence is not found, the first argument to `f`
    will be `None`.

    Returns True iff the keypath exists and we applied the function.

    """

    try:
        if len(keys) > 1:
            parent = reduce(getitem, keys[:-1], d)
        elif len(keys) > 0:
            parent = d
        else:
            raise ValueError("keys must not be empty.")
    except KeyError:
        return False
    else:
        key = keys[-1]
        orig = parent.get(key, None)
        parent[key] = f(orig, *args)

        return True
