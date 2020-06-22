import sqlalchemy as sql
from sqlalchemy.orm import relationship

from . import Base

class LibraryRecord(Base):
    __tablename__ = 'f_library_record'

    id = sql.Column(sql.Integer, sql.Sequence('f_library_record_seq_id'), primary_key=True)

    book_name = sql.Column(sql.String(100))
    taken_by_id = sql.Column(sql.Integer, sql.ForeignKey('f_person.id'))
    taken_by = relationship('Person')

    taken_at_id = sql.Column(sql.Date, sql.ForeignKey('f_time.id'))
    taken_at = relationship('FinalTime', foreign_keys=[taken_at_id])
    returned_at_id = sql.Column(sql.Date, sql.ForeignKey('f_time.id'))
    returned_at = relationship('FinalTime', foreign_keys=[returned_at_id])

    def serialize(self):
        return {
            'id': self.id,
            'book_name': self.book_name,
            'taken_by': self.taken_by.serialize(),
            'taken_at': self.taken_at,
            'returned_at': self.returned_at,
        }