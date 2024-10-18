def is_intersecting(set_a: set, set_b: set) -> bool:
    """
    judge whether set_a intersects set_b
    """
    return not set_a.isdisjoint(set_b)


def union_set(set_a: set, set_b: set) -> set:
    return set_a.union(set_b)


from func_util.func_util import fuse

items = [{1, 2, 3}, {2, 5, 6}, {1}, {4, 5, 6}]

fuse_res = fuse(predicate_func=is_intersecting, fuse_func=union_set, items=items)

# fuse_res  [{1, 2, 3, 4, 5, 6}]
