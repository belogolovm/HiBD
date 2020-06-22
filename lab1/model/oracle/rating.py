import sqlalchemy as sql
from sqlalchemy.orm import relationship

from . import Base


class Rating(Base):
    __tablename__ = 'oracle_rating'

    id = sql.Column(sql.Integer, sql.Sequence('rating_seq_id'), primary_key=True)

    discipline = sql.Column(sql.String(200), nullable=False)
    rating = sql.Column(sql.Integer, nullable=False)
    rating_letter = sql.Column(sql.String(2), nullable=False)
    date = sql.Column(sql.DateTime, nullable=False)
    student_id = sql.Column(sql.Integer, sql.ForeignKey('oracle_person.id'), nullable=False)
    student = relationship('OraclePerson', foreign_keys=[student_id])
    
    def serialize(self):
        return {
            'id': self.id,
            'discipline': self.discipline,
            'rating': self.rating,
            'date': str(self.date),
            'student': self.student.serialize(),
        }