#!/usr/bin/python3
"""Import the FileStorage class from the file_storage module in the models.engine package"""
from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
