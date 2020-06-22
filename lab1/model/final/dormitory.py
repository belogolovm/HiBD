import sqlalchemy as sql
from sqlalchemy.orm import relationship

from . import Base


class Dormitory(Base):
    __tablename__ = 'f_dormitory'

    id = sql.Column(sql.Integer, sql.Sequence('f_dormitory_seq_id'), primary_key=True)

    name = sql.Column(sql.String(100))
    total_rooms = sql.Column(sql.Integer)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'total_rooms': self.total_rooms
        }