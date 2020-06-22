import sqlalchemy as sql
from . import Base


class Discipline(Base):
    __tablename__ = 'discipline'

    id = sql.Column(sql.Integer, autoincrement=True, primary_key=True)

    university_name = sql.Column(sql.String, nullable=False)
    standard = sql.Column(sql.String, nullable=False)
    name = sql.Column(sql.String, nullable=False)
    faculty = sql.Column(sql.String, nullable=False)
    specialty = sql.Column(sql.String, nullable=False)
    term = sql.Column(sql.Integer, nullable=False)
    lecture_hours = sql.Column(sql.Integer, nullable=False)
    practice_hours = sql.Column(sql.Integer, nullable=False)
    laboratory_hours = sql.Column(sql.Integer, nullable=False)
    is_exam = sql.Column(sql.Boolean, nullable=False)


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