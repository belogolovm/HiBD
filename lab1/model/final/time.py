import sqlalchemy as sql
from sqlalchemy.orm import relationship

from . import Base


class FinalTime(Base):
    __tablename__ = 'f_time'

    id = sql.Column(sql.Date, primary_key=True)

    year = sql.Column(sql.Integer)
    year_id = sql.Column(sql.Integer)
    term = sql.Column(sql.String(20))
    term_id = sql.Column(sql.Integer)

    end_year = sql.Column(sql.Date)
    end_term = sql.Column(sql.Date)

    def serialize(self):
        return {
            'id': self.id,
            'year': self.year,
            'year_id': self.year_id,
            'term': self.term,
            'term_id': self.term_id,
        }