from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .discipline import Discipline
from .rating import Rating


def create_schema(engine):
    Base.metadata.create_all(engine)