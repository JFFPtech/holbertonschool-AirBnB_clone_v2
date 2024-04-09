#!/usr/bin/python3
"""This module defines the State class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """This class defines the states table"""
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete", backref="state")

    @property
    def cities(self):
        """Getter method to return the list of City objects linked to the current State"""
        from models import storage
        city_objs = []
        cities_dict = storage.all(City)
        for city in cities_dict.values():
            if city.state_id == self.id:
                city_objs.append(city)
        return city_objs
