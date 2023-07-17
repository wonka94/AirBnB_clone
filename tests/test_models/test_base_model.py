#!/usr/bin/python3

"""a test module for base_model"""


import unittest
from datetime import datetime
from time import sleep
from models import base_model as bm


class TestBaseModel(unittest.TestCase):
    """a TestCase for testing BaseModel"""

    def test_contains_correct_attributes(self):
        """test if a BaseModel object contains correct attributes"""
        a = bm.BaseModel("args")
        self.assertTrue(hasattr(a, "id"))
        self.assertTrue(hasattr(a, "created_at"))
        self.assertTrue(hasattr(a, "updated_at"))
        self.assertTrue(hasattr(a, "save"))
        self.assertTrue(hasattr(a, "to_dict"))
        self.assertNotIn("args", a.__dict__.values())

    def test_str_represention(self):
        """test the string representation of BaseModel"""
        a = bm.BaseModel()
        self.assertEqual(str(a), f"[BaseModel] ({a.id}) {a.__dict__}")

    def test_attribute_is_unique_and_of_correct_type(self):
        """test if object sttributes is of correct type"""
        b1 = bm.BaseModel()
        sleep(0.05)
        b2 = bm.BaseModel()
        self.assertNotEqual(b1.id, b2.id)
        self.assertLess(b1.created_at, b2.created_at)
        self.assertEqual(b1.created_at, b1.updated_at)
        self.assertIsInstance(b1.id, str)
        self.assertIsInstance(b1.created_at, datetime)
        self.assertIsInstance(b1.updated_at, datetime)


if __name__ == "__main__":
    unittest.main()
