from copy import deepcopy
from operator import add
from unittest import TestCase

from fabsync.functools import fnone, update_in


class FNoneTestCase(TestCase):
    def test_noop(self):
        f = fnone(self._args)

        args = f(None, 1)

        self.assertEqual(args, (None, 1))

    def test_default(self):
        f = fnone(self._args, 0)

        args = f(None, 1)

        self.assertEqual(args, (0, 1))

    def test_missing_default(self):
        f = fnone(self._args, 0)

        args = f(None, None)

        self.assertEqual(args, (0, None))

    def test_extra_default(self):
        f = fnone(self._args, 0, 1, 2)

        args = f(None, 1)

        self.assertEqual(args, (0, 1))

    def _args(self, *args):
        return args


class UpdateInTestCase(TestCase):
    def test_no_keys(self):
        d = {}

        with self.assertRaises(ValueError):
            update_in(d, (), add, 1)

    def test_missing_path(self):
        d = {'a': {'b': {'c': 1, 'd': 1}}}
        expected = deepcopy(d)

        ok = update_in(d, ('x', 'y', 'z'), fnone(add, 0), 1)

        self.assertFalse(ok)
        self.assertEqual(d, expected)

    def test_shallow(self):
        d = {'a': 1}

        ok = update_in(d, ('a',), add, 1)

        self.assertTrue(ok)
        self.assertEqual(d, {'a': 2})

    def test_deep(self):
        d = {'a': {'b': {'c': 1, 'd': 1}}}

        ok = update_in(d, ('a', 'b', 'c'), add, 1)

        self.assertTrue(ok)
        self.assertEqual(d, {'a': {'b': {'c': 2, 'd': 1}}})

    def test_new_key(self):
        d = {'a': 1}

        ok = update_in(d, ('b',), fnone(add, 0), 1)

        self.assertTrue(ok)
        self.assertEqual(d, {'a': 1, 'b': 1})

    def test_new_key_deep(self):
        d = {'a': {'b': {'c': 1}}}
        expected = deepcopy(d)
        expected['a']['b']['z'] = 1

        ok = update_in(d, ('a', 'b', 'z'), fnone(add, 0), 1)

        self.assertTrue(ok)
        self.assertEqual(d, expected)
