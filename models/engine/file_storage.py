#!/usr/bin/python3
"""This module defines the FileStorage class"""
import json

class FileStorage:
    """This class manages storage of JSON file"""
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns the dictionary of all objects"""
        if cls:
            objects = {}
            for key, obj in FileStorage.__objects.items():
                if isinstance(obj, cls):
                    objects[key] = obj
            return objects
        else:
            return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        serialized_objs = {}
        for key, value in FileStorage.__objects.items():
            serialized_objs[key] = value.to_dict()
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as file:
            json.dump(serialized_objs, file)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as file:
                serialized_objs = json.load(file)
                for key, value in serialized_objs.items():
                    class_name, obj_id = key.split('.')
                    module = __import__("models." + class_name.lower(), fromlist=[class_name])
                    class_ = getattr(module, class_name)
                    obj = class_(**value)
                    FileStorage.__objects[key] = obj
        except FileNotFoundError:
            pass

    def close(self):
        """Call reload() method for deserializing the JSON file to objects"""
        self.reload()
