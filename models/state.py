#!/usr/bin/python3
"""Defines the State class."""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv
from models.city import City

class State(BaseModel, Base):
    """Represents a state for a SQL database."""
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete", backref="state")

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """Gets a list of City instances with state_id matching this State's id."""
            from models import storage
            all_cities = storage.all(City)
            return [city for city in all_cities.values() if city.state_id == self.id]
