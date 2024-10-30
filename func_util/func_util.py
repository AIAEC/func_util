"""
supporting some extra utility functions under python.
"""

from functools import partial
from itertools import filterfalse, chain

from toolz import concat

from func_util.ordered_set import OrderedSet
from func_util.predicate import is_namedtuple, is_sequence

from collections import defaultdict
from copy import deepcopy
from numbers import Number
from operator import attrgetter
from typing import Any, Callable, Dict, Iterable, List, Literal, Optional, Sequence, Tuple, Union


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


def separate(func: Callable[[Any], bool], items: Iterable[Any]) -> Tuple[List[Any], List[Any]]:
    """
    separate items into two list using given func, with all items of first list returning True, and all items of second
    list returning False

    :param func: callable
    :param items: iterable of items
    :return: (List[Any], List[Any])
    """
    positive_items, negative_items = [], []
    for item in items:
        if func(item):
            positive_items.append(item)
        else:
            negative_items.append(item)
    return positive_items, negative_items


def group(
        grouping_func: Callable[[Any, Any], bool],
        items: List[Any], strict_mode: bool = False,
        commutative: Literal['and', 'or', 'none'] = 'or'
) -> List[List[Any]]:
    """
    clusters items that satisfies the condition into the same group and returns all groups

    :param grouping_func: input item0, item1, return bool.   if item0 and item1 in same group, return True, else return False
    :param items: list, set, tuple and other iterable container
    :param strict_mode: if strict_mode is true, any a pair of items in same group should satisfy the condition.
                        if strict_mode is false, any item in a group need at least one another item to satisfy the condition.

    :param commutative: grouping_func(A,B) and/or grouping_func(B,A) as the condition of group条件,
                        if it is none, grouping_func(A,B) as the condition

    :return: [[items of group0], [items of group1], ...]   return a list of groups, any group is a list of items
    notice: if item can not find another item to satisfy the condition, use a group to store it separately.
    """

    def can_group(A, B):
        if commutative == 'and':
            return grouping_func(A, B) and grouping_func(B, A)
        elif commutative == 'or':
            return grouping_func(A, B) or grouping_func(B, A)
        else:
            return grouping_func(A, B)

    def group_helper(items: List[Any]) -> List[List[Any]]:
        result: List[List[Any]] = []

        ungrouped_indices: OrderedSet = OrderedSet(range(len(items)))
        while len(ungrouped_indices) > 0:
            cur_idx = ungrouped_indices.pop()
            cur_group: List[Any] = []
            group_candidate = OrderedSet([cur_idx])

            while len(group_candidate) > 0:
                cand_idx = group_candidate.pop()
                cur_group.append(items[cand_idx])

                idx_nearby_cands: OrderedSet = OrderedSet()
                for ungrouped_idx in ungrouped_indices:
                    if can_group(items[ungrouped_idx], items[cand_idx]):
                        idx_nearby_cands.add(ungrouped_idx)

                ungrouped_indices.difference_update(idx_nearby_cands)  # type: ignore
                group_candidate.update(idx_nearby_cands)  # type: ignore

            result.append(cur_group)
        return result

    def strict_group_helper(items: List[Any]) -> List[List[Any]]:
        result: List[List[Any]] = []
        for item in items:
            for cur_group in result:
                if all(can_group(item, cur_item) for cur_item in cur_group):
                    cur_group.append(item)
                    break
            else:  # non cur_group satisfy if check
                result.append([item])
        return result

    return strict_group_helper(items) if strict_mode else group_helper(items)


def lfilter(func: Callable, iter: Iterable) -> List[Any]:
    """
    shortcut for list(filter(func, iter))

    :param func: callable object
    :param iter:

    :return: list of filter(func, iter)
    """
    return list(filter(func, iter))


def lmap(func: Callable, *iter: Iterable) -> List[Any]:
    """
    shortcut for list(map(func, iter))

    :param func: callable object
    :param iter:

    :return: list of map(func, iter)
    """
    return list(map(func, *iter))


def lconcat(iter: Iterable) -> List[Any]:
    """
    shortcut for list(chain.from_iterable(iter))

    :param iter: iterable

    :return: list of flatten objects
    """
    return list(chain.from_iterable(iter))


def min_max(iter: Iterable, key: Callable[[Any], Union[int, float, tuple]] = None, copied: bool = True):
    """
    return  min and max in the items

    :param iter: iterable container
    :param key: None or lambda,  if it is None, use itself as value to compare, else use the returning of key as value to compare
    :param copied: if True, deep copy a backup as result , else return themselves as result

    :return: tuple of 2 items, (min_item, max_item)
    """
    key = key or (lambda v: v)
    min_v, max_v = float("inf"), float("-inf")
    min_item, max_item = None, None
    for item in iter:
        item_v = key(item)
        if item_v < min_v:
            min_item = item
            min_v = item_v

        if item_v > max_v:
            max_item = item
            max_v = item_v

    if copied:
        min_item = deepcopy(min_item)
        max_item = deepcopy(max_item)

    return [min_item, max_item]


def group_by(key: Callable[[object], object], seq: Sequence[object]) -> Dict[object, List[object]]:
    """
    group the item of the given sequence by return of key function

    :param key: callable, given single object, returns hashable object
    :param seq: sequence of objects

    :return: Dict[object, List[object]], with key being the mapped value, value to be the list of objects
    """
    if not callable(key):
        key = attrgetter(key)
    d = defaultdict(lambda: [].append)
    for item in seq:
        d[key(item)](item)
    rv = {}
    for k, v in d.items():
        rv[k] = v.__self__
    return rv


def sign(expr: Any, reverse: bool = False) -> int:
    """
    shortcut for (expr ? 1 : -1)

    :param expr: expression
    :param reverse: whether do (expr ? -1: 1) instead
    :return: 1 or -1
    """
    return 1 if expr ^ reverse else -1


def argmin(seq: Sequence, key: Optional[Callable[[Any], Number]] = None) -> Optional[int]:
    """
    return the index of min
    :param seq:
    :param key:
    :return:
    """
    if not seq:
        return None

    default_key = lambda x: x
    key = key or default_key
    min_idx = None
    min_val = None

    for i, item in enumerate(seq):
        val = key(item)
        if min_val is None or val < min_val:
            min_val = val
            min_idx = i

    return min_idx


def argmax(seq: Sequence, key: Optional[Callable[[Any], Number]] = None) -> Optional[int]:
    """
    return the index of max
    :param seq:
    :param key:
    :return:
    """
    return argmin(seq, lambda x: -key(x) if key else -x)
