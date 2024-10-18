"""
supporting some extra utility functions under python.
"""

from functools import partial
from itertools import filterfalse
from typing import Any, Callable, Iterable, Sequence

from toolz import concat

from func_util.predicate import is_namedtuple, is_sequence


class FuseError(Exception):
    """
    when failed in fuse_func and without predicate func, raise this exception

    """


def base_fuse(
        predicate_func: Callable[[Any, Any], bool] | None,
        fuse_func: Callable[[Any, Any], Any],
        items: Iterable[Any],
        allow_none_as_fusion_output: bool = False,
) -> list[Any]:
    """

    fuse items into a new item when they satisfy predicate_fun until there is no a pair of items can satisfy.

    fuse_func should make sure items can be fused  when predicate_func return true.

    try to fuse each other when predicate_func is not given:
        1. if allow_none_as_fusion_output is false, None is invalid result in fusing function.
        2. if allow_none_as_fusion_output is True, None is valid result in fusing function.

    :param predicate_func: judge whether items can be fused
    :param fuse_func: calculate the result of fusing items
    :param items:
    :param allow_none_as_fusion_output: allow None as valid output
    :return: list of fused items
    """
    fusing_candidates = items

    fusing_finished: bool = False
    while not fusing_finished:
        fusion_items = []

        for i, fusing_cand in enumerate(fusing_candidates):
            for j, fusion_item in enumerate(fusion_items):
                if predicate_func is None:
                    try:
                        fusion = fuse_func(fusing_cand, fusion_item)
                        if fusion is None and not allow_none_as_fusion_output:
                            raise FuseError
                    except FuseError:
                        continue
                    else:
                        fusion_items[j] = fusion
                        break
                else:
                    if predicate_func(fusing_cand, fusion_item):
                        fusion_items[j] = fuse_func(fusing_cand, fusion_item)
                        break
            else:  # left_item cannot be converged into any converged_item
                fusion_items.append(fusing_cand)

        fusing_finished = len(fusion_items) == len(fusing_candidates)
        fusing_candidates = fusion_items

    return fusion_items


def fuse(
        predicate_func: Callable[[Any, Any], bool] | None, fuse_func: Callable[[Any, Any], Any], items: Iterable[Any]
) -> list[Any]:
    """
    fuse items into a new item when they satisfy predicate_fun until there is no a pair of items can satisfy.

    :param predicate_func: judge whether items can be fused
    :param fuse_func: calculate the result of fusing items
    :param items:
    :return:
    """
    return base_fuse(predicate_func=predicate_func, fuse_func=fuse_func, items=items)


def fuse_if_possible(
        fuse_func: Callable[[Any, Any], Any | None], items: Iterable[Any], allow_none_as_fusion_output: bool = False
) -> list[Any]:
    """
     try to fuse each other without predicate_func:
        1. if allow_none_as_fusion_output is false, None is invalid result in fusing function.
        2. if allow_none_as_fusion_output is True, None is valid result in fusing function.

    :param fuse_func:
    :param items:
    :param allow_none_as_fusion_output:
    :return:
    """
    return base_fuse(
        predicate_func=None, fuse_func=fuse_func, items=items, allow_none_as_fusion_output=allow_none_as_fusion_output
    )


def lflatten(iter: Sequence[Any], flatten_named_tuple: bool = False) -> list[Any]:
    """
    flatten sequence into a list
    :param iter:
    :param flatten_named_tuple:
    :return:
    """

    if not flatten_named_tuple and is_namedtuple(iter):
        return [iter]

    if not is_sequence(iter):
        return [iter]

    return list(concat(lflatten(item) for item in iter))


def lfilter_out(func: Callable, iter: Iterable) -> list[Any]:
    """
    filter out those items of iter object which func(item) is True, and compose remained items into a list.
    :param func:
    :param iter:
    :return: list of filterfalse(func, iter)
    """
    return list(filterfalse(func, iter))


def for_each(func: Callable, iterable: Iterable, raise_on_error: bool = True) -> None:
    """
    calling the function iteratively on all of elements
    :param func:
    :param iterable:
    :param raise_on_error: ignore error and continue run when raise_on_error is false
    :return: None
    """
    for element in iterable:
        try:
            func(element)
        except Exception:
            if raise_on_error:
                raise Exception
            continue


def map_by(func: Callable) -> Callable[[Iterable[Any]], Iterable[Any]]:
    """
    return a partial function of map

    :param func:
    :return:
    """
    return partial(map, func)


def be_type(type_or_type_tuple: type | tuple[type]) -> Callable[[Any], bool]:
    """
    return a function used to judge the type is specified type or not

    equal to lambda item: isinstance(item, type_or_type_tuple)
    :param type_or_type_tuple:  specified type or types tuple
    :return:
    """

    def predicator(item):
        return isinstance(item, type_or_type_tuple)

    return predicator


def mode(iter: Iterable) -> Any:
    """
    calculate mode in iterable object
    :param iter:
    :return:
    """
    _list = list(iter)
    return max(set(_list), key=_list.count)


def indices(
        iter: Iterable, predicate: Callable[[object], bool] = bool, with_value: bool = False
) -> list[int | tuple[int, object]]:
    """
    return the index of item that predicate is true in the iterable object
    :param iter:
    :param predicate:
    :param with_value: return with value of item, like  [ (idx1, value1), (idx2, value2) ..]
    :return:
    """
    map_func = lambda idx, val: idx
    if with_value:
        map_func = lambda idx, val: (idx, val)

    return [map_func(i, val) for i, val in enumerate(iter) if predicate(val)]
