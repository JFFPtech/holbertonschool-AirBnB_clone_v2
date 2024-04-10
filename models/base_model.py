#!/usr/bin/python3
"""Defines a base class for all models in the hbnb clone."""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from datetime import datetime
from os import getenv
import models
import uuid

time_fmt = "%Y-%m-%dT%H:%M:%S.%f"

Base = declarative_base() if getenv("HBNB_TYPE_STORAGE") == 'db' else object

class BaseModel:
    """A base class for all hbnb models."""

    if getenv("HBNB_TYPE_STORAGE") == 'db':
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initializes a new model instance."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        for key, value in kwargs.items():
            if key not in ['__class__', 'created_at', 'updated_at']:
                setattr(self, key, value)
        if 'created_at' in kwargs:
            self.created_at = datetime.strptime(kwargs['created_at'], time_fmt) if isinstance(kwargs['created_at'], str) else self.created_at
        if 'updated_at' in kwargs:
            self.updated_at = datetime.strptime(kwargs['updated_at'], time_fmt) if isinstance(kwargs['updated_at'], str) else self.updated_at

    def __str__(self):
        """Returns a string representation of the instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates the instance's updated_at timestamp and saves to storage."""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, save_to_disk=False):
        """Converts instance into a dictionary format."""
        new_dict = {**self.__dict__, "__class__": self.__class__.__name__}
        new_dict["created_at"] = self.created_at.isoformat() if 'created_at' in new_dict else new_dict["created_at"]
        new_dict["updated_at"] = self.updated_at.isoformat() if 'updated_at' in new_dict else new_dict["updated_at"]
        new_dict.pop('_sa_instance_state', None)
        if '_password' in new_dict:
            new_dict['password'] = new_dict.pop('_password')
        new_dict.pop('amenities', None)
        new_dict.pop('reviews', None)
        if not save_to_disk:
            new_dict.pop('password', None)
        return new_dict

    def delete(self):
        """Deletes the current instance from storage."""
        models.storage.delete(self)
