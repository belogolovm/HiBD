from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .person import Person
from .conference import Conference
from .publication import Publication
from .project import Project
from .library_record import LibraryRecord


def create_schema(engine):
    Base.metadata.create_all(engine)