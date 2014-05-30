from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String
)

from bottleplate.app.models import Base


class User(Base):
    """Model of a user."""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    birthdate = Column(DateTime)

    def __init__(self):
        self.firstname = ''
        self.lastname = ''
