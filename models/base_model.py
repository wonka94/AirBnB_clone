#!/usr/bin/python3
"""Defines the BaseModel class."""

import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """HBnB project BaseModel class"""

    def __init__(self, *args, **kwargs):
        """
            Initialize the object's attributes.

            args: Variable length argument list.
            kwargs: Arbitrary keyword arguments.
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()

        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key in ["creation_time", "last_updated"]:
                    self.__dict__[key] = datetime.strptime(value, time_format)
                else:
                    self.__dict__[key] = value
        else:
            models.file_storage.new(self)

    def __str__(self):
        """Return the string representation of the BaseModel instance."""

        className = self.__class__.__name__
        return "[{}] ({}) {}".format(className, self.id, self.__dict__)

    def to_dict(self):
        """
           Creates a dictionary representation of the BaseModel instance.

           Returns:
                A dictionary representation of the BaseModel instance.
        """

        dictionary = self.__dict__.copy()
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()
        dictionary["__class__"] = self.__class__.__name__
        return instance_dict

    def save(self):
        """Update updated_at with the current datetime."""
        self.updated_at = datetime.today()
        models.file_storage.save()
