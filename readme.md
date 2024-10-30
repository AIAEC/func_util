# func_util
is another functional programming toolkit in python to make your life easier. 
It's strongly inspired by packages like
[toolz](https://github.com/pytoolz/toolz), [pyfunctional](https://github.com/EntilZha/PyFunctional).
Instead of rewriting the same functionality in different API style, we glean the small glittering trinket(also battle field tested) into
this package every now and then from our daily work in algorithm of [intelligent basement designing system](https://www.basementplayer.com), 
which is fairly compatible with other functional packages.

You might want to have a look at this package if you're:
* heavy FP programmer, who occasionally build your own FP libraries
* fan of toolz, pyfunctional or lodash(js)
* tired of importing gigantic numpy or scipy for only small fraction of usage, like argmin, argmax

# Example

### lflatten:  Flatten nested list into a flat list
```bash
>>> from func_util.func_util import lflatten
>>> words = ["how", ["do", ["you" , "do"] ] ] 
>>> words = lflatten(words)
>>> print(words)
["how", "do", "you", "do"]
```

### fuse:  fuse list of items into a new list according to predicate function
When you have a list of items, a new fused item could be created by fusing 2 items according to given fuse_func, which 
in turn could possibly be fused into another new item and in the very end, we could get a new list of fused items.

```bash
>>> from func_util.func_util import fuse
>>> items = [{1, 2, 3}, {2, 5, 6}, {1}, {4, 5, 6}]
>>> fuse_res = fuse(predicate_func=lambda s1, s2: s1.isdisjoint(s2), fuse_func=lambda s1, s2: s1.union(s2), items=items)
>>> print(fuse_res)
[{1, 2, 3, 4, 5, 6}]
```

### group:  cluster items into groups according to grouping_func
It works most likely to clustering from machine learning, except it takes a list of items as parameter.
```bash
>>> from func_util.func_util import group
>>> items = [{1, 2}, {2, 6}, {1, 3}, {1, 4}, {8, 9}]
>>> group_res = group(grouping_func=lambda s1, s2: s1.isdisjoint(s2), items=items)
>>> print(group_res)
[ [{1, 4}, {1, 3}, {1, 2}, {2, 6}], [{8, 9}] ]
```

### map_by:  compose a map function and pass it everywhere
```bash
>>> from func_util.func_util import map_by
>>> plus_one = map_by(lambda x: x + 1)
>>> times_two = map_by(lambda x: x * 2)
>>> items = [1, 2, 3]
>>> plus_one(times_two(items))
[3, 5, 7]
```

### be_type:  simply tool of type predication
```bash
>>> items = [1, 2, 3.5]
>>> integers = list(filter(be_type(int), items))
```

### separate:   separate items into two opposite lists according to func
```bash
>>> nums = [1, 2, 3, 4, 5, 6]
>>> even, odd = separate(func=lambda x: x % 2 == 0, items=nums)
even: [2, 4, 6]    odd: [1, 3, 5]
```

### min_max:    return min_item and max_item from items, and key_fun maps item to numeric for comparing
```bash

#pseudo-code

cycle = Cycle(radius=5)
rectangle = Rectangle(width=2, height=5)
square = Square(side_length=2)
key_func: a function calculate the area of shape 
min, max = min_max(iter=[cycle, rectangle, square], key=key_func)
# min: square         max: cycle
```


### group_by:   group items by key which is a mapping function that maps object to a hashable object.   returning is a dict, key is mapping object, value is items.

```bash

#pseudo-code

items = [cycle, rectangle, bus, subway]
key_fun: a function maps item to the string for the classifacation
res = group_by(key=key_fun, seq=items)

# res:   {"shape": [cycle, rectangle],  "transportation": [bus, subway]}
```

### sign:  arithmetic tool for boolean
```bash
>>> working_hours = 6
>>> income = 10
>>> extra = 2
>>> total = income + extra * sign(working_hours >= 8)
8
```

### OrderedSet
Missing from native collection package, we make OrderedSet based on OrderedDict and give it a `set` alike api.

## Prerequisite
1. python3.8+  
2. toolz


## Install
### func-util is on the Python Package Index (PyPI):
```bash

pip install func-util

```

