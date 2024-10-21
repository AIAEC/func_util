# func_util
supporting some extra utility functions under python. 

# Example

### lflatten:  Flatten sequence into a list
```bash
>>> from func_util.func_util import lflatten
>>> words = ["how", ["do", ["you" , "do"] ] ] 
>>> words = lflatten(words)
>>> print(words)
["how", "do", "you", "do"]
```

### fuse:  fuse intersecting sets
```bash
>>> from func_util.func_util import fuse
>>> items = [{1, 2, 3}, {2, 5, 6}, {1}, {4, 5, 6}]
>>> fuse_res = fuse(predicate_func=lambda s1, s2: s1.isdisjoint(s2), fuse_func=lambda s1, s2: s1.union(s2), items=items)
>>> print(fuse_res)
[{1, 2, 3, 4, 5, 6}]
```

### group:  group intersecting sets
```bash
>>> from func_util.func_util import group
>>> items = [{1, 2}, {2, 6}, {1, 3}, {1, 4}, {8, 9}]
>>> group_res = group(grouping_func=lambda s1, s2: s1.isdisjoint(s2), items=items)
>>> print(group_res)
[ [{1, 4}, {1, 3}, {1, 2}, {2, 6}], [{8, 9}] ]
```

## Prerequisite
1. python3.8+  
2. toolz


## Install
### func-util is on the Python Package Index (PyPI):
```bash

pip install func-util

```

