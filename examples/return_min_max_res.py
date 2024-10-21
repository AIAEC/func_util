from func_util.func_util import min_max

nums = [1, 2, 3, 4, 5, -6]

min1, max1 = min_max(iter=nums)
# min1: -6    max1: 5

min2, max2 = min_max(iter=nums, key=lambda x: x * x)
# min2: 1     max2: -6