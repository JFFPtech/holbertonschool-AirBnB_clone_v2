#!/usr/bin/python3
"""DBStorage module"""
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import Base
from models.state import State
from models.city import City
from os import getenv
from sqlalchemy.ext.declarative import declarative_base

class DBStorage:
    """Manages storage of hbnb models in a SQL database."""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the database engine."""
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        db = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(f'mysql+mysqldb://{user}:{password}@localhost/{db}',
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            # Drop all tables if the environment is set for testing
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of all objects of a given class."""
        if cls is None:
            cls = [State, City]
        elif not isinstance(cls, list):
            cls = [cls]
        
        objects = {}
        for model in cls:
            session_query = self.__session.query(model).all()
            for obj in session_query:
                key = f"{obj.__class__.__name__}.{obj.id}"
                objects[key] = obj
        return objects

    def new(self, obj):
        """Adds a new object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commits all changes to the database."""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the current database session."""
        if obj:
            self.__session.delete(obj)

    def get(self, cls, id):
        """Method to retrieve one object of class cls from the database by id."""
        if cls and id:
            return self.__session.query(cls).get(id)
        return None

    def reload(self):
        """Recreates the database schema and initializes a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)()

    def close(self):
        """Disposes of the current Session."""
        self.__session.close()
