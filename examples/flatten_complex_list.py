from func_util.func_util import lflatten

complex_list = [[1, 2, 3, [4, [5]]], [[[[[6]]]]], [7]]
flatten_res = lflatten(complex_list)

# flatten_res [1,2,3,4,5,6,7]

