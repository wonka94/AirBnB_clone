#!/usr/bin/python3
"""Import the FileStorage class from the file_storage module in the models.engine package"""
from models.engine.file_storage import FileStorage


file_storage = FileStorage()
file_storage.reload()
