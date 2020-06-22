import sqlalchemy as sql
from sqlalchemy.orm import relationship

from . import Base


class Rating(Base):
    __tablename__ = 'rating'

    id = sql.Column(sql.Integer, autoincrement=True, primary_key=True)

    discipline_id = sql.Column(sql.Integer, sql.ForeignKey('discipline.id'))
    discipline = relationship('Discipline')
    rating = sql.Column(sql.Integer, nullable=False)
    date = sql.Column(sql.DateTime, nullable=False)
    teacher_name = sql.Column(sql.String, nullable=False)
    teacher_id = sql.Column(sql.Integer, nullable=False)
    student_name = sql.Column(sql.String, nullable=False)
    student_id = sql.Column(sql.Integer, nullable=False)
    
    
    def serialize(self):
        return {
            'id': self.id,
            'discipline': self.discipline.serialize() if self.discipline is not None else None,
            'rating': self.rating,
            'date': str(self.date),
            'teacher_name': self.teacher_name,
            'teacher_id': self.teacher_id,
            'student_name': self.student_name,
            'student_id': self.student_id,
        }