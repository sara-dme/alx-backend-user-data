#!/usr/bin/env python3
"""DB module ___
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DataBase class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Add user to database"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """ find a user by key word args """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
        except NoResultFound:
            raise
        except InvalidRequestError:
            raise
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user attributes"""
        user = self.find_user_by(id=user_id)
        for key, val in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, val)
            else:
                raise ValueError
        self._session.commit()
