"""a test module for beautiful_code_that_passes_pycodestyle.py"""


import unittest

import beautiful_code_that_passes_pycodestyle as de
from beautiful_code_that_passes_pycodestyle import DemoClass
from beautiful_code_that_passes_pycodestyle import demo_function


class DemoTest(unittest.TestCase):
    """a demo test class"""

    def test_demo(self):
        """a demo test method"""
        demo_class = DemoClass()
        self.assertIsInstance(demo_class, DemoClass)
        self.assertTrue(hasattr(demo_class, "demo_method"))
        self.assertTrue("demo_function" in dir(de))
