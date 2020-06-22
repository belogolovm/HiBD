import sqlalchemy as sql
from sqlalchemy.orm import relationship

from . import Base


class Rating(Base):
    __tablename__ = 'f_rating'

    id = sql.Column(sql.Integer, sql.Sequence('f_rating_seq_id'), primary_key=True)

    discipline_id = sql.Column(sql.Integer, sql.ForeignKey('f_discipline.id'))
    discipline = relationship('Discipline')
    rating = sql.Column(sql.Integer)
    rating_letter = sql.Column(sql.String(2))
    date_id = sql.Column(sql.Date, sql.ForeignKey('f_time.id'))
    date = relationship('FinalTime')
    teacher_id = sql.Column(sql.Integer, sql.ForeignKey('f_person.id'))
    teacher = relationship('Person', foreign_keys=[teacher_id])
    student_id = sql.Column(sql.Integer, sql.ForeignKey('f_person.id'))
    student = relationship('Person', foreign_keys=[student_id])
    
    def serialize(self):
        return {
            'id': self.id,
            'discipline': self.discipline.serialize() if self.discipline is not None else None,
            'rating': self.rating,
            'date': str(self.date),
            'teacher': self.teacher.serialize() if self.teacher is not None else None,
            'student': self.student.serialize() if self.student is not None else None,
        }