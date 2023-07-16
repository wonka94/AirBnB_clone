#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Represents an abstracted storage engine.

    Attributes:
        __file_path (str): Path to the JSON file.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "save_file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        object_class = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(object_class, obj.id)] = obj

    def save(self):
        """Serialize __objects to the JSON file."""
        object_dict = FileStorage.__objects
        s_obj = {obj: object_dict[obj].to_dict() for obj in object_dict.keys()}
        with open(FileStorage.__file_path, "w") as fi:
            json.dump(s_obj, fi)

    def reload(self):
        """Deserializes the JSON file to __objects if it exists."""
        try:
            with open(FileStorage.__file_path) as fi:
                object_dict = json.load(fi)
                for obj_value in object_dict.values():
                    className = obj_value["__class__"]
                    del obj_value["__class__"]
                    self.new(eval(className)(**obj_value))
        except FileNotFoundError:
            return
