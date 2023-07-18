#!/usr/bin/python3

"""a test module for base_model"""


import os
import unittest
from datetime import datetime
from time import sleep

from models import base_model as bm
import models


class TestBaseModel(unittest.TestCase):
    """a TestCase for testing BaseModel"""

    def test_contains_correct_attributes(self):
        """test if a BaseModel object contains correct attributes"""
        a = bm.BaseModel()
        self.assertTrue(hasattr(a, "id"))
        self.assertTrue(hasattr(a, "created_at"))
        self.assertTrue(hasattr(a, "updated_at"))
        self.assertTrue(hasattr(a, "save"))
        self.assertTrue(hasattr(a, "to_dict"))
        # test when the attribute 'args' is not used.
        b = bm.BaseModel(None)
        self.assertNotIn(None, b.__dict__.values())
        # test_when_kwargs_passed_is_empty
        empty_dict = {}
        c = bm.BaseModel(**empty_dict)
        self.assertEqual(len(c.__dict__), 3)
        self.assertTrue(hasattr(c, "id"))
        self.assertTrue(hasattr(c, "created_at"))
        self.assertTrue(hasattr(c, "updated_at"))
        # test_when_kwargs_passed_is_not_empty
        non_empty_dict = {"created_at": "2017-06-14T22:31:03.285259",
                          "updated_at": "2017-06-14T22:31:03.285259",
                          "project": "AirBnB"}
        d = bm.BaseModel(**non_empty_dict)
        self.assertEqual(d.created_at,
                         datetime.strptime(non_empty_dict["created_at"],
                                           "%Y-%m-%dT%H:%M:%S.%f"))
        self.assertEqual(d.updated_at,
                         datetime.strptime(non_empty_dict["updated_at"],
                                           "%Y-%m-%dT%H:%M:%S.%f"))
        self.assertTrue('project' in d.__dict__
                        and 'AirBnB' == d.__dict__['project'])
        self.assertEqual(d.project, "AirBnB")
        # test when args and kwargs are passed, BaseModel should ignore args
        non_empty_dict = {"created_at": "2017-06-14T22:31:03.285259",
                          "updated_at": "2017-06-14T22:31:03.285259",
                          "project": "AirBnB"}
        e = bm.BaseModel("1234", **non_empty_dict)
        self.assertNotIn("1234", e.__dict__.values())
        self.assertTrue(hasattr(e, "project"))
        self.assertEqual(e.project, "AirBnB")
        self.assertEqual(e.created_at,
                         datetime.strptime(non_empty_dict["created_at"],
                                           "%Y-%m-%dT%H:%M:%S.%f"))
        self.assertEqual(d.updated_at,
                         datetime.strptime(non_empty_dict["updated_at"],
                                           "%Y-%m-%dT%H:%M:%S.%f"))
        self.assertTrue('project' in e.__dict__
                        and 'AirBnB' == e.__dict__['project'])

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

    def test_methods_behave_correctly(self):
        """test if all methods in BaseModel behave correctly"""
        b = bm.BaseModel()
        # test save() method
        self.assertEqual(b.created_at, b.updated_at)
        sleep(0.05)
        b.save()
        self.assertNotEqual(b.created_at, b.updated_at)
        self.assertLess(b.created_at, b.updated_at)
        # test to_dict() method
        sut_dict = b.to_dict()
        self.assertIsInstance(sut_dict, dict)
        self.assertIn('__class__', sut_dict)
        self.assertIn('id', sut_dict)
        self.assertIn('created_at', sut_dict)
        self.assertIn('updated_at', sut_dict)
        self.assertEqual(b.created_at.isoformat(), sut_dict['created_at'])
        self.assertEqual(b.updated_at.isoformat(), sut_dict['updated_at'])
        self.assertEqual(len(sut_dict), 4)
        self.assertDictEqual(sut_dict, {'__class__': b.__class__.__name__,
                                        'id': b.id,
                                        'created_at': b.created_at.isoformat(),
                                        'updated_at': b.updated_at.isoformat()
                                        })

    def test_new_method_not_called_when_dict_obj_is_passed_to_BaseModel(self):
        """
        Test that storage.new() is not called when a BaseModel obj is
        created from a dict object
        """
        non_empty_dict = {"created_at": datetime.utcnow().isoformat(),
                          "updated_at": datetime.utcnow().isoformat(),
                          "name": "Vanbliser"}
        b = bm.BaseModel(**non_empty_dict)
        self.assertTrue(b not in models.storage.all().values(),
                        "{}".format(models.storage.all().values()))
        del b

        b = bm.BaseModel()
        self.assertTrue(b in models.storage.all().values())

    def test_that_save_method_updates_updated_at_attr(self):
        """
        Checks that save() method updates 'updated_at' attribute
        """
        b = bm.BaseModel()
        sleep(0.02)
        temp_update = b.updated_at
        b.save()
        self.assertLess(temp_update, b.updated_at)

    def test_that_save_can_update_two_or_more_times(self):
        """
        Tests that the save method updates 'updated_at' two times
        """
        b = bm.BaseModel()
        sleep(0.02)
        temp_update = b.updated_at
        b.save()
        sleep(0.02)
        temp1_update = b.updated_at
        self.assertLess(temp_update, temp1_update)
        sleep(0.01)
        b.save()
        self.assertLess(temp1_update, b.updated_at)

    '''
     def test_save_update_file(self):
        """
        Tests if file is updated when the 'save' is called
        """
        b = bm.BaseModel()
        b.save()
        bid = "BaseModel.{}".format(b.id)
        with open("file.json", encoding="utf-8") as f:
            self.assertIn(bid, f.read())
    '''
    def test_that_to_dict_contains_correct_keys(self):
        """
        Checks whether to_dict() returns the expected key
        """
        b_dict = bm.BaseModel().to_dict()
        attrs = ("id", "created_at", "updated_at", "__class__")
        for attr in attrs:
            self.assertIn(attr, b_dict)

    def test_to_dict_contains_added_attributes(self):
        """
        Checks that new attributes are also returned by to_dict()
        """
        b = bm.BaseModel()
        attrs = ["id", "created_at", "updated_at", "__class__"]
        b.name = "Vanbliser"
        b.email = "firduas@gmail.com"
        attrs.extend(["name", "email"])
        for attr in attrs:
            self.assertIn(attr, b.to_dict())

    def test_to_dict_output(self):
        """
        Checks the output returned by to_dict()
        """
        b = bm.BaseModel()
        dt = datetime.now()
        b.id = "12345"
        b.created_at = b.updated_at = dt
        test_dict = {
            'id': "12345",
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
            '__class__': 'BaseModel'
        }
        self.assertDictEqual(test_dict, b.to_dict())

    def test_to_dict_with_args(self):
        """
        Checks that TypeError is returned when argument is passed to to_dict()
        """
        b = bm.BaseModel()
        with self.assertRaises(TypeError):
            b.to_dict(None)

    def test_to_dict_not_dunder_dict(self):
        """Checks that to_dict() is a dict object not equal to __dict__"""
        b = bm.BaseModel()
        self.assertNotEqual(b.to_dict(), b.__dict__)


if __name__ == "__main__":
    unittest.main()
