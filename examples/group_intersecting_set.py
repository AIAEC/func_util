from examples.fuse_intersecting_set import is_intersecting
from func_util.func_util import group

items = [{1, 2}, {2, 6}, {1, 3}, {1, 4}, {8, 9}]

group_res = group(grouping_func=is_intersecting, items=items)

# group_res  [[{1, 4}, {1, 3}, {1, 2}, {2,6}]  , [{8, 9}] ]