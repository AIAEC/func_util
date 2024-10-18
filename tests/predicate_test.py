from collections import namedtuple, deque, UserList
from unittest import TestCase

from func_util.predicate import is_namedtuple, is_sequence


class FuncUtilTest(TestCase):
    def test_is_named_tuple(self):
        NumClass = namedtuple("NumClass", "a b")
        instance = NumClass(1, 2)
        self.assertTrue(is_namedtuple(instance))
        self.assertFalse(is_namedtuple([]))
        self.assertFalse(is_namedtuple((1, 2)))
        self.assertFalse(is_namedtuple({}))
        self.assertFalse(is_namedtuple(set()))
        self.assertFalse(is_namedtuple(""))
        self.assertFalse(is_namedtuple(b""))

        class NumClassMimic:
            def __init__(self, a, b):
                self.a = a
                self.b = b

        self.assertFalse(is_namedtuple(NumClassMimic(1, 2)))


    def test_is_sequence(self):
        self.assertTrue(is_sequence([]))
        self.assertTrue(is_sequence([1]))
        self.assertTrue(is_sequence((1,)))
        self.assertTrue(is_sequence(deque([1])))
        self.assertTrue(is_sequence(UserList()))
        self.assertFalse(is_sequence({1: 1}))
        self.assertFalse(
            is_sequence(
                {
                    1,
                }
            )
        )
        self.assertFalse(is_sequence(1))
        self.assertFalse(is_sequence("123"))

        self.assertTrue(is_sequence("123", exclude_str_and_bytes=False))
        self.assertFalse(is_sequence("123", exclude_str_and_bytes=True))
        self.assertTrue(is_sequence(b"123", exclude_str_and_bytes=False))
        self.assertFalse(is_sequence(b"123", exclude_str_and_bytes=True))

        class Mimic:
            def __iter__(self):
                return iter([1, 2, 3])

            def __getitem__(self, item):
                return 1

            def __setitem__(self, key, value):
                pass

        self.assertFalse(is_sequence(Mimic()))