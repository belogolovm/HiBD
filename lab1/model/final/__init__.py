from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .conference import Conference
from .discipline import Discipline
from .dormitory import Dormitory
from .dormitory_person import DormitoryPerson
from .group import Group
from .lesson_record import LessonRecord
from .library_record import LibraryRecord
from .person import Person
from .project import Project
from .publication import Publication
from .rating import Rating
from .room import Room
from .time import FinalTime


def drop_schema(engine):
    # Base.metadata.drop_all(engine)
    pass

def create_schema(engine):
    Base.metadata.create_all(engine)