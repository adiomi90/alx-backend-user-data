#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """
    A class representing a database connection and operations.

    Attributes:
        _engine: The SQLAlchemy engine used for database connection.
        __session: The SQLAlchemy session used for database operations.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the DB class.

        Creates the database engine, drops existing tables, creates new tables,
        and initializes the session.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Gets the SQLAlchemy session.

        If the session is not yet initialized, creates a
        new session and returns it.

        Returns:
            The SQLAlchemy session.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database.

        Args:
            email: The email of the user.
            hashed_password: The hashed password of the user.

        Returns:
            The created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user in the database based on the given criteria.

        Args:
            **kwargs: Keyword arguments representing the search criteria.

        Returns:
            The found User object.

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
        """
        Updates a user in the database.

        Args:
            user_id: The ID of the user to update.
            **kwargs: Keyword arguments representing the
            fields to update.

        Raises:
            ValueError: If the user with the given ID is not
            found or an invalid field is provided.
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
