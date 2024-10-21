from func_util.func_util import separate

nums = [1, 2, 3, 4, 5, 6]

even, odd = separate(func=lambda x: x % 2 == 0, items=nums)

# even: [2, 4, 6]    odd:[1, 3, 5]