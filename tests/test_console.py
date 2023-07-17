#!/usr/bin/python3

"""a test module for console.py"""


import io
import unittest
import unittest.mock
from console import process_input as pi
from console import HBNBCommand as cc


class TestProcessImput(unittest.TestCase):
    """TestCase for process_input"""
    def test_empty_input(self):
        """test when empty string is supplied"""
        a = pi("")
        self.assertListEqual(a, [])

    def test_non_empty_input(self):
        """test when a string is passed"""
        a = pi("-c hello")
        b = pi("he ,he he")
        c = pi("{hello all}")
        d = pi("[hello all]")
        self.assertListEqual(a, ['-c', 'hello'])
        self.assertListEqual(b, ['he', 'he', 'he'])
        self.assertListEqual(c, ['{hello all}'])
        self.assertListEqual(d, ['[hello all]'])

    def test_no_arg_passed(self):
        """test when no argument is passed"""
        with self.assertRaises(TypeError):
            a = pi()


class TestHBNBCommand(unittest.TestCase):
    """TestCase for HBNBCommand"""
    def test_do_EOF(self):
        """test the do_EOF method"""
        self.assertTrue(cc().do_EOF("arg"))

    def test_do_quit(self):
        """test the do_quit method"""
        self.assertTrue(cc().do_quit("arg"))

    def test_default(self):
        """test the do_default method"""
        c = cc()
        a = c.default("zzz")
        b = c.default("yyy \a")
        self.assertFalse(a)
        self.assertFalse(b)

    def test_do_all(self):
        """test the do_all method"""
        out = io.StringIO
        with unittest.mock.patch('sys.stdout', new_callable=out) as stdout:
            cc().do_all("zzz")
            self.assertEqual(stdout.getvalue(), "** class doesn't exist **\n")
        with unittest.mock.patch('sys.stdout', new_callable=out) as stdout:
            cc().do_all("User")
            self.assertEqual(stdout.getvalue(), "[]\n")


if __name__ == "__main__":
    unittest.main()
