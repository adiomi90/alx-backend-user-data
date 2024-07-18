#!/usr/bin/env python3
""" DB module for the user authentication service. """

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """Class representing the database for the user authentication service."""

    def __init__(self) -> None:
        """Initialize a new DB instance."""
        self._engine = create_engine("sqlite:///a.db",
                                     echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Get the session object for the database."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The newly created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user in the database based on the given criteria.

        Args:
            **kwargs: Keyword arguments representing the search criteria.

        Returns:
            User: The found User object.

        Raises:
            NoResultFound: If no user is found matching the criteria.
            InvalidRequestError: If an invalid search criteria is provided.
        """
        all_users = self._session.query(User)
        for k, v in kwargs.items():
            if k not in User.__dict__:
                raise InvalidRequestError
            for usr in all_users:
                if getattr(usr, k) == v:
                    return usr
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user in the database with the given attributes.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Keyword arguments representing the attributes to update.

        Raises:
            ValueError: If the user with the given ID is not found or if an
            invalid attribute is provided.
        """
        try:
            usr = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError()
        for k, v in kwargs.items():
            if hasattr(usr, k):
                setattr(usr, k, v)
            else:
                raise ValueError
        self._session.commit()
