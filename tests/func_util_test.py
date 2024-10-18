from collections import namedtuple
from functools import partial
from unittest import TestCase

from func_util.func_util import (
    be_type,
    for_each,
    fuse,
    fuse_if_possible,
    FuseError,
    indices,
    lflatten,
    map_by,
    mode,
)


class FuncUtilTest(TestCase):
    def test_for_each(self):
        def add(to: list[int], num: int):
            to.append(num)

        a = [0]

        nums = []
        for_each(partial(add, a), nums)
        self.assertEqual(a, [0])

        nums = [1, 10, 100]
        for_each(partial(add, a), nums)
        self.assertEqual(a, [0, 1, 10, 100])

        def divide(divided: list, divider: int):
            divided[0] = divided[0] / divider

        a = [100]
        dividers = [2, 0, 2]
        for_each(partial(divide, a), dividers, raise_on_error=False)
        self.assertEqual(a[0], 25)

    def test_map_by(self):
        self.assertListEqual([2, 4, 6], list(map_by(lambda v: v * 2)([1, 2, 3])))

    def test_fuse_in_number_case(self):
        def predicate_func(num0, num1):
            return not (bool(num0 % 2) ^ bool(num1 % 2))

        def fuse_func(num0, num1):
            return num0 * num1

        items0 = [num for num in range(2, 20, 2)]
        result = fuse(predicate_func=predicate_func, fuse_func=fuse_func, items=items0)
        self.assertEqual(1, len(result))
        self.assertEqual(0, result[0] % 2)

        items1 = [num for num in range(1, 20, 2)]
        result = fuse(predicate_func=predicate_func, fuse_func=fuse_func, items=items1)

        self.assertEqual(1, len(result))
        self.assertEqual(1, result[0] % 2)

        result = fuse(predicate_func=predicate_func, fuse_func=fuse_func, items=items1 + items0)
        self.assertEqual(2, len(result))
        self.assertEqual(1, sum([num % 2 for num in result]))

        result = fuse(predicate_func=predicate_func, fuse_func=fuse_func, items=[])
        self.assertListEqual([], result)

    def test_fuse_without_predicate_func(self):
        def fuse_func1(num0, num1):
            if num0 == num1:
                return num0
            return None

        nums = [-1, -1, 0, 0, 0, 0, 5, 5, 6, 7, 3, 99, -101, 0, 0, -1, 6]
        result = fuse_if_possible(fuse_func=fuse_func1, items=nums, allow_none_as_fusion_output=False)
        assert result == [-1, 0, 5, 6, 7, 3, 99, -101]

        def fuse_func2(num0, num1):
            if num0 == num1:
                return None
            raise FuseError

        nums = [-1, -1, 0, 0, 0, 0, 5, 5, 6, 7, 3, 99, -101, 0, 0, -1, 6]
        result = fuse_if_possible(fuse_func=fuse_func2, items=nums, allow_none_as_fusion_output=True)
        self.assertListEqual(result,[None, 7, 3, 99, -101, -1])

    def test_be_type(self):
        type_predicator = be_type(float)
        self.assertTrue(type_predicator(1.1))
        self.assertFalse(type_predicator(1))

    def test_lflatten(self):
        self.assertListEqual([], lflatten([]))

        self.assertListEqual([1], lflatten(1))

        normal_list = [1, 2, 3]
        self.assertListEqual([1, 2, 3], lflatten(normal_list))

        nested_list = [1, [2]]
        self.assertListEqual([1, 2], lflatten(nested_list))

        complex_nested_list = [1, [2], [3, [4], [[5, 6]]]]
        self.assertListEqual([1, 2, 3, 4, 5, 6], lflatten(complex_nested_list))

        test_list = ["[f,s]", 1, [2], [3, [4], 5], []]
        result_list = lflatten(test_list)
        self.assertEqual(["[f,s]", 1, 2, 3, 4, 5], result_list)

        test_list = [[[[[[[[1]]], 2]], 3]], 4]
        result_list = lflatten(test_list)
        self.assertEqual([1, 2, 3, 4], result_list)

        TestTuple = namedtuple("Test", "a b c")
        instance = TestTuple(1, 2, 3)
        test_list = [[instance], [[instance], instance]]
        result_list = lflatten(test_list)
        self.assertListEqual([instance, instance, instance], result_list)

        result = lflatten("123")
        self.assertListEqual(["123"], result)

    def test_mode(self):
        # test mode function for a list of numbers
        # if all numbers are different, return the first number
        num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(1, mode(num_list))

        # if there are two numbers that appear the most, return the first one
        num_list = [1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 10, 10]
        self.assertEqual(5, mode(num_list))

        # if there is one number that appears the most, return it
        num_list = [1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 10, 10, 10]
        self.assertEqual(10, mode(num_list))

    def test_indices(self):
        nums = [1, 2, 3, 4, 5, 6]
        _indices = indices(nums, predicate=lambda n: n % 2 == 1)
        self.assertListEqual([0, 2, 4], _indices)

        _val_indices = indices(nums, predicate=lambda n: n % 2 == 1, with_value=True)
        self.assertListEqual([(0, 1), (2, 3), (4, 5)], _val_indices)

        _indices = indices([0, 1, 0, 2, 0, 3])
        self.assertListEqual([1, 3, 5], _indices)
