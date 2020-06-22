import sqlalchemy as sql
from . import Base


class Discipline(Base):
    __tablename__ = 'f_discipline'

    id = sql.Column(sql.Integer, sql.Sequence('f_discipline_seq_id'), primary_key=True)

    university_name = sql.Column(sql.String(100))
    standard = sql.Column(sql.String(10))
    name = sql.Column(sql.String(100))
    faculty = sql.Column(sql.String(100))
    specialty = sql.Column(sql.String(100))
    term = sql.Column(sql.Integer)
    lecture_hours = sql.Column(sql.Integer)
    practice_hours = sql.Column(sql.Integer)
    laboratory_hours = sql.Column(sql.Integer)
    is_exam = sql.Column(sql.Boolean)


    def serialize(self):
        return {
            'id': self.id,
            'university_name': self.university_name,
            'standard': self.standard,
            'name': self.name,
            'faculty': self.faculty,
            'specialty': self.specialty,
            'term': self.term,
            'lecture_hours': self.lecture_hours,
            'practice_hours': self.practice_hours,
            'laboratory_hours': self.laboratory_hours,
            'is_exam': self.is_exam
        }