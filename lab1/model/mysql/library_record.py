import sqlalchemy as sql
from sqlalchemy.orm import relationship

from lab1.model.mysql.project import project_person
from . import Base

from .conference import conference_person
from .publication import publication_person

class LibraryRecord(Base):
    __tablename__ = 'library_record'

    id = sql.Column(sql.Integer, autoincrement=True, primary_key=True)

    book_name = sql.Column(sql.String(100), nullable=False)
    taken_by_id = sql.Column(sql.Integer, sql.ForeignKey('person.id'), nullable=False)
    taken_by = relationship('Person')

    taken_at = sql.Column(sql.Date, nullable=False)
    returned_at = sql.Column(sql.Date)

    def serialize(self):
        return {
            'id': self.id,
            'book_name': self.book_name,
            'taken_by': self.taken_by.serialize(),
            'taken_at': self.taken_at,
            'returned_at': self.returned_at,
        }