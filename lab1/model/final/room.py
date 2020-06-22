import sqlalchemy as sql
from sqlalchemy.orm import relationship

from . import Base


class Room(Base):
    __tablename__ = 'f_room'

    id = sql.Column(sql.Integer, sql.Sequence('f_room_seq_id'), primary_key=True)

    dormitory_id = sql.Column(sql.Integer, sql.ForeignKey('f_dormitory.id'))
    dormitory = relationship('Dormitory')

    room_number = sql.Column(sql.String(5))
    insects = sql.Column(sql.Boolean)
    max_person = sql.Column(sql.Integer)
    latest_debug = sql.Column(sql.Date)

    def serialize(self):
        return {
            'id': self.id,
            'dormitory': self.dormitory.serialize() if self.dormitory is not None else None,
            'room_number': self.room_number,
            'insects': self.insects,
            'max_person': self.max_person,
            'last_debug': self.latest_debug
        }