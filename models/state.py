#!/usr/bin/python3
"""This module defines the State class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv
from models.city import City


class State(BaseModel, Base):
    """This class defines the states table"""
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete", backref="state")

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """Returns the list of City instances with state_id equal to the
            current State.id"""
            from models import storage
            cities = storage.all(City)
            return [city for city in cities.values() if city.state_id == self.id]