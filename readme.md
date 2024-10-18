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


## Prerequisite
1. python3.8+  
2. toolz

## Install 

### func-util is on the Python Package Index (PyPI):
```bash

pip install func-util

```

