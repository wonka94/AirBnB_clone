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
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(value, time_format)
                else:
                    self.__dict__[key] = value
        else:
            models.storage.new(self)

    def save(self):
        """Update updated_at with the current datetime."""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """
           Creates a dictionary representation of the BaseModel instance.

           Returns:
                A dictionary representation of the BaseModel instance.
        """

        instance_dict = self.__dict__.copy()
        instance_dict["created_at"] = self.created_at.isoformat()
        instance_dict["updated_at"] = self.updated_at.isoformat()
        instance_dict["__class__"] = self.__class__.__name__
        return instance_dict

    def __str__(self):
        """Return the string representation of the BaseModel instance."""

        className = self.__class__.__name__
        return "[{}] ({}) {}".format(className, self.id, self.__dict__)
